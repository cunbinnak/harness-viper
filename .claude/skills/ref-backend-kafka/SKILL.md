---
name: ref-backend-kafka
description: Pattern Kafka cho backend — config đầy đủ (producer idempotent/acks, consumer manual-ack/JSON, error handler + DLT), EventPublisher + Consumer đầy đủ function, publish after-commit, consumer idempotent. Load khi BUILD backend target phát/nhận event.
---

> Situational ref cho stack-spring-boot — load khi boundary dùng Kafka.
# Reference: Backend Kafka (event producer + consumer)

> **Load khi:** BUILD backend target phát/nhận Kafka event (`build.md` Bước 3 nêu khi nào nạp).
> **Quan hệ:** convention bắt buộc → `stack-spring-boot`; contract event → `docs/arch/{name}.md §5`; config nâng cao → `ref-backend-config`.
> **Nguyên tắc:** publish **sau commit DB**; consumer **idempotent**; payload là **DTO/record tường minh** (không raw `Map`); topic/group/retry từ **config**.

## 1. Config — producer + consumer + error handler

`application.yml`:
```yaml
spring:
  kafka:
    bootstrap-servers: ${KAFKA_SERVER_HOST:localhost:9092}
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      acks: all                         # bền vững — chờ ISR ack
      properties:
        enable.idempotence: true        # producer không gửi trùng khi retry
    consumer:
      group-id: ${KAFKA_GROUP:order-service}
      auto-offset-reset: earliest
      enable-auto-commit: false         # commit thủ công (ack-mode manual)
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring.json.trusted.packages: "com.example.*"   # KHÔNG để "*"
    listener:
      ack-mode: manual

app:
  kafka:
    topics:
      order-created: ${TOPIC_ORDER_CREATED:order.created.v1}    # topic name từ config, có version
```

```java
// topic name từ config (không hardcode trong code)
@ConfigurationProperties(prefix = "app.kafka")
public record KafkaTopics(Map<String, String> topics) {
    public String of(String key) { return topics.get(key); }
}

@Configuration
@EnableConfigurationProperties(KafkaTopics.class)
class KafkaConfig {

    // Retry + Dead Letter Topic: fail N lần -> đẩy sang {topic}.DLT
    @Bean
    DefaultErrorHandler kafkaErrorHandler(KafkaTemplate<String, Object> template) {
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(template);
        DefaultErrorHandler handler = new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 3));
        handler.addNotRetryableExceptions(BusinessException.class);   // lỗi nghiệp vụ không retry
        return handler;
    }

    // Truy vết xuyên service: lấy X-Request-ID của record vào MDC traceId (ref-backend-logging §3).
    // Boot tự gắn bean RecordInterceptor duy nhất vào container factory mặc định.
    @Bean
    RecordInterceptor<String, Object> mdcRecordInterceptor() {
        return new RecordInterceptor<>() {
            @Override
            public ConsumerRecord<String, Object> intercept(ConsumerRecord<String, Object> rec, Consumer<String, Object> consumer) {
                Header h = rec.headers().lastHeader(HeaderConstants.REQUEST_ID);
                MDC.put(LogConstants.TRACE_ID, h != null ? new String(h.value(), StandardCharsets.UTF_8) : UUID.randomUUID().toString());
                return rec;
            }
            @Override
            public void afterRecord(ConsumerRecord<String, Object> rec, Consumer<String, Object> consumer) {
                MDC.clear();
            }
        };
    }
}
```

> `KafkaTemplate<String,Object>`, `ProducerFactory`, `ConsumerFactory`, container factory: Spring Boot tự cấu hình từ yml — chỉ khai bean khi cần custom (vd error handler/DLT trên).

## 2. Event payload (DTO tường minh)

```java
// payload/OrderCreatedEvent.java — record, có eventId để consumer dedup
public record OrderCreatedEvent(
        String eventId,         // UUID — khóa idempotency
        long orderId,
        String tenantId,
        Instant occurredAt) {}
```

## 3. Producer — EventPublisher + publish after-commit

```java
// interface
public interface EventPublisher {
    void publish(String topicKey, String partitionKey, Object event);   // topicKey -> KafkaTopics.of(...)
}

// impl
@Service
@RequiredArgsConstructor                            // KHÔNG viết constructor tay
class KafkaEventPublisher implements EventPublisher {
    private final KafkaTemplate<String, Object> template;
    private final KafkaTopics topics;
    @Override
    public void publish(String topicKey, String partitionKey, Object event) {
        ProducerRecord<String, Object> rec = new ProducerRecord<>(topics.of(topicKey), partitionKey, event);   // partitionKey giữ ordering theo entity
        String traceId = MDC.get(LogConstants.TRACE_ID);                    // AFTER_COMMIT chạy cùng thread request → MDC còn
        if (traceId != null) rec.headers().add(HeaderConstants.REQUEST_ID, traceId.getBytes(StandardCharsets.UTF_8));
        template.send(rec);
    }
}
```

```java
// PUBLISH AFTER-COMMIT: service phát domain event; chỉ gửi Kafka khi DB đã commit
@Service
@RequiredArgsConstructor
class OrderCommandService {
    private final OrderRepository repository;
    private final ApplicationEventPublisher domainEvents;   // Spring in-process
    @Transactional
    public void create(CreateOrderCommand cmd) {
        Order order = repository.save(Order.create(cmd));
        domainEvents.publishEvent(new OrderCreatedEvent(
            UUID.randomUUID().toString(), order.getId(), cmd.tenantId(), Instant.now()));
    }
}

@Component
@RequiredArgsConstructor
class OrderEventRelay {
    private final EventPublisher publisher;
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)   // chỉ gửi sau commit
    void on(OrderCreatedEvent e) {
        publisher.publish("order-created", String.valueOf(e.orderId()), e);
    }
}
```

## 4. Consumer — idempotent + manual ack

```java
@Component
@RequiredArgsConstructor
class OrderEventConsumer {

    private final ProcessedEventStore processed;   // dedup store (DB/Redis)
    private final OrderProjectionService projection;

    @KafkaListener(topics = "#{@kafkaTopics.of('order-created')}", groupId = "${spring.kafka.consumer.group-id}")
    void onOrderCreated(OrderCreatedEvent event, Acknowledgment ack) {
        if (processed.exists(event.eventId())) {     // IDEMPOTENT: đã xử lý -> bỏ qua
            ack.acknowledge();
            return;
        }
        projection.apply(event);                     // xử lý nghiệp vụ (idempotent về mặt hiệu ứng)
        processed.markProcessed(event.eventId());
        ack.acknowledge();                           // commit offset sau khi xử lý xong
    }
}
```

## 5. Idempotency store

```java
public interface ProcessedEventStore {
    boolean exists(String eventId);
    void markProcessed(String eventId);   // lưu eventId (DB unique / Redis SETNX + TTL)
}
```
- Dedup theo `eventId` / `transaction id` / idempotency key — KHÔNG xử lý trùng.
- Kafka là **at-least-once** → consumer PHẢI idempotent (DB unique constraint hoặc store ở trên).

## 6. Error handling
- `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`: retry theo `FixedBackOff` rồi đẩy `{topic}.DLT` (xem §1).
- Lỗi nghiệp vụ (`BusinessException`) → **không retry** (`addNotRetryableExceptions`), đẩy DLT/skip.
- KHÔNG để exception nuốt im lặng; log có `eventId` + context (không log payload nhạy cảm).
- KHÔNG xử lý nặng/blocking lâu trong listener → tách async/batch nếu cần.

## Anti-patterns (review flag)
- Publish event **trong** transaction (trước commit) → DB rollback nhưng event đã gửi.
- Consumer không idempotent → xử lý trùng khi redelivery.
- Payload raw `Map` thay vì DTO/record; topic/group/retry hardcode trong code.
- `enable-auto-commit: true` + xử lý nặng → mất message khi crash giữa chừng.
- `spring.json.trusted.packages: "*"` (rủi ro deserialize).

## Done
- Producer publish after-commit, payload DTO; consumer idempotent + manual ack; topic/group/retry từ config; có DLT + backoff; không log dữ liệu nhạy cảm.

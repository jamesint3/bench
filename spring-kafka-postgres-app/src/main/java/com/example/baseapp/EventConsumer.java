package com.example.baseapp;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.tracing.Tracer;
import java.time.OffsetDateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class EventConsumer {

    private static final Logger LOG = LoggerFactory.getLogger(EventConsumer.class);

    private final ObjectMapper objectMapper;
    private final EventRecordRepository repository;
    private final Tracer tracer;

    public EventConsumer(ObjectMapper objectMapper, EventRecordRepository repository, Tracer tracer) {
        this.objectMapper = objectMapper;
        this.repository = repository;
        this.tracer = tracer;
    }

    @KafkaListener(topics = "${app.kafka.topic}", groupId = "${spring.kafka.consumer.group-id}")
    public void consume(String message) throws Exception {
        EventRequest event = objectMapper.readValue(message, EventRequest.class);
        repository.findByEventId(event.eventId()).orElseGet(() -> repository.save(
            new EventRecord(event.eventId(), event.payload(), OffsetDateTime.now())
        ));
        String traceId = tracer.currentSpan() == null ? "n/a" : tracer.currentSpan().context().traceId();
        LOG.info("Consumed and stored event {} traceId={}", event.eventId(), traceId);
    }
}

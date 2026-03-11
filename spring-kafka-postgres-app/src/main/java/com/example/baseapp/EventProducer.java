package com.example.baseapp;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.tracing.Span;
import io.micrometer.tracing.Tracer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class EventProducer {

    private static final Logger LOG = LoggerFactory.getLogger(EventProducer.class);

    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper;
    private final String topic;
    private final Tracer tracer;

    public EventProducer(
        KafkaTemplate<String, String> kafkaTemplate,
        ObjectMapper objectMapper,
        @Value("${app.kafka.topic}") String topic,
        Tracer tracer
    ) {
        this.kafkaTemplate = kafkaTemplate;
        this.objectMapper = objectMapper;
        this.topic = topic;
        this.tracer = tracer;
    }

    public void publish(EventRequest request) {
        try {
            String body = objectMapper.writeValueAsString(request);
            kafkaTemplate.send(topic, request.eventId(), body);
            Span currentSpan = tracer.currentSpan();
            String traceId = currentSpan == null ? "n/a" : currentSpan.context().traceId();
            LOG.info("Published event {} traceId={}", request.eventId(), traceId);
        } catch (JsonProcessingException e) {
            throw new IllegalArgumentException("Invalid event payload", e);
        }
    }
}

package com.example.baseapp;

import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/events")
public class EventController {

    private final EventProducer producer;
    private final EventRecordRepository repository;

    public EventController(EventProducer producer, EventRecordRepository repository) {
        this.producer = producer;
        this.repository = repository;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.ACCEPTED)
    public void publish(@Valid @RequestBody EventRequest request) {
        producer.publish(request);
    }

    @GetMapping
    public List<EventRecord> findAll() {
        return repository.findAll();
    }
}

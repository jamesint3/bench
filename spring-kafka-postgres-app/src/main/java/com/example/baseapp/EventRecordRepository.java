package com.example.baseapp;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EventRecordRepository extends JpaRepository<EventRecord, Long> {
    Optional<EventRecord> findByEventId(String eventId);
}

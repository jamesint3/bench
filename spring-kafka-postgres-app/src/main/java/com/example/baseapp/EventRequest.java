package com.example.baseapp;

import jakarta.validation.constraints.NotBlank;

public record EventRequest(@NotBlank String eventId, @NotBlank String payload) {
}

package com.codemaster.ai.controller;

import com.codemaster.ai.dto.ApiResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/health")
public class HealthController {

    @GetMapping
    public ResponseEntity<ApiResponse<Map<String, Object>>> health() {
        Map<String, Object> healthData = new HashMap<>();
        healthData.put("status", "UP");
        healthData.put("service", "Spring AI API");
        healthData.put("timestamp", LocalDateTime.now());
        healthData.put("version", "1.0.0");

        return ResponseEntity.ok(ApiResponse.success(healthData));
    }

    @GetMapping("/ready")
    public ResponseEntity<ApiResponse<Map<String, String>>> ready() {
        Map<String, String> readyData = new HashMap<>();
        readyData.put("status", "READY");

        return ResponseEntity.ok(ApiResponse.success(readyData));
    }

    @GetMapping("/live")
    public ResponseEntity<ApiResponse<Map<String, String>>> live() {
        Map<String, String> liveData = new HashMap<>();
        liveData.put("status", "LIVE");

        return ResponseEntity.ok(ApiResponse.success(liveData));
    }
}

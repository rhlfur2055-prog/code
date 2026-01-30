package com.example.msa.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@Tag(name = "Health", description = "헬스체크 API")
@RestController
@RequestMapping("/api/health")
public class HealthController {

    @Operation(summary = "서버 상태 확인", description = "서버가 정상 동작하는지 확인합니다")
    @GetMapping
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "UP");
        response.put("service", "msa-user-api");
        response.put("timestamp", LocalDateTime.now());
        return ResponseEntity.ok(response);
    }

    @Operation(summary = "상세 상태 확인", description = "서버의 상세 상태를 확인합니다")
    @GetMapping("/detail")
    public ResponseEntity<Map<String, Object>> healthDetail() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "UP");
        response.put("service", "msa-user-api");
        response.put("version", "1.0.0");
        response.put("timestamp", LocalDateTime.now());

        Map<String, Object> system = new HashMap<>();
        system.put("javaVersion", System.getProperty("java.version"));
        system.put("availableProcessors", Runtime.getRuntime().availableProcessors());
        system.put("freeMemory", Runtime.getRuntime().freeMemory() / 1024 / 1024 + " MB");
        system.put("totalMemory", Runtime.getRuntime().totalMemory() / 1024 / 1024 + " MB");

        response.put("system", system);
        return ResponseEntity.ok(response);
    }
}

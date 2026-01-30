package com.codemaster.ai.controller;

import com.codemaster.ai.dto.DetectionResponse;
import com.codemaster.ai.dto.TranscriptionResponse;
import com.codemaster.ai.service.AiService;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import reactor.core.publisher.Mono;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "*")
public class AiController {

    private final AiService aiService;

    public AiController(AiService aiService) {
        this.aiService = aiService;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "healthy"));
    }

    @PostMapping(value = "/detect", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Mono<DetectionResponse> detectObjects(@RequestParam("file") MultipartFile file) {
        return aiService.detectObjects(file);
    }

    @PostMapping(value = "/transcribe", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Mono<TranscriptionResponse> transcribe(@RequestParam("file") MultipartFile file) {
        return aiService.transcribe(file);
    }

    @PostMapping(value = "/remove-background", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Mono<Map<String, Object>> removeBackground(@RequestParam("file") MultipartFile file) {
        return aiService.removeBackground(file);
    }

    @PostMapping(value = "/caption", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Mono<Map<String, Object>> imageCaption(@RequestParam("file") MultipartFile file) {
        return aiService.imageCaption(file);
    }
}

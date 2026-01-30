package com.codemaster.ai.service;

import com.codemaster.ai.dto.DetectionResponse;
import com.codemaster.ai.dto.LicensePlateResponse;
import com.codemaster.ai.dto.TranscriptionResponse;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Mono;
import reactor.netty.http.client.HttpClient;

import java.io.IOException;
import java.time.Duration;
import java.util.Map;
import java.util.UUID;

/**
 * K-MaaS AI 서비스
 * Spring Boot ↔ FastAPI(Python) 연동
 *
 * 주요 기능:
 * - 번호판 인식 (YOLO + OCR)
 * - 객체 탐지 (YOLO)
 * - 음성 인식 (Whisper)
 * - 배경 제거
 */
@Service
public class AiService {

    private static final Logger log = LoggerFactory.getLogger(AiService.class);

    private final WebClient webClient;

    public AiService(@Value("${ai.python.server.url:http://localhost:8000}") String pythonServerUrl,
                     @Value("${ai.timeout.connect:5000}") int connectTimeout,
                     @Value("${ai.timeout.read:30000}") int readTimeout) {

        // HttpClient 타임아웃 설정
        HttpClient httpClient = HttpClient.create()
                .responseTimeout(Duration.ofMillis(readTimeout));

        this.webClient = WebClient.builder()
                .baseUrl(pythonServerUrl)
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .defaultHeader("X-Request-Source", "spring-boot")
                .build();

        log.info("AI Service initialized - URL: {}, ConnectTimeout: {}ms, ReadTimeout: {}ms",
                pythonServerUrl, connectTimeout, readTimeout);
    }

    /**
     * 🚗 K-MaaS 번호판 인식 API
     * CircuitBreaker + Retry 패턴 적용
     */
    @CircuitBreaker(name = "aiServer", fallbackMethod = "licensePlateFallback")
    @Retry(name = "aiServer")
    public Mono<LicensePlateResponse> detectLicensePlate(MultipartFile file) {
        String requestId = UUID.randomUUID().toString();
        log.info("[{}] 번호판 인식 요청 시작 - 파일: {}", requestId, file.getOriginalFilename());

        return callPythonApi("/api/v1/license-plate/detect", file, LicensePlateResponse.class, requestId)
                .doOnSuccess(response ->
                    log.info("[{}] 번호판 인식 완료 - 결과: {}", requestId, response.getPlateNumber()))
                .doOnError(e ->
                    log.error("[{}] 번호판 인식 실패: {}", requestId, e.getMessage()));
    }

    /**
     * 번호판 인식 Fallback (CircuitBreaker 발동 시)
     */
    public Mono<LicensePlateResponse> licensePlateFallback(MultipartFile file, Throwable t) {
        log.warn("CircuitBreaker 발동 - Fallback 응답 반환. 원인: {}", t.getMessage());
        LicensePlateResponse response = new LicensePlateResponse();
        response.setSuccess(false);
        response.setErrorMessage("AI 서버 일시적 장애. 잠시 후 다시 시도해주세요.");
        return Mono.just(response);
    }

    /**
     * 객체 탐지 API (YOLO)
     */
    @CircuitBreaker(name = "aiServer", fallbackMethod = "detectionFallback")
    public Mono<DetectionResponse> detectObjects(MultipartFile file) {
        String requestId = UUID.randomUUID().toString();
        return callPythonApi("/detect", file, DetectionResponse.class, requestId);
    }

    public Mono<DetectionResponse> detectionFallback(MultipartFile file, Throwable t) {
        log.warn("Detection Fallback: {}", t.getMessage());
        return Mono.just(new DetectionResponse(false, null, 0));
    }

    /**
     * 음성 인식 API (Whisper)
     */
    @CircuitBreaker(name = "aiServer", fallbackMethod = "transcriptionFallback")
    public Mono<TranscriptionResponse> transcribe(MultipartFile file) {
        String requestId = UUID.randomUUID().toString();
        return callPythonApi("/transcribe", file, TranscriptionResponse.class, requestId);
    }

    public Mono<TranscriptionResponse> transcriptionFallback(MultipartFile file, Throwable t) {
        log.warn("Transcription Fallback: {}", t.getMessage());
        return Mono.just(new TranscriptionResponse(false, null, null));
    }

    /**
     * 배경 제거 API
     */
    @SuppressWarnings("unchecked")
    public Mono<Map<String, Object>> removeBackground(MultipartFile file) {
        String requestId = UUID.randomUUID().toString();
        return callPythonApi("/remove-background", file, Map.class, requestId)
                .map(result -> (Map<String, Object>) result);
    }

    /**
     * 이미지 캡션 API
     */
    @SuppressWarnings("unchecked")
    public Mono<Map<String, Object>> imageCaption(MultipartFile file) {
        String requestId = UUID.randomUUID().toString();
        return callPythonApi("/caption", file, Map.class, requestId)
                .map(result -> (Map<String, Object>) result);
    }

    /**
     * Python AI 서버 호출 공통 메서드
     * - Multipart 파일 전송
     * - Request ID 기반 추적
     * - 에러 핸들링
     */
    private <T> Mono<T> callPythonApi(String endpoint, MultipartFile file,
                                       Class<T> responseType, String requestId) {
        try {
            MultipartBodyBuilder builder = new MultipartBodyBuilder();
            builder.part("file", new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            });

            long startTime = System.currentTimeMillis();

            return webClient.post()
                    .uri(endpoint)
                    .header("X-Request-ID", requestId)
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(BodyInserters.fromMultipartData(builder.build()))
                    .retrieve()
                    .onStatus(status -> status.is4xxClientError(),
                            response -> Mono.error(new RuntimeException(
                                    "클라이언트 에러: " + response.statusCode())))
                    .onStatus(status -> status.is5xxServerError(),
                            response -> Mono.error(new RuntimeException(
                                    "AI 서버 에러: " + response.statusCode())))
                    .bodyToMono(responseType)
                    .doOnSuccess(response -> {
                        long elapsed = System.currentTimeMillis() - startTime;
                        log.info("[{}] API 호출 완료 - endpoint: {}, 소요시간: {}ms",
                                requestId, endpoint, elapsed);
                    })
                    .doOnError(WebClientResponseException.class, e ->
                            log.error("[{}] API 호출 실패 - status: {}, body: {}",
                                    requestId, e.getStatusCode(), e.getResponseBodyAsString()));

        } catch (IOException e) {
            log.error("[{}] 파일 읽기 실패: {}", requestId, e.getMessage());
            return Mono.error(new RuntimeException("파일 처리 실패", e));
        }
    }
}

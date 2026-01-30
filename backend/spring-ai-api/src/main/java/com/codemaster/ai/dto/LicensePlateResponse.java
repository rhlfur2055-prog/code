package com.codemaster.ai.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * K-MaaS 번호판 인식 응답 DTO
 * Python FastAPI의 Pydantic 모델과 1:1 매핑
 */
public class LicensePlateResponse {

    /**
     * 요청 성공 여부
     */
    private boolean success;

    /**
     * 요청 ID (추적용)
     */
    @JsonProperty("request_id")
    private String requestId;

    /**
     * 인식된 번호판 번호 (예: "12가3456")
     */
    @JsonProperty("plate_number")
    private String plateNumber;

    /**
     * 인식 신뢰도 (0.0 ~ 1.0)
     */
    private Double confidence;

    /**
     * 번호판 영역 좌표
     */
    @JsonProperty("bounding_box")
    private BoundingBox boundingBox;

    /**
     * 차량 유형 (승용차, 트럭, 오토바이 등)
     */
    @JsonProperty("vehicle_type")
    private String vehicleType;

    /**
     * 처리 소요 시간 (밀리초)
     */
    @JsonProperty("processing_time_ms")
    private Long processingTimeMs;

    /**
     * 여러 번호판 탐지 시 목록
     */
    private List<PlateInfo> plates;

    /**
     * 에러 메시지 (실패 시)
     */
    @JsonProperty("error_message")
    private String errorMessage;

    public LicensePlateResponse() {
    }

    public LicensePlateResponse(boolean success, String requestId, String plateNumber,
                                 Double confidence, BoundingBox boundingBox, String vehicleType,
                                 Long processingTimeMs, List<PlateInfo> plates, String errorMessage) {
        this.success = success;
        this.requestId = requestId;
        this.plateNumber = plateNumber;
        this.confidence = confidence;
        this.boundingBox = boundingBox;
        this.vehicleType = vehicleType;
        this.processingTimeMs = processingTimeMs;
        this.plates = plates;
        this.errorMessage = errorMessage;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getPlateNumber() {
        return plateNumber;
    }

    public void setPlateNumber(String plateNumber) {
        this.plateNumber = plateNumber;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public BoundingBox getBoundingBox() {
        return boundingBox;
    }

    public void setBoundingBox(BoundingBox boundingBox) {
        this.boundingBox = boundingBox;
    }

    public String getVehicleType() {
        return vehicleType;
    }

    public void setVehicleType(String vehicleType) {
        this.vehicleType = vehicleType;
    }

    public Long getProcessingTimeMs() {
        return processingTimeMs;
    }

    public void setProcessingTimeMs(Long processingTimeMs) {
        this.processingTimeMs = processingTimeMs;
    }

    public List<PlateInfo> getPlates() {
        return plates;
    }

    public void setPlates(List<PlateInfo> plates) {
        this.plates = plates;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    /**
     * 번호판 영역 좌표
     */
    public static class BoundingBox {
        private int x;
        private int y;
        private int width;
        private int height;

        public BoundingBox() {
        }

        public BoundingBox(int x, int y, int width, int height) {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
        }

        public int getX() {
            return x;
        }

        public void setX(int x) {
            this.x = x;
        }

        public int getY() {
            return y;
        }

        public void setY(int y) {
            this.y = y;
        }

        public int getWidth() {
            return width;
        }

        public void setWidth(int width) {
            this.width = width;
        }

        public int getHeight() {
            return height;
        }

        public void setHeight(int height) {
            this.height = height;
        }
    }

    /**
     * 개별 번호판 정보 (다중 탐지 시)
     */
    public static class PlateInfo {
        @JsonProperty("plate_number")
        private String plateNumber;

        private Double confidence;

        @JsonProperty("bounding_box")
        private BoundingBox boundingBox;

        public PlateInfo() {
        }

        public PlateInfo(String plateNumber, Double confidence, BoundingBox boundingBox) {
            this.plateNumber = plateNumber;
            this.confidence = confidence;
            this.boundingBox = boundingBox;
        }

        public String getPlateNumber() {
            return plateNumber;
        }

        public void setPlateNumber(String plateNumber) {
            this.plateNumber = plateNumber;
        }

        public Double getConfidence() {
            return confidence;
        }

        public void setConfidence(Double confidence) {
            this.confidence = confidence;
        }

        public BoundingBox getBoundingBox() {
            return boundingBox;
        }

        public void setBoundingBox(BoundingBox boundingBox) {
            this.boundingBox = boundingBox;
        }
    }
}

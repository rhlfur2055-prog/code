package com.codemaster.ai.dto;

import java.util.List;

public class DetectionResponse {
    private boolean success;
    private List<Detection> detections;
    private int count;

    public DetectionResponse() {
    }

    public DetectionResponse(boolean success, List<Detection> detections, int count) {
        this.success = success;
        this.detections = detections;
        this.count = count;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public List<Detection> getDetections() {
        return detections;
    }

    public void setDetections(List<Detection> detections) {
        this.detections = detections;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }

    public static class Detection {
        private String className;
        private double confidence;
        private List<Double> bbox;

        public Detection() {
        }

        public Detection(String className, double confidence, List<Double> bbox) {
            this.className = className;
            this.confidence = confidence;
            this.bbox = bbox;
        }

        public String getClassName() {
            return className;
        }

        public void setClassName(String className) {
            this.className = className;
        }

        public double getConfidence() {
            return confidence;
        }

        public void setConfidence(double confidence) {
            this.confidence = confidence;
        }

        public List<Double> getBbox() {
            return bbox;
        }

        public void setBbox(List<Double> bbox) {
            this.bbox = bbox;
        }
    }
}

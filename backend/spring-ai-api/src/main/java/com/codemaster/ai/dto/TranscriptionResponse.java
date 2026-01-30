package com.codemaster.ai.dto;

public class TranscriptionResponse {
    private boolean success;
    private String text;
    private String language;

    public TranscriptionResponse() {
    }

    public TranscriptionResponse(boolean success, String text, String language) {
        this.success = success;
        this.text = text;
        this.language = language;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }
}

-- ================================
-- MSA Project - Database Initialization Script
-- ================================
-- This script runs when the MySQL container starts for the first time
-- File: 01_init.sql

-- Set character encoding
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Create database if not exists (usually handled by MYSQL_DATABASE env var)
-- CREATE DATABASE IF NOT EXISTS msa_database;
-- USE msa_database;

-- ================================
-- User Management Table
-- ================================
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('USER', 'ADMIN') DEFAULT 'USER',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================
-- AI Request Log Table
-- ================================
CREATE TABLE IF NOT EXISTS ai_request_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    request_id VARCHAR(36) NOT NULL UNIQUE,
    user_id BIGINT,
    request_type ENUM('LICENSE_PLATE', 'OBJECT_DETECTION', 'TRANSCRIPTION', 'BACKGROUND_REMOVAL', 'CAPTION') NOT NULL,
    status ENUM('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED') DEFAULT 'PENDING',
    request_payload JSON,
    response_payload JSON,
    processing_time_ms INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_request_id (request_id),
    INDEX idx_user_id (user_id),
    INDEX idx_request_type (request_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================
-- License Plate Detection Results
-- ================================
CREATE TABLE IF NOT EXISTS license_plate_results (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    request_id VARCHAR(36) NOT NULL,
    plate_number VARCHAR(20),
    confidence DECIMAL(5,4),
    bounding_box_x INT,
    bounding_box_y INT,
    bounding_box_width INT,
    bounding_box_height INT,
    vehicle_type VARCHAR(50),
    image_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES ai_request_logs(request_id) ON DELETE CASCADE,
    INDEX idx_plate_number (plate_number),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================
-- Study Progress Table (for frontend)
-- ================================
CREATE TABLE IF NOT EXISTS study_progress (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    category VARCHAR(100) NOT NULL,
    slug VARCHAR(200) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_progress (user_id, category, slug),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_category (user_id, category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================
-- Bookmarks Table
-- ================================
CREATE TABLE IF NOT EXISTS bookmarks (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    category VARCHAR(100) NOT NULL,
    slug VARCHAR(200) NOT NULL,
    title VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_bookmark (user_id, category, slug),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================
-- API Usage Statistics
-- ================================
CREATE TABLE IF NOT EXISTS api_statistics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    endpoint VARCHAR(200) NOT NULL,
    request_count INT DEFAULT 0,
    avg_response_time_ms DECIMAL(10,2),
    error_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_stat (date, endpoint),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================
-- Insert Default Admin User
-- ================================
-- Password: admin123 (bcrypt hash)
INSERT INTO users (username, email, password_hash, role, is_active)
VALUES ('admin', 'admin@codemaster.local', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MqA1VJzJZNx9W0g9Q2lBgRnKqBCfCqe', 'ADMIN', TRUE)
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- ================================
-- Grant Permissions (if needed)
-- ================================
-- GRANT ALL PRIVILEGES ON msa_database.* TO 'root'@'%';
-- FLUSH PRIVILEGES;

SELECT 'Database initialization completed successfully!' AS status;

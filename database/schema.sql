-- PDF Classifier Database Schema
-- Version: 1.0
-- Created: 2025-10-08

CREATE DATABASE IF NOT EXISTS pdf_classifier 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE pdf_classifier;

-- Table: document_types
CREATE TABLE IF NOT EXISTS document_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: documents
CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    document_type_id INT,
    predicted_type_id INT,
    confidence_score DECIMAL(5,4),
    status ENUM('pending', 'analyzing', 'classified', 'validated', 'error') DEFAULT 'pending',
    is_validated BOOLEAN DEFAULT FALSE,
    validated_by VARCHAR(100),
    validated_at TIMESTAMP NULL,
    
    -- Extracted information
    extracted_text TEXT,
    cuit VARCHAR(20),
    provider VARCHAR(200),
    document_date DATE,
    document_number VARCHAR(100),
    total_amount DECIMAL(15,2),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    processed_at TIMESTAMP NULL,
    error_message TEXT,
    
    FOREIGN KEY (document_type_id) REFERENCES document_types(id),
    FOREIGN KEY (predicted_type_id) REFERENCES document_types(id),
    
    INDEX idx_filename (filename),
    INDEX idx_document_type (document_type_id),
    INDEX idx_status (status),
    INDEX idx_document_date (document_date),
    INDEX idx_cuit (cuit),
    INDEX idx_provider (provider),
    INDEX idx_created_at (created_at),
    INDEX idx_is_validated (is_validated),
    FULLTEXT INDEX idx_extracted_text (extracted_text)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: processing_logs
CREATE TABLE IF NOT EXISTS processing_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    user VARCHAR(100),
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    INDEX idx_document_id (document_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: ml_training_data
CREATE TABLE IF NOT EXISTS ml_training_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    text_features TEXT,
    correct_type_id INT,
    used_for_training BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (correct_type_id) REFERENCES document_types(id),
    INDEX idx_used_for_training (used_for_training)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default document types
INSERT INTO document_types (name, description) VALUES
('Factura', 'Factura de venta o compra'),
('Nota de Debito', 'Nota de débito'),
('Nota de Credito', 'Nota de crédito'),
('Remito', 'Remito de mercadería'),
('Desconocido', 'Tipo de documento no identificado');

-- Create view for document statistics
CREATE OR REPLACE VIEW document_statistics AS
SELECT 
    dt.name AS document_type,
    COUNT(d.id) AS total_documents,
    SUM(CASE WHEN d.is_validated THEN 1 ELSE 0 END) AS validated_documents,
    AVG(d.confidence_score) AS avg_confidence,
    COUNT(CASE WHEN d.status = 'pending' THEN 1 END) AS pending_count,
    COUNT(CASE WHEN d.status = 'error' THEN 1 END) AS error_count
FROM document_types dt
LEFT JOIN documents d ON dt.id = d.document_type_id
GROUP BY dt.id, dt.name;

-- Create view for recent documents
CREATE OR REPLACE VIEW recent_documents AS
SELECT 
    d.id,
    d.original_filename,
    d.filename,
    dt.name AS document_type,
    d.status,
    d.confidence_score,
    d.is_validated,
    d.document_date,
    d.provider,
    d.cuit,
    d.created_at
FROM documents d
LEFT JOIN document_types dt ON d.document_type_id = dt.id
ORDER BY d.created_at DESC
LIMIT 100;

-- =============================================
-- 📁 Archivo: /database/bank_marketing_schema_postgres.sql
-- =============================================

-- Crear base de datos (ejecutar con un superusuario, fuera del contexto de la BD)
-- Nota: En PostgreSQL no existe "IF NOT EXISTS" dentro del bloque CREATE DATABASE
-- por lo que puedes ejecutarlo de manera segura; si ya existe, lanzará una advertencia.
CREATE DATABASE bank_marketing;

-- Cambiar contexto a la base de datos
\c bank_marketing;

-- =============================================
-- Tabla de clientes (dataset)
-- =============================================
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    age INT NOT NULL,
    job VARCHAR(50),
    marital VARCHAR(20),
    education VARCHAR(50),
    "default" VARCHAR(10),
    balance DOUBLE PRECISION,
    housing VARCHAR(10),
    loan VARCHAR(10),
    contact VARCHAR(20),
    day INT,
    month VARCHAR(10),
    duration INT,
    campaign INT,
    pdays INT,
    previous INT,
    poutcome VARCHAR(20),
    deposit VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- Tabla de predicciones
-- =============================================
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(id) ON DELETE SET NULL,
    age INT,
    job VARCHAR(50),
    marital VARCHAR(20),
    education VARCHAR(50),
    balance DOUBLE PRECISION,
    result INT,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- Tabla opcional: métricas de rendimiento del modelo
-- =============================================
CREATE TABLE IF NOT EXISTS evaluation_metrics (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50),
    accuracy DOUBLE PRECISION,
    precision DOUBLE PRECISION,
    recall DOUBLE PRECISION,
    f1 DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

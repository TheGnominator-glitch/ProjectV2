SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS flask_db_unilibre
    DEFAULT CHARACTER SET utf8mb4;
USE flask_db_unilibre;

CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    carrera VARCHAR(150) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo (solo se insertan si la tabla está vacía, así se puede
-- ejecutar este script varias veces sin duplicar registros)
INSERT INTO estudiantes (nombre, apellido, edad, carrera)
SELECT * FROM (
    SELECT 'Juan' AS nombre, 'Pérez' AS apellido, 20 AS edad, 'Ingeniería de Sistemas' AS carrera
    UNION ALL SELECT 'María', 'González', 22, 'Ingeniería Industrial'
    UNION ALL SELECT 'Carlos', 'Rodríguez', 21, 'Ingeniería Electrónica'
) AS ejemplos
WHERE NOT EXISTS (SELECT 1 FROM estudiantes);

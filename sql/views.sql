-- ============================================================
-- Views do projeto Pipeline de Dados com IoT e Docker
-- ============================================================


-- View 1: Temperatura média por ambiente
-- Compara as temperaturas registradas em ambientes internos
-- (In) e externos (Out).
CREATE OR REPLACE VIEW avg_temp_por_ambiente AS
SELECT
    ambiente,
    ROUND(AVG(temp)::numeric, 2) AS avg_temp
FROM temperature_readings
GROUP BY ambiente;


-- View 2: Quantidade de leituras por hora do dia
-- Permite analisar como as medições estão distribuídas
-- ao longo das 24 horas do dia.
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM noted_date)::integer AS hora,
    COUNT(*) AS contagem
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM noted_date)
ORDER BY hora;


-- View 3: Temperaturas mínima, média e máxima por dia
-- Permite acompanhar a variação diária das temperaturas.
CREATE OR REPLACE VIEW temp_por_dia AS
SELECT
    DATE(noted_date) AS data,
    MIN(temp) AS temp_min,
    ROUND(AVG(temp)::numeric, 2) AS temp_media,
    MAX(temp) AS temp_max
FROM temperature_readings
GROUP BY DATE(noted_date)
ORDER BY data;

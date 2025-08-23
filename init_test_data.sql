-- ============================================
-- DATOS DE PRUEBA PARA TESTING - AUDITE
-- ============================================

-- Este archivo se ejecuta automáticamente al crear la BD

-- Limpiar datos existentes (solo en testing)
TRUNCATE TABLE IF EXISTS autodiagnostico_respuestas CASCADE;
TRUNCATE TABLE IF EXISTS autodiagnostico_opciones CASCADE;
TRUNCATE TABLE IF EXISTS autodiagnostico_preguntas CASCADE;
TRUNCATE TABLE IF EXISTS respuestas_formulario CASCADE;
TRUNCATE TABLE IF EXISTS preguntas_formulario CASCADE;
TRUNCATE TABLE IF EXISTS formularios_industria CASCADE;
TRUNCATE TABLE IF EXISTS categorias_industria CASCADE;

-- Reset de secuencias
SELECT setval(pg_get_serial_sequence('categorias_industria', 'id'), 1, false);
SELECT setval(pg_get_serial_sequence('formularios_industria', 'id'), 1, false);
SELECT setval(pg_get_serial_sequence('preguntas_formulario', 'id'), 1, false);
SELECT setval(pg_get_serial_sequence('autodiagnostico_preguntas', 'id'), 1, false);
SELECT setval(pg_get_serial_sequence('autodiagnostico_opciones', 'id'), 1, false);

-- Mensaje de inicio
DO $$
BEGIN
    RAISE NOTICE '🚀 Inicializando datos de prueba para AUDITE Testing...';
END
$$;

-- ===========================================
-- 1. CATEGORÍAS DE INDUSTRIA
-- ===========================================

INSERT INTO categorias_industria (nombre, descripcion, icono, color, activa, orden) VALUES
('Industrial', 'Sector manufacturero y de procesamiento industrial', '🏭', '#3b82f6', true, 1),
('Comercial', 'Sector comercio, retail y servicios', '🏢', '#10b981', true, 2),
('Agropecuario', 'Sector agrícola, ganadero y forestal', '🚜', '#f59e0b', true, 3),
('Servicios', 'Sector servicios profesionales y técnicos', '💼', '#8b5cf6', true, 4),
('Hospitalario', 'Sector salud y servicios médicos', '🏥', '#ef4444', true, 5);

-- ===========================================
-- 2. FORMULARIOS POR INDUSTRIA  
-- ===========================================

INSERT INTO formularios_industria (categoria_id, nombre, descripcion, activo, orden, tiempo_estimado) VALUES
-- Industrial
(1, 'Diagnóstico Industrial Básico', 'Evaluación energética para plantas industriales y manufactureras', true, 1, 15),
(1, 'Diagnóstico Industrial Avanzado', 'Análisis profundo para grandes complejos industriales', true, 2, 30),

-- Comercial  
(2, 'Diagnóstico Comercial Estándar', 'Evaluación para locales comerciales y oficinas', true, 1, 12),
(2, 'Diagnóstico Retail Especializado', 'Análisis específico para centros comerciales y retail', true, 2, 20),

-- Agropecuario
(3, 'Diagnóstico Agropecuario Básico', 'Evaluación para pequeñas y medianas explotaciones', true, 1, 18),
(3, 'Diagnóstico Agroindustrial', 'Análisis para plantas de procesamiento agrícola', true, 2, 25);

-- ===========================================
-- 3. PREGUNTAS DE AUTODIAGNÓSTICO BÁSICO
-- ===========================================

INSERT INTO autodiagnostico_preguntas (numero_orden, pregunta, tipo_respuesta, es_obligatoria, es_activa, ayuda_texto) VALUES
(1, '¿En qué sector opera principalmente su empresa?', 'radio', true, true, 'Seleccione el sector que mejor describe su actividad principal'),
(2, '¿Cuál es el tamaño aproximado de sus instalaciones?', 'radio', true, true, 'Considere el área total construida de sus instalaciones'),
(3, '¿Cuántos empleados tiene su empresa aproximadamente?', 'radio', true, true, 'Incluya empleados de tiempo completo y medio tiempo'),
(4, '¿Cuál es su consumo eléctrico mensual aproximado?', 'radio', true, true, 'Revise su factura eléctrica más reciente'),
(5, '¿Ha realizado alguna auditoría energética anteriormente?', 'radio', true, true, 'Una auditoría energética es un análisis profesional del consumo de energía');

-- ===========================================
-- 4. OPCIONES DE AUTODIAGNÓSTICO
-- ===========================================

-- Pregunta 1: Sector
INSERT INTO autodiagnostico_opciones (pregunta_id, texto_opcion, valor, orden, es_activa, tiene_sugerencia, sugerencia) VALUES
(1, 'Industrial/Manufacturero', 'industrial', 1, true, true, 'El sector industrial típicamente consume mucha energía en procesos. Considere implementar sistemas de gestión energética.'),
(1, 'Comercial/Servicios', 'comercial', 2, true, true, 'En el sector comercial, la iluminación y climatización son los principales consumos. LED y sistemas eficientes son prioritarios.'),
(1, 'Agropecuario', 'agropecuario', 3, true, true, 'El sector agropecuario puede beneficiarse mucho de energías renovables, especialmente solar para riego y procesamiento.'),
(1, 'Servicios Profesionales', 'servicios', 4, true, true, 'Las oficinas pueden lograr grandes ahorros con equipamiento eficiente y automatización de sistemas.'),
(1, 'Otro', 'otro', 5, true, false, null);

-- Pregunta 2: Tamaño instalaciones  
INSERT INTO autodiagnostico_opciones (pregunta_id, texto_opcion, valor, orden, es_activa, tiene_sugerencia, sugerencia) VALUES
(2, 'Menos de 100 m²', 'pequena', 1, true, true, 'Para espacios pequeños, enfóquese en iluminación LED y equipos eficientes.'),
(2, '100 - 500 m²', 'mediana', 2, true, true, 'Espacios medianos pueden beneficiarse de sistemas de control automático y zonificación.'),
(2, '500 - 2000 m²', 'grande', 3, true, true, 'Instalaciones grandes requieren sistemas de gestión energética y monitoreo continuo.'),
(2, 'Más de 2000 m²', 'muy_grande', 4, true, true, 'Instalaciones muy grandes necesitan auditorías profesionales y sistemas avanzados de control.');

-- Pregunta 3: Empleados
INSERT INTO autodiagnostico_opciones (pregunta_id, texto_opcion, valor, orden, es_activa) VALUES  
(3, '1-5 empleados', '1-5', 1, true),
(3, '6-20 empleados', '6-20', 2, true),
(3, '21-50 empleados', '21-50', 3, true),
(3, '51-100 empleados', '51-100', 4, true),
(3, 'Más de 100 empleados', '100+', 5, true);

-- Pregunta 4: Consumo eléctrico
INSERT INTO autodiagnostico_opciones (pregunta_id, texto_opcion, valor, orden, es_activa, tiene_sugerencia, sugerencia) VALUES
(4, 'Menos de $50.000 mensuales', 'bajo', 1, true, true, 'Con consumo bajo, enfóquese en cambios de bajo costo como iluminación LED.'),
(4, '$50.000 - $200.000 mensuales', 'medio', 2, true, true, 'Consumo medio permite inversiones en equipamiento más eficiente con retorno rápido.'),
(4, '$200.000 - $500.000 mensuales', 'alto', 3, true, true, 'Consumo alto justifica auditoría profesional e inversiones en sistemas de gestión.'),
(4, 'Más de $500.000 mensuales', 'muy_alto', 4, true, true, 'Consumo muy alto requiere análisis profesional inmediato y sistema de monitoreo continuo.'),
(4, 'No lo sé', 'no_se', 5, true, true, 'Es importante conocer su facturación eléctrica. Revise sus facturas de los últimos 12 meses.');

-- Pregunta 5: Auditoría previa
INSERT INTO autodiagnostico_opciones (pregunta_id, texto_opcion, valor, orden, es_activa, tiene_sugerencia, sugerencia) VALUES
(5, 'Sí, en los últimos 2 años', 'si_reciente', 1, true, true, 'Excelente. Revise si se implementaron las recomendaciones y mida los resultados.'),
(5, 'Sí, hace más de 2 años', 'si_antigua', 2, true, true, 'Es tiempo de actualizar su auditoría. La tecnología y precios han cambiado mucho.'),
(5, 'No, nunca', 'nunca', 3, true, true, 'Una auditoría energética puede identificar ahorros del 10-30% en su factura eléctrica.'),
(5, 'No estoy seguro', 'no_seguro', 4, true, true, 'Consulte con su equipo técnico si se han realizado evaluaciones energéticas anteriores.');

-- ===========================================
-- 5. EJEMPLO DE PREGUNTAS PARA FORMULARIO INDUSTRIAL
-- ===========================================

INSERT INTO preguntas_formulario (formulario_id, texto, subtitulo, tipo, opciones, orden, requerida, activa) VALUES
(1, '¿Cuáles son sus principales procesos industriales?', 'Seleccione todos los que apliquen a su operación', 'checkbox', 
'[
    {"value": "soldadura", "label": "Soldadura"},
    {"value": "corte", "label": "Corte y mecanizado"},
    {"value": "fundicion", "label": "Fundición"},
    {"value": "pintura", "label": "Pintura y recubrimientos"},
    {"value": "ensamble", "label": "Ensamble"},
    {"value": "control_calidad", "label": "Control de calidad"}
]'::json, 1, true, true),

(1, '¿Qué tipo de sistema de climatización utiliza?', null, 'radio',
'[
    {"value": "central", "label": "Sistema central"},
    {"value": "splits", "label": "Equipos split individuales"},
    {"value": "evaporativo", "label": "Enfriamiento evaporativo"},
    {"value": "ninguno", "label": "Sin climatización"}
]'::json, 2, true, true),

(1, '¿Cuál es su horario de operación principal?', null, 'radio',
'[
    {"value": "8x5", "label": "8 horas, 5 días a la semana"},
    {"value": "12x5", "label": "12 horas, 5 días a la semana"},  
    {"value": "24x5", "label": "24 horas, 5 días a la semana"},
    {"value": "24x7", "label": "24 horas, 7 días a la semana"}
]'::json, 3, true, true);

-- Mensaje de finalización
DO $$
BEGIN
    RAISE NOTICE '✅ Datos de prueba inicializados correctamente';
    RAISE NOTICE '📊 Categorías: % | Formularios: % | Preguntas Autodiag: %', 
        (SELECT COUNT(*) FROM categorias_industria),
        (SELECT COUNT(*) FROM formularios_industria), 
        (SELECT COUNT(*) FROM autodiagnostico_preguntas);
END
$$;
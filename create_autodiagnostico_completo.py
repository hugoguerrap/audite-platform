#!/usr/bin/env python3
"""
Crear autodiagnóstico completo para el home (formulario fijo)
"""

import requests
import json

API_BASE = "http://localhost:18000"
ADMIN_CREDENTIALS = {"username": "admin_audite", "password": "AuditE2024!SecureAdmin#2024"}

def get_admin_token():
    response = requests.post(f"{API_BASE}/admin/auth/login", json=ADMIN_CREDENTIALS)
    return response.json()['access_token']

def api_call(method, endpoint, data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    url = f"{API_BASE}{endpoint}"
    
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=data, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=data, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"❌ Error en {endpoint}: {response.status_code} - {response.text}")
        return None

def main():
    print("🏠 CREANDO AUTODIAGNÓSTICO COMPLETO PARA HOME")
    print("=============================================")
    
    token = get_admin_token()
    
    # 1. Limpiar preguntas existentes del autodiagnóstico
    print("🧹 Limpiando autodiagnóstico existente...")
    
    preguntas_existentes = api_call("GET", "/autodiagnostico/admin/preguntas", token=token)
    if preguntas_existentes:
        for pregunta in preguntas_existentes:
            api_call("DELETE", f"/autodiagnostico/admin/preguntas/{pregunta['id']}", token=token)
        print(f"✅ {len(preguntas_existentes)} preguntas anteriores eliminadas")
    
    # 2. Crear autodiagnóstico completo y profesional
    print("🎨 Creando autodiagnóstico completo...")
    
    preguntas_autodiagnostico = [
        # === PREGUNTA 1: SECTOR ===
        {
            "numero_orden": 1,
            "pregunta": "¿En qué sector opera principalmente su empresa?",
            "tipo_respuesta": "radio",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Seleccione el sector que mejor describe su actividad económica principal"
        },
        
        # === PREGUNTA 2: TAMAÑO EMPRESA ===
        {
            "numero_orden": 2,
            "pregunta": "¿Cuál es el tamaño aproximado de su empresa?",
            "tipo_respuesta": "radio",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Considere tanto el número de empleados como el área de sus instalaciones"
        },
        
        # === PREGUNTA 3: CONSUMO ENERGÉTICO ===
        {
            "numero_orden": 3,
            "pregunta": "¿Cuál es su facturación energética mensual aproximada?",
            "tipo_respuesta": "radio",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Revise su factura eléctrica más reciente para una estimación más precisa"
        },
        
        # === PREGUNTA 4: AUDITORÍA PREVIA ===
        {
            "numero_orden": 4,
            "pregunta": "¿Ha realizado alguna auditoría energética anteriormente?",
            "tipo_respuesta": "radio",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Una auditoría energética es un análisis profesional del consumo de energía de su empresa"
        },
        
        # === PREGUNTA 5: PRINCIPALES DESAFÍOS ===
        {
            "numero_orden": 5,
            "pregunta": "¿Cuáles son sus principales desafíos energéticos actuales?",
            "tipo_respuesta": "checkbox",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Seleccione todos los que considere relevantes para su empresa"
        },
        
        # === PREGUNTA 6: OBJETIVOS ===
        {
            "numero_orden": 6,
            "pregunta": "¿Cuáles son sus principales objetivos con una consultoría energética?",
            "tipo_respuesta": "checkbox",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Seleccione hasta 3 objetivos prioritarios"
        },
        
        # === PREGUNTA 7: PRESUPUESTO ===
        {
            "numero_orden": 7,
            "pregunta": "¿Cuál es el presupuesto aproximado que destinaría a mejoras energéticas?",
            "tipo_respuesta": "radio",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Esta información nos ayuda a generar recomendaciones acordes a su realidad financiera"
        },
        
        # === PREGUNTA 8: TIMEFRAME ===
        {
            "numero_orden": 8,
            "pregunta": "¿En qué plazo esperaría implementar mejoras energéticas?",
            "tipo_respuesta": "radio",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Considere tanto la urgencia como la disponibilidad de recursos"
        },
        
        # === PREGUNTA 9: INFORMACIÓN DE CONTACTO ===
        {
            "numero_orden": 9,
            "pregunta": "¿Cómo prefiere que lo contactemos para presentar los resultados?",
            "tipo_respuesta": "radio",
            "es_obligatoria": False,
            "es_activa": True,
            "ayuda_texto": "Opcional: para enviarle un reporte personalizado de recomendaciones"
        },
        
        # === PREGUNTA 10: COMENTARIOS ADICIONALES ===
        {
            "numero_orden": 10,
            "pregunta": "¿Hay alguna información adicional que considere importante mencionar?",
            "tipo_respuesta": "text",
            "es_obligatoria": False,
            "es_activa": True,
            "ayuda_texto": "Cualquier detalle específico sobre su situación energética actual"
        }
    ]
    
    # Crear las preguntas
    preguntas_creadas = []
    for pregunta_data in preguntas_autodiagnostico:
        pregunta = api_call("POST", "/autodiagnostico/admin/preguntas", pregunta_data, token)
        if pregunta:
            preguntas_creadas.append(pregunta)
            print(f"✅ Pregunta {pregunta['numero_orden']}: {pregunta['pregunta'][:50]}...")
    
    print(f"\n🎨 CREANDO OPCIONES PARA LAS PREGUNTAS...")
    
    # 3. Crear opciones para cada pregunta
    for pregunta in preguntas_creadas:
        crear_opciones_para_pregunta(pregunta, token)
    
    print(f"\n🎉 AUTODIAGNÓSTICO COMPLETO CREADO!")
    print(f"📊 {len(preguntas_creadas)} preguntas con opciones personalizadas")
    print(f"🌐 Disponible en: http://localhost:18080/diagnostico")

def crear_opciones_para_pregunta(pregunta, token):
    """Crear opciones específicas para cada pregunta"""
    
    pregunta_id = pregunta["id"]
    numero_orden = pregunta["numero_orden"]
    
    opciones_por_pregunta = {
        1: [  # Sector
            {"texto_opcion": "Industrial/Manufacturero", "valor": "industrial", "orden": 1, "tiene_sugerencia": True, "sugerencia": "El sector industrial puede lograr ahorros del 15-30% optimizando procesos y equipamiento."},
            {"texto_opcion": "Comercial/Retail", "valor": "comercial", "orden": 2, "tiene_sugerencia": True, "sugerencia": "En comercio, la iluminación LED y climatización eficiente son las mejores inversiones."},
            {"texto_opcion": "Servicios/Oficinas", "valor": "servicios", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Las oficinas pueden ahorrar significativamente con equipamiento eficiente y automatización."},
            {"texto_opcion": "Agropecuario", "valor": "agropecuario", "orden": 4, "tiene_sugerencia": True, "sugerencia": "El sector agropecuario tiene gran potencial con energías renovables y optimización de riego."},
            {"texto_opcion": "Hospitalario/Salud", "valor": "salud", "orden": 5, "tiene_sugerencia": True, "sugerencia": "Centros de salud requieren eficiencia sin comprometer la operación crítica."},
            {"texto_opcion": "Educacional", "valor": "educacion", "orden": 6, "tiene_sugerencia": True, "sugerencia": "Instituciones educativas pueden ser ejemplos de sustentabilidad energética."},
            {"texto_opcion": "Otro", "valor": "otro", "orden": 7, "es_especial": True}
        ],
        
        2: [  # Tamaño empresa
            {"texto_opcion": "Microempresa (1-10 empleados)", "valor": "micro", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Para microempresas recomendamos medidas de bajo costo y retorno rápido como LED y equipos eficientes."},
            {"texto_opcion": "Pequeña empresa (11-50 empleados)", "valor": "pequena", "orden": 2, "tiene_sugerencia": True, "sugerencia": "Pequeñas empresas pueden implementar mejoras graduales con financiamiento accesible."},
            {"texto_opcion": "Mediana empresa (51-200 empleados)", "valor": "mediana", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Medianas empresas pueden justificar inversiones en tecnología y sistemas de control automatizado."},
            {"texto_opcion": "Gran empresa (+200 empleados)", "valor": "grande", "orden": 4, "tiene_sugerencia": True, "sugerencia": "Grandes empresas deben considerar sistemas de gestión energética ISO 50001 y energías renovables."}
        ],
        
        3: [  # Facturación energética
            {"texto_opcion": "Menos de $100,000 mensuales", "valor": "muy_bajo", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Con consumo bajo, enfóquese en medidas de bajo costo: LED, equipos eficientes clase A."},
            {"texto_opcion": "$100,000 - $500,000 mensuales", "valor": "bajo", "orden": 2, "tiene_sugerencia": True, "sugerencia": "Su nivel de consumo permite inversiones en equipamiento eficiente con retorno de 1-3 años."},
            {"texto_opcion": "$500,000 - $1,500,000 mensuales", "valor": "medio", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Consumo medio-alto justifica auditoría profesional e inversiones en automatización."},
            {"texto_opcion": "$1,500,000 - $5,000,000 mensuales", "valor": "alto", "orden": 4, "tiene_sugerencia": True, "sugerencia": "Consumo alto requiere análisis profesional inmediato y sistema de monitoreo continuo."},
            {"texto_opcion": "Más de $5,000,000 mensuales", "valor": "muy_alto", "orden": 5, "tiene_sugerencia": True, "sugerencia": "Consumo muy alto justifica inversiones importantes en gestión energética y energías renovables."},
            {"texto_opcion": "No estoy seguro", "valor": "no_se", "orden": 6, "es_especial": True, "tiene_sugerencia": True, "sugerencia": "Es importante conocer su facturación energética. Revise facturas de los últimos 12 meses."}
        ],
        
        4: [  # Auditoría previa
            {"texto_opcion": "Sí, en los últimos 2 años", "valor": "si_reciente", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Excelente. Revise si implementó las recomendaciones y evalúe los resultados obtenidos."},
            {"texto_opcion": "Sí, hace más de 2 años", "valor": "si_antigua", "orden": 2, "tiene_sugerencia": True, "sugerencia": "Es tiempo de actualizar. La tecnología y costos han cambiado significativamente."},
            {"texto_opcion": "No, nunca hemos hecho una", "valor": "nunca", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Una primera auditoría puede identificar ahorros inmediatos del 10-30% en su factura."},
            {"texto_opcion": "No estoy seguro", "valor": "no_seguro", "orden": 4, "es_especial": True, "tiene_sugerencia": True, "sugerencia": "Consulte con su equipo técnico si se realizaron evaluaciones energéticas anteriores."}
        ],
        
        5: [  # Desafíos energéticos
            {"texto_opcion": "Facturas energéticas muy altas", "valor": "costos_altos", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Para reducir costos, identifique equipos de mayor consumo y optimice horarios de operación."},
            {"texto_opcion": "Equipos antiguos e ineficientes", "valor": "equipos_antiguos", "orden": 2, "tiene_sugerencia": True, "sugerencia": "La renovación gradual de equipos antiguos puede generar ahorros significativos con retorno rápido."},
            {"texto_opcion": "Falta de control y monitoreo", "valor": "sin_control", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Un sistema de monitoreo en tiempo real es clave para identificar oportunidades de ahorro."},
            {"texto_opcion": "Cortes o problemas de suministro", "valor": "problemas_suministro", "orden": 4, "tiene_sugerencia": True, "sugerencia": "Considere sistemas de respaldo y mejore la calidad de su instalación eléctrica."},
            {"texto_opcion": "Falta de conocimiento técnico", "valor": "falta_conocimiento", "orden": 5, "tiene_sugerencia": True, "sugerencia": "La capacitación técnica y asesoría especializada son inversiones que se pagan solas."},
            {"texto_opcion": "Presión por certificaciones ambientales", "valor": "certificaciones", "orden": 6, "tiene_sugerencia": True, "sugerencia": "Las certificaciones ISO 14001 y huella de carbono son cada vez más importantes para competitividad."}
        ],
        
        6: [  # Objetivos
            {"texto_opcion": "Reducir costos operativos", "valor": "reducir_costos", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Enfoque en medidas de retorno rápido: LED, equipos eficientes, optimización de procesos."},
            {"texto_opcion": "Mejorar competitividad", "valor": "competitividad", "orden": 2, "tiene_sugerencia": True, "sugerencia": "La eficiencia energética mejora márgenes y permite precios más competitivos."},
            {"texto_opcion": "Cumplir con regulaciones ambientales", "valor": "regulaciones", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Anticiparse a regulaciones futuras es una ventaja competitiva importante."},
            {"texto_opcion": "Implementar energías renovables", "valor": "renovables", "orden": 4, "tiene_sugerencia": True, "sugerencia": "Las energías renovables ofrecen ahorro a largo plazo y beneficios de imagen corporativa."},
            {"texto_opcion": "Obtener certificaciones verdes", "valor": "certificaciones_verdes", "orden": 5, "tiene_sugerencia": True, "sugerencia": "Certificaciones como LEED, ISO 50001 abren nuevos mercados y oportunidades."},
            {"texto_opcion": "Mejorar imagen corporativa", "valor": "imagen", "orden": 6, "tiene_sugerencia": True, "sugerencia": "La sostenibilidad energética es un diferenciador importante ante clientes y stakeholders."}
        ],
        
        7: [  # Presupuesto
            {"texto_opcion": "Menos de $1,000,000", "valor": "bajo", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Con presupuesto limitado, priorice medidas de alto impacto y bajo costo como iluminación LED."},
            {"texto_opcion": "$1,000,000 - $5,000,000", "valor": "medio", "orden": 2, "tiene_sugerencia": True, "sugerencia": "Presupuesto medio permite combinar medidas de bajo costo con algunas inversiones en equipamiento."},
            {"texto_opcion": "$5,000,000 - $20,000,000", "valor": "alto", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Presupuesto alto permite implementar sistemas integrales de gestión energética."},
            {"texto_opcion": "Más de $20,000,000", "valor": "muy_alto", "orden": 4, "tiene_sugerencia": True, "sugerencia": "Con presupuesto amplio, considere soluciones completas incluyendo energías renovables."},
            {"texto_opcion": "Depende de los resultados", "valor": "variable", "orden": 5, "tiene_sugerencia": True, "sugerencia": "Perfecto enfoque. Una auditoría le mostrará el ROI de diferentes alternativas."},
            {"texto_opcion": "Aún no lo hemos definido", "valor": "sin_definir", "orden": 6, "es_especial": True, "tiene_sugerencia": True, "sugerencia": "Una auditoría energética le ayudará a definir presupuestos basados en retornos reales."}
        ],
        
        8: [  # Timeframe
            {"texto_opcion": "Inmediatamente (1-3 meses)", "valor": "inmediato", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Para implementación rápida, enfóquese en medidas operacionales y cambios de bajo costo."},
            {"texto_opcion": "Corto plazo (3-6 meses)", "valor": "corto", "orden": 2, "tiene_sugerencia": True, "sugerencia": "Plazo ideal para implementar mejoras graduales con excelente retorno de inversión."},
            {"texto_opcion": "Mediano plazo (6-12 meses)", "valor": "mediano", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Tiempo suficiente para planificar e implementar soluciones integrales más complejas."},
            {"texto_opcion": "Largo plazo (+12 meses)", "valor": "largo", "orden": 4, "tiene_sugerencia": True, "sugerencia": "Perfecto para proyectos grandes como energías renovables y sistemas de gestión."},
            {"texto_opcion": "Solo evaluación inicial", "valor": "solo_evaluacion", "orden": 5, "tiene_sugerencia": True, "sugerencia": "Una evaluación inicial le dará la base para planificar implementaciones futuras."}
        ],
        
        9: [  # Contacto
            {"texto_opcion": "Email con reporte detallado", "valor": "email", "orden": 1},
            {"texto_opcion": "Llamada telefónica", "valor": "telefono", "orden": 2},
            {"texto_opcion": "Reunión presencial/virtual", "valor": "reunion", "orden": 3},
            {"texto_opcion": "WhatsApp/Mensaje", "valor": "whatsapp", "orden": 4},
            {"texto_opcion": "Prefiero no ser contactado", "valor": "no_contacto", "orden": 5, "es_especial": True}
        ]
    }
    
    if numero_orden in opciones_por_pregunta:
        opciones = opciones_por_pregunta[numero_orden]
        
        for opcion_data in opciones:
            opcion_data["pregunta_id"] = pregunta_id
            
            # Valores por defecto
            if "es_por_defecto" not in opcion_data:
                opcion_data["es_por_defecto"] = False
            if "es_especial" not in opcion_data:
                opcion_data["es_especial"] = False
            if "es_activa" not in opcion_data:
                opcion_data["es_activa"] = True
            if "tiene_sugerencia" not in opcion_data:
                opcion_data["tiene_sugerencia"] = False
            if "sugerencia" not in opcion_data:
                opcion_data["sugerencia"] = None
            
            resultado = api_call("POST", "/autodiagnostico/admin/opciones", opcion_data, token)
            # No print para cada opción para no llenar la consola

if __name__ == "__main__":
    main()
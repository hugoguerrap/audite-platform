#!/usr/bin/env python3
"""
Script para crear formularios de demostración completos
con todos los tipos de preguntas y funcionalidades avanzadas
"""

import requests
import json
import time

# Configuración
API_BASE = "http://localhost:18000"
ADMIN_CREDENTIALS = {
    "username": "admin_audite", 
    "password": "AuditE2024!SecureAdmin#2024"
}

def get_admin_token():
    """Obtener token de administrador"""
    response = requests.post(
        f"{API_BASE}/admin/auth/login",
        json=ADMIN_CREDENTIALS
    )
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Error login admin: {response.text}")

def api_call(method, endpoint, data=None, token=None):
    """Función helper para llamadas API"""
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
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"❌ Error en {endpoint}: {response.status_code} - {response.text}")
        return None

def main():
    print("🎨 CREANDO FORMULARIOS DE DEMOSTRACIÓN")
    print("=====================================")
    
    try:
        # 1. Obtener token admin
        print("🔐 Obteniendo token de administrador...")
        token = get_admin_token()
        print("✅ Token obtenido exitosamente")
        
        # 2. Crear formularios para cada categoría
        categorias = api_call("GET", "/api/categorias-industria")
        if not categorias or not categorias.get("categorias"):
            print("❌ No se encontraron categorías")
            return
        
        for categoria in categorias["categorias"]:
            print(f"\n🏭 Procesando categoría: {categoria['nombre']}")
            
            # Crear formulario específico para la categoría
            formulario_data = {
                "categoria_id": categoria["id"],
                "nombre": f"Diagnóstico {categoria['nombre']} Completo",
                "descripcion": f"Evaluación energética especializada para el sector {categoria['nombre'].lower()} con preguntas condicionales y análisis avanzado",
                "activo": True,
                "orden": 1,
                "tiempo_estimado": 15 + categoria["id"] * 3  # 15, 18, 21 minutos
            }
            
            formulario = api_call("POST", "/api/admin/formularios", formulario_data, token)
            if not formulario:
                continue
                
            print(f"✅ Formulario creado: ID {formulario['id']}")
            
            # 3. Crear preguntas específicas por categoría
            crear_preguntas_por_categoria(categoria, formulario, token)
            
        print("\n🎉 ¡FORMULARIOS DE DEMOSTRACIÓN CREADOS EXITOSAMENTE!")
        print("\n📍 Accede a: http://localhost:18080/admin")
        print("👤 Usuario: admin_audite")
        print("🔑 Contraseña: AuditE2024!SecureAdmin#2024")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def crear_preguntas_por_categoria(categoria, formulario, token):
    """Crear preguntas específicas según la categoría"""
    
    formulario_id = formulario["id"]
    categoria_nombre = categoria["nombre"]
    
    if categoria_nombre == "Industrial":
        crear_preguntas_industriales(formulario_id, token)
    elif categoria_nombre == "Comercial":
        crear_preguntas_comerciales(formulario_id, token)
    elif categoria_nombre == "Agropecuario":
        crear_preguntas_agropecuarias(formulario_id, token)

def crear_preguntas_industriales(formulario_id, token):
    """Preguntas para el sector industrial con condicionales avanzados"""
    
    preguntas = [
        # Pregunta 1: Información básica
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuál es el tipo de industria de su empresa?",
            "subtitulo": "Esta información nos ayudará a personalizar las recomendaciones",
            "tipo": "radio",
            "opciones": [
                {"value": "manufactura", "label": "Manufactura y producción"},
                {"value": "alimentaria", "label": "Industria alimentaria"},
                {"value": "textil", "label": "Industria textil"},
                {"value": "metalmecanica", "label": "Metalmecánica"},
                {"value": "quimica", "label": "Química y farmacéutica"},
                {"value": "otro", "label": "Otro"}
            ],
            "tiene_opcion_otro": True,
            "placeholder_otro": "Especifique su tipo de industria",
            "orden": 1,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 2: Tamaño de planta
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuál es el área aproximada de su planta industrial?",
            "tipo": "radio",
            "opciones": [
                {"value": "pequena", "label": "Menos de 1,000 m²"},
                {"value": "mediana", "label": "1,000 - 5,000 m²"},
                {"value": "grande", "label": "5,000 - 20,000 m²"},
                {"value": "muy_grande", "label": "Más de 20,000 m²"}
            ],
            "orden": 2,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 3: Equipos principales (checkbox)
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué tipos de equipos industriales utiliza?",
            "subtitulo": "Seleccione todos los que apliquen a su operación",
            "tipo": "checkbox",
            "opciones": [
                {"value": "hornos", "label": "Hornos industriales"},
                {"value": "compresores", "label": "Compresores de aire"},
                {"value": "motores", "label": "Motores eléctricos"},
                {"value": "soldadura", "label": "Equipos de soldadura"},
                {"value": "refrigeracion", "label": "Sistemas de refrigeración"},
                {"value": "ventilacion", "label": "Sistemas de ventilación"},
                {"value": "automatizacion", "label": "Sistemas de automatización"}
            ],
            "orden": 3,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 4: Horarios de operación
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuáles son sus horarios principales de operación?",
            "tipo": "radio",
            "opciones": [
                {"value": "8x5", "label": "8 horas, 5 días a la semana"},
                {"value": "12x5", "label": "12 horas, 5 días a la semana"},
                {"value": "16x5", "label": "16 horas, 5 días a la semana"},
                {"value": "24x5", "label": "24 horas, 5 días a la semana"},
                {"value": "24x7", "label": "24 horas, 7 días a la semana"}
            ],
            "orden": 4,
            "requerida": True,
            "activa": True
        },
        
        # PREGUNTA CONDICIONAL 5: Solo si tiene hornos
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué tipo de combustible utilizan sus hornos industriales?",
            "tipo": "checkbox",
            "opciones": [
                {"value": "gas_natural", "label": "Gas natural"},
                {"value": "gnc", "label": "GNC (Gas Natural Comprimido)"},
                {"value": "diesel", "label": "Diésel"},
                {"value": "electricidad", "label": "Electricidad"},
                {"value": "carbon", "label": "Carbón"},
                {"value": "biomasa", "label": "Biomasa"}
            ],
            "orden": 5,
            "requerida": True,
            "activa": True,
            "pregunta_padre_id": 3,  # Pregunta de equipos
            "condicion_valor": {"valor": ["hornos"]},
            "condicion_operador": "includes"
        },
        
        # Pregunta 6: Facturación energética
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuál es su facturación energética mensual aproximada?",
            "tipo": "radio",
            "opciones": [
                {"value": "bajo", "label": "Menos de $500,000"},
                {"value": "medio", "label": "$500,000 - $2,000,000"},
                {"value": "alto", "label": "$2,000,000 - $5,000,000"},
                {"value": "muy_alto", "label": "Más de $5,000,000"}
            ],
            "orden": 6,
            "requerida": True,
            "activa": True
        },
        
        # PREGUNTA CONDICIONAL 7: Solo si facturación alta
        {
            "formulario_id": formulario_id,
            "texto": "Con una facturación energética alta, ¿cuáles son sus prioridades de ahorro?",
            "subtitulo": "Seleccione hasta 3 opciones en orden de prioridad",
            "tipo": "checkbox",
            "opciones": [
                {"value": "reducir_costos", "label": "Reducir costos operativos"},
                {"value": "mejorar_eficiencia", "label": "Mejorar eficiencia de equipos"},
                {"value": "energia_renovable", "label": "Implementar energías renovables"},
                {"value": "automatizacion", "label": "Automatización y control"},
                {"value": "mantenimiento", "label": "Optimizar mantenimiento"},
                {"value": "capacitacion", "label": "Capacitación del personal"}
            ],
            "orden": 7,
            "requerida": False,
            "activa": True,
            "pregunta_padre_id": 6,  # Pregunta de facturación
            "condicion_valor": {"valor": ["alto", "muy_alto"]},
            "condicion_operador": "includes"
        },
        
        # Pregunta 8: Campo de texto libre
        {
            "formulario_id": formulario_id,
            "texto": "Describa brevemente sus principales desafíos energéticos",
            "subtitulo": "Esta información nos ayudará a generar recomendaciones más precisas",
            "tipo": "textarea",
            "opciones": None,
            "orden": 8,
            "requerida": False,
            "activa": True
        },
        
        # Pregunta 9: Campo numérico
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuántos empleados trabajan en su planta industrial?",
            "tipo": "number",
            "opciones": None,
            "orden": 9,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 10: Select dropdown
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuál es la antigüedad promedio de sus equipos principales?",
            "tipo": "select",
            "opciones": [
                {"value": "nuevos", "label": "Menos de 2 años"},
                {"value": "recientes", "label": "2-5 años"},
                {"value": "medios", "label": "5-10 años"},
                {"value": "antiguos", "label": "10-15 años"},
                {"value": "muy_antiguos", "label": "Más de 15 años"}
            ],
            "orden": 10,
            "requerida": True,
            "activa": True
        }
    ]
    
    # Crear las preguntas
    for pregunta_data in preguntas:
        pregunta = api_call("POST", "/api/admin/preguntas", pregunta_data, token)
        if pregunta:
            print(f"   ✅ Pregunta industrial creada: {pregunta_data['texto'][:50]}...")
        time.sleep(0.1)  # Pequeña pausa entre requests

def crear_preguntas_comerciales(formulario_id, token):
    """Preguntas para el sector comercial"""
    
    preguntas = [
        # Pregunta 1: Tipo de negocio
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué tipo de establecimiento comercial es?",
            "tipo": "radio",
            "opciones": [
                {"value": "oficina", "label": "Oficinas corporativas"},
                {"value": "retail", "label": "Tienda retail/comercio"},
                {"value": "restaurante", "label": "Restaurante/cafetería"},
                {"value": "centro_comercial", "label": "Centro comercial"},
                {"value": "hotel", "label": "Hotel/hospedaje"},
                {"value": "otro", "label": "Otro tipo"}
            ],
            "tiene_opcion_otro": True,
            "placeholder_otro": "Especifique el tipo de establecimiento",
            "orden": 1,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 2: Área del local
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuál es el área total de su establecimiento?",
            "tipo": "radio",
            "opciones": [
                {"value": "muy_pequeno", "label": "Menos de 50 m²"},
                {"value": "pequeno", "label": "50 - 200 m²"},
                {"value": "mediano", "label": "200 - 500 m²"},
                {"value": "grande", "label": "500 - 2,000 m²"},
                {"value": "muy_grande", "label": "Más de 2,000 m²"}
            ],
            "orden": 2,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 3: Sistemas de climatización
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué sistemas de climatización utiliza?",
            "tipo": "checkbox",
            "opciones": [
                {"value": "ac_central", "label": "Aire acondicionado central"},
                {"value": "ac_split", "label": "Aires acondicionados tipo split"},
                {"value": "ventiladores", "label": "Ventiladores"},
                {"value": "calefaccion", "label": "Sistema de calefacción"},
                {"value": "ninguno", "label": "Sin climatización"}
            ],
            "orden": 3,
            "requerida": True,
            "activa": True
        },
        
        # PREGUNTA CONDICIONAL 4: Solo para restaurantes
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué equipos de cocina profesional utiliza?",
            "subtitulo": "Estos equipos suelen ser los de mayor consumo energético",
            "tipo": "checkbox",
            "opciones": [
                {"value": "cocina_gas", "label": "Cocina a gas"},
                {"value": "cocina_electrica", "label": "Cocina eléctrica"},
                {"value": "horno_conveccion", "label": "Horno de convección"},
                {"value": "freidora", "label": "Freidora industrial"},
                {"value": "parrilla", "label": "Parrilla/plancha"},
                {"value": "lavavajillas", "label": "Lavavajillas industrial"},
                {"value": "refrigerador_comercial", "label": "Refrigeradores comerciales"},
                {"value": "congelador", "label": "Congeladores"}
            ],
            "orden": 4,
            "requerida": True,
            "activa": True,
            "pregunta_padre_id": 1,  # Pregunta tipo de negocio
            "condicion_valor": {"valor": "restaurante"},
            "condicion_operador": "="
        },
        
        # Pregunta 5: Horarios de atención
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuáles son sus horarios de atención al público?",
            "tipo": "radio",
            "opciones": [
                {"value": "horario_comercial", "label": "Horario comercial (8:00 - 18:00)"},
                {"value": "horario_extendido", "label": "Horario extendido (8:00 - 22:00)"},
                {"value": "horario_mall", "label": "Horario de mall (10:00 - 22:00)"},
                {"value": "24_horas", "label": "24 horas"},
                {"value": "fines_semana", "label": "Solo fines de semana"}
            ],
            "orden": 5,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 6: Iluminación
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué tipo de iluminación predomina en su establecimiento?",
            "tipo": "radio",
            "opciones": [
                {"value": "led", "label": "LED (Alta eficiencia)"},
                {"value": "fluorescente", "label": "Fluorescente"},
                {"value": "incandescente", "label": "Incandescente"},
                {"value": "halogeno", "label": "Halógeno"},
                {"value": "mixto", "label": "Combinación de varios tipos"}
            ],
            "orden": 6,
            "requerida": True,
            "activa": True
        },
        
        # PREGUNTA CONDICIONAL 7: Solo si NO es LED
        {
            "formulario_id": formulario_id,
            "texto": "¿Estaría interesado en un plan de actualización a iluminación LED?",
            "subtitulo": "El cambio a LED puede generar ahorros del 50-80% en iluminación",
            "tipo": "radio",
            "opciones": [
                {"value": "muy_interesado", "label": "Muy interesado - implementar inmediatamente"},
                {"value": "interesado", "label": "Interesado - evaluar costos"},
                {"value": "tal_vez", "label": "Tal vez - necesito más información"},
                {"value": "no_interesado", "label": "No interesado por ahora"}
            ],
            "orden": 7,
            "requerida": False,
            "activa": True,
            "pregunta_padre_id": 6,  # Pregunta tipo iluminación
            "condicion_valor": {"valor": "led"},
            "condicion_operador": "!="
        }
    ]
    
    for pregunta_data in preguntas:
        pregunta = api_call("POST", "/api/admin/preguntas", pregunta_data, token)
        if pregunta:
            condicional = " (CONDICIONAL)" if pregunta_data.get("pregunta_padre_id") else ""
            print(f"   ✅ Industrial{condicional}: {pregunta_data['texto'][:40]}...")
        time.sleep(0.1)

def crear_preguntas_comerciales(formulario_id, token):
    """Preguntas para el sector comercial"""
    
    preguntas = [
        # Pregunta 1: Área del local
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuál es el área de su local comercial?",
            "tipo": "number",
            "opciones": None,
            "orden": 1,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 2: Número de empleados
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuántas personas trabajan habitualmente en el local?",
            "tipo": "select",
            "opciones": [
                {"value": "1-3", "label": "1 a 3 personas"},
                {"value": "4-10", "label": "4 a 10 personas"},
                {"value": "11-25", "label": "11 a 25 personas"},
                {"value": "26-50", "label": "26 a 50 personas"},
                {"value": "50+", "label": "Más de 50 personas"}
            ],
            "orden": 2,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 3: Equipos de refrigeración
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué equipos de refrigeración/conservación utiliza?",
            "tipo": "checkbox",
            "opciones": [
                {"value": "refrigerador_comercial", "label": "Refrigeradores comerciales"},
                {"value": "congelador", "label": "Congeladores"},
                {"value": "vitrina_refrigerada", "label": "Vitrinas refrigeradas"},
                {"value": "camara_fria", "label": "Cámara fría"},
                {"value": "ninguno", "label": "No utilizamos refrigeración"}
            ],
            "orden": 3,
            "requerida": True,
            "activa": True
        },
        
        # PREGUNTA CONDICIONAL 4: Solo si tiene refrigeración
        {
            "formulario_id": formulario_id,
            "texto": "¿Con qué frecuencia realiza mantenimiento a sus equipos de refrigeración?",
            "tipo": "radio",
            "opciones": [
                {"value": "mensual", "label": "Mensual"},
                {"value": "trimestral", "label": "Cada 3 meses"},
                {"value": "semestral", "label": "Cada 6 meses"},
                {"value": "anual", "label": "Una vez al año"},
                {"value": "nunca", "label": "No realizamos mantenimiento programado"}
            ],
            "orden": 4,
            "requerida": True,
            "activa": True,
            "pregunta_padre_id": 3,  # Pregunta refrigeración
            "condicion_valor": {"valor": "ninguno"},
            "condicion_operador": "!="
        }
    ]
    
    for pregunta_data in preguntas:
        pregunta = api_call("POST", "/api/admin/preguntas", pregunta_data, token)
        if pregunta:
            condicional = " (CONDICIONAL)" if pregunta_data.get("pregunta_padre_id") else ""
            print(f"   ✅ Comercial{condicional}: {pregunta_data['texto'][:40]}...")
        time.sleep(0.1)

def crear_preguntas_agropecuarias(formulario_id, token):
    """Preguntas para el sector agropecuario"""
    
    preguntas = [
        # Pregunta 1: Tipo de actividad
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuál es su actividad agropecuaria principal?",
            "tipo": "radio",
            "opciones": [
                {"value": "agricultura", "label": "Agricultura (cultivos)"},
                {"value": "ganaderia", "label": "Ganadería"},
                {"value": "avicultura", "label": "Avicultura"},
                {"value": "porcicultura", "label": "Porcicultura"},
                {"value": "lecheria", "label": "Lechería"},
                {"value": "mixto", "label": "Actividad mixta"},
                {"value": "agroindustria", "label": "Agroindustria/procesamiento"}
            ],
            "orden": 1,
            "requerida": True,
            "activa": True
        },
        
        # Pregunta 2: Extensión
        {
            "formulario_id": formulario_id,
            "texto": "¿Cuál es la extensión total de su explotación?",
            "tipo": "radio",
            "opciones": [
                {"value": "pequena", "label": "Menos de 10 hectáreas"},
                {"value": "mediana", "label": "10 - 50 hectáreas"},
                {"value": "grande", "label": "50 - 200 hectáreas"},
                {"value": "muy_grande", "label": "Más de 200 hectáreas"}
            ],
            "orden": 2,
            "requerida": True,
            "activa": True
        },
        
        # PREGUNTA CONDICIONAL 3: Solo para agricultura
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué tipo de sistema de riego utiliza?",
            "tipo": "radio",
            "opciones": [
                {"value": "goteo", "label": "Riego por goteo"},
                {"value": "aspersion", "label": "Riego por aspersión"},
                {"value": "surcos", "label": "Riego por surcos"},
                {"value": "microaspersion", "label": "Microaspersión"},
                {"value": "manual", "label": "Riego manual"},
                {"value": "secano", "label": "Cultivo de secano (sin riego)"}
            ],
            "orden": 3,
            "requerida": True,
            "activa": True,
            "pregunta_padre_id": 1,  # Pregunta actividad principal
            "condicion_valor": {"valor": "agricultura"},
            "condicion_operador": "="
        },
        
        # Pregunta 4: Maquinaria agrícola
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué maquinaria agrícola utiliza regularmente?",
            "subtitulo": "Seleccione todos los equipos que utiliza frecuentemente",
            "tipo": "checkbox",
            "opciones": [
                {"value": "tractor", "label": "Tractores"},
                {"value": "cosechadora", "label": "Cosechadoras"},
                {"value": "pulverizadora", "label": "Pulverizadoras"},
                {"value": "arado", "label": "Arados"},
                {"value": "sembradora", "label": "Sembradoras"},
                {"value": "bomba_agua", "label": "Bombas de agua"},
                {"value": "generador", "label": "Generadores eléctricos"}
            ],
            "orden": 4,
            "requerida": True,
            "activa": True
        },
        
        # PREGUNTA CONDICIONAL 5: Solo si tiene ganadería/lechería
        {
            "formulario_id": formulario_id,
            "texto": "¿Qué equipos utiliza para el manejo del ganado?",
            "tipo": "checkbox",
            "opciones": [
                {"value": "ordenadora", "label": "Máquina ordeñadora"},
                {"value": "tanque_frio", "label": "Tanque de frío"},
                {"value": "mixer", "label": "Mixer de alimentos"},
                {"value": "bebederos", "label": "Bebederos automáticos"},
                {"value": "ventilacion_galpones", "label": "Ventilación de galpones"},
                {"value": "cerca_electrica", "label": "Cerco eléctrico"}
            ],
            "orden": 5,
            "requerida": True,
            "activa": True,
            "pregunta_padre_id": 1,  # Pregunta actividad principal
            "condicion_valor": {"valor": ["ganaderia", "lecheria", "avicultura", "porcicultura"]},
            "condicion_operador": "includes"
        },
        
        # Pregunta 6: Certificaciones
        {
            "formulario_id": formulario_id,
            "texto": "¿Tiene alguna certificación ambiental o de calidad?",
            "tipo": "checkbox",
            "opciones": [
                {"value": "iso_14001", "label": "ISO 14001 (Gestión Ambiental)"},
                {"value": "bpa", "label": "BPA (Buenas Prácticas Agrícolas)"},
                {"value": "organico", "label": "Certificación Orgánica"},
                {"value": "global_gap", "label": "GlobalGAP"},
                {"value": "comercio_justo", "label": "Comercio Justo"},
                {"value": "ninguna", "label": "No tengo certificaciones"}
            ],
            "orden": 6,
            "requerida": False,
            "activa": True
        }
    ]
    
    for pregunta_data in preguntas:
        pregunta = api_call("POST", "/api/admin/preguntas", pregunta_data, token)
        if pregunta:
            condicional = " (CONDICIONAL)" if pregunta_data.get("pregunta_padre_id") else ""
            print(f"   ✅ Agropecuario{condicional}: {pregunta_data['texto'][:40]}...")
        time.sleep(0.1)

def crear_formulario_autodiagnostico_avanzado(token):
    """Crear preguntas adicionales para el autodiagnóstico básico"""
    
    preguntas_adicionales = [
        # Pregunta 2: Tamaño empresa
        {
            "numero_orden": 2,
            "pregunta": "¿Cuál es el tamaño aproximado de su empresa?",
            "tipo_respuesta": "radio",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Considere el número total de empleados y el área de sus instalaciones"
        },
        
        # Pregunta 3: Consumo energético
        {
            "numero_orden": 3,
            "pregunta": "¿Cuál es su principal preocupación energética actual?",
            "tipo_respuesta": "checkbox",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Puede seleccionar múltiples opciones"
        },
        
        # Pregunta 4: Auditoría previa
        {
            "numero_orden": 4,
            "pregunta": "¿Ha realizado alguna auditoría energética anteriormente?",
            "tipo_respuesta": "radio",
            "es_obligatoria": True,
            "es_activa": True,
            "ayuda_texto": "Una auditoría energética es un análisis profesional del uso de energía"
        }
    ]
    
    for pregunta_data in preguntas_adicionales:
        pregunta = api_call("POST", "/autodiagnostico/admin/preguntas", pregunta_data, token)
        if pregunta:
            print(f"   ✅ Autodiagnóstico básico: {pregunta_data['pregunta'][:40]}...")
        time.sleep(0.1)
    
    # Crear opciones para estas preguntas
    crear_opciones_autodiagnostico(token)

def crear_opciones_autodiagnostico(token):
    """Crear opciones para las nuevas preguntas de autodiagnóstico"""
    
    # Obtener las preguntas creadas
    preguntas = api_call("GET", "/autodiagnostico/admin/preguntas", token=token)
    if not preguntas:
        return
    
    for pregunta in preguntas:
        if pregunta["numero_orden"] == 2:  # Tamaño empresa
            opciones = [
                {"texto_opcion": "Microempresa (1-10 empleados)", "valor": "micro", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Para microempresas, enfóquese en cambios de bajo costo con retorno rápido."},
                {"texto_opcion": "Pequeña empresa (11-50 empleados)", "valor": "pequena", "orden": 2, "tiene_sugerencia": True, "sugerencia": "Las pequeñas empresas pueden implementar mejoras graduales con financiamiento accesible."},
                {"texto_opcion": "Mediana empresa (51-200 empleados)", "valor": "mediana", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Las medianas empresas pueden justificar inversiones en tecnología eficiente y sistemas de control."},
                {"texto_opcion": "Gran empresa (+200 empleados)", "valor": "grande", "orden": 4, "tiene_sugerencia": True, "sugerencia": "Las grandes empresas deben implementar sistemas de gestión energética y considerar energías renovables."}
            ]
            
            for opcion in opciones:
                opcion["pregunta_id"] = pregunta["id"]
                api_call("POST", "/autodiagnostico/admin/opciones", opcion, token)
        
        elif pregunta["numero_orden"] == 3:  # Preocupaciones energéticas
            opciones = [
                {"texto_opcion": "Facturas muy altas", "valor": "costos_altos", "orden": 1, "tiene_sugerencia": True, "sugerencia": "Para reducir costos, analice los equipos de mayor consumo y considere horarios de operación."},
                {"texto_opcion": "Equipos antiguos e ineficientes", "valor": "equipos_antiguos", "orden": 2, "tiene_sugerencia": True, "sugerencia": "El reemplazo gradual de equipos antiguos puede generar ahorros significativos."},
                {"texto_opcion": "Cortes de energía frecuentes", "valor": "cortes", "orden": 3, "tiene_sugerencia": True, "sugerencia": "Considere sistemas de respaldo y mejore la calidad de la instalación eléctrica."},
                {"texto_opcion": "Falta de control y monitoreo", "valor": "sin_control", "orden": 4, "tiene_sugerencia": True, "sugerencia": "Un sistema de monitoreo le permitirá identificar oportunidades de ahorro en tiempo real."}
            ]
            
            for opcion in opciones:
                opcion["pregunta_id"] = pregunta["id"]
                api_call("POST", "/autodiagnostico/admin/opciones", opcion, token)

if __name__ == "__main__":
    main()
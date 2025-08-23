#!/usr/bin/env python3
"""
Añadir preguntas avanzadas con condicionales que funcionen
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
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"❌ Error en {endpoint}: {response.status_code} - {response.text}")
        return None

def main():
    print("🔗 AÑADIENDO PREGUNTAS AVANZADAS Y CONDICIONALES")
    print("===============================================")
    
    token = get_admin_token()
    
    # 1. Obtener preguntas del formulario industrial
    preguntas_industriales = api_call("GET", "/api/formulario/1/preguntas", token=token)
    
    if preguntas_industriales:
        # Buscar pregunta de equipos para crear condicional
        pregunta_equipos_id = None
        for p in preguntas_industriales:
            if "equipos industriales" in p["texto"].lower():
                pregunta_equipos_id = p["id"]
                break
        
        if pregunta_equipos_id:
            # Crear pregunta condicional correcta
            pregunta_condicional = {
                "formulario_id": 1,
                "texto": "¿Cuál es la potencia total aproximada de sus hornos industriales?",
                "subtitulo": "Solo conteste si seleccionó que utiliza hornos industriales",
                "tipo": "select",
                "opciones": [
                    {"value": "baja", "label": "Menos de 100 kW"},
                    {"value": "media", "label": "100 - 500 kW"},
                    {"value": "alta", "label": "500 - 1000 kW"},
                    {"value": "muy_alta", "label": "Más de 1000 kW"}
                ],
                "orden": 50,
                "requerida": True,
                "activa": True,
                "pregunta_padre_id": pregunta_equipos_id,
                "condicion_valor": {"valor": "hornos"},
                "condicion_operador": "includes"
            }
            
            resultado = api_call("POST", "/api/admin/preguntas", pregunta_condicional, token)
            if resultado:
                print("✅ Pregunta condicional de hornos creada exitosamente")
        
        # Buscar pregunta de área para crear otra condicional
        pregunta_area_id = None
        for p in preguntas_industriales:
            if "área aproximada" in p["texto"].lower():
                pregunta_area_id = p["id"]
                break
        
        if pregunta_area_id:
            # Crear pregunta condicional para plantas grandes
            pregunta_gestion = {
                "formulario_id": 1,
                "texto": "Para plantas industriales grandes, ¿tiene implementado algún sistema de gestión energética?",
                "tipo": "radio",
                "opciones": [
                    {"value": "iso_50001", "label": "ISO 50001 certificado"},
                    {"value": "sistema_basico", "label": "Sistema básico de monitoreo"},
                    {"value": "en_desarrollo", "label": "En proceso de implementación"},
                    {"value": "no_tiene", "label": "No tiene sistema de gestión"}
                ],
                "orden": 51,
                "requerida": False,
                "activa": True,
                "pregunta_padre_id": pregunta_area_id,
                "condicion_valor": {"valor": ["grande", "muy_grande"]},
                "condicion_operador": "includes"
            }
            
            resultado = api_call("POST", "/api/admin/preguntas", pregunta_gestion, token)
            if resultado:
                print("✅ Pregunta condicional de gestión energética creada")

    # 2. Añadir pregunta de texto libre al formulario comercial
    pregunta_texto_libre = {
        "formulario_id": 2,
        "texto": "¿Cuáles considera que son sus principales oportunidades de ahorro energético?",
        "subtitulo": "Describa en sus propias palabras qué aspectos cree que podrían mejorar",
        "tipo": "textarea",
        "opciones": None,
        "orden": 10,
        "requerida": False,
        "activa": True
    }
    
    resultado = api_call("POST", "/api/admin/preguntas", pregunta_texto_libre, token)
    if resultado:
        print("✅ Pregunta de texto libre añadida al formulario comercial")

    # 3. Añadir pregunta tipo ordering al formulario agropecuario
    pregunta_prioridades_agro = {
        "formulario_id": 3,
        "texto": "Ordene por prioridad las siguientes áreas de mejora energética",
        "subtitulo": "Arrastre y ordene del 1 (más importante) al 5 (menos importante)",
        "tipo": "ordering",
        "opciones": [
            {"value": "riego", "label": "Optimización del sistema de riego"},
            {"value": "maquinaria", "label": "Renovación de maquinaria"},
            {"value": "instalaciones", "label": "Mejora de instalaciones"},
            {"value": "renovables", "label": "Implementación de energías renovables"},
            {"value": "automatizacion", "label": "Automatización de procesos"}
        ],
        "orden": 10,
        "requerida": True,
        "activa": True
    }
    
    resultado = api_call("POST", "/api/admin/preguntas", pregunta_prioridades_agro, token)
    if resultado:
        print("✅ Pregunta tipo 'ordering' añadida al formulario agropecuario")

    print("\n🎉 ¡PREGUNTAS AVANZADAS AÑADIDAS!")
    print("\n📊 RESUMEN FINAL:")
    
    # Mostrar resumen final
    for form_id in [1, 2, 3]:
        preguntas = api_call("GET", f"/api/formulario/{form_id}/preguntas", token=token)
        categoria = ["Industrial", "Comercial", "Agropecuario"][form_id-1]
        if preguntas:
            condicionales = sum(1 for p in preguntas if p.get("pregunta_padre_id"))
            print(f"   📋 {categoria}: {len(preguntas)} preguntas ({condicionales} condicionales)")

if __name__ == "__main__":
    main()
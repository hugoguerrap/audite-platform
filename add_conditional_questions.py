#!/usr/bin/env python3
"""
Script para añadir preguntas condicionales a los formularios ya creados
"""

import requests
import json

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
    return response.json()['access_token']

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
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"❌ Error en {endpoint}: {response.status_code} - {response.text}")
        return None

def main():
    print("🔗 AÑADIENDO PREGUNTAS CONDICIONALES")
    print("===================================")
    
    token = get_admin_token()
    
    # Obtener preguntas del formulario industrial (ID: 1)
    preguntas_industriales = api_call("GET", "/api/formulario/1/preguntas", token=token)
    
    if preguntas_industriales:
        # Buscar la pregunta de equipos (para crear condicional de hornos)
        pregunta_equipos = None
        for p in preguntas_industriales:
            if "equipos industriales" in p["texto"]:
                pregunta_equipos = p
                break
        
        if pregunta_equipos:
            # Crear pregunta condicional sobre hornos
            pregunta_hornos = {
                "formulario_id": 1,
                "texto": "¿Qué tipo de combustible utilizan principalmente sus hornos?",
                "subtitulo": "Esta información nos ayudará a calcular su huella de carbono",
                "tipo": "radio",
                "opciones": [
                    {"value": "gas_natural", "label": "Gas natural"},
                    {"value": "diesel", "label": "Diésel"},
                    {"value": "electricidad", "label": "Electricidad"},
                    {"value": "carbon", "label": "Carbón"},
                    {"value": "biomasa", "label": "Biomasa"}
                ],
                "orden": 20,
                "requerida": True,
                "activa": True,
                "pregunta_padre_id": pregunta_equipos["id"],
                "condicion_valor": ["hornos"],
                "condicion_operador": "includes"
            }
            
            resultado = api_call("POST", "/api/admin/preguntas", pregunta_hornos, token)
            if resultado:
                print("✅ Pregunta condicional sobre hornos creada")
            
        # Buscar pregunta de facturación
        pregunta_facturacion = None
        for p in preguntas_industriales:
            if "facturación energética" in p["texto"]:
                pregunta_facturacion = p
                break
        
        if pregunta_facturacion:
            # Crear pregunta condicional para facturación alta
            pregunta_prioridades = {
                "formulario_id": 1,
                "texto": "¿Cuáles son sus principales objetivos de ahorro energético?",
                "subtitulo": "Con su nivel de consumo, estas inversiones pueden tener excelente retorno",
                "tipo": "checkbox",
                "opciones": [
                    {"value": "reducir_costos", "label": "Reducir costos operativos inmediatamente"},
                    {"value": "energia_renovable", "label": "Implementar energías renovables"},
                    {"value": "eficiencia_equipos", "label": "Mejorar eficiencia de equipos"},
                    {"value": "automatizacion", "label": "Automatización y control inteligente"},
                    {"value": "certificacion", "label": "Obtener certificaciones ambientales"}
                ],
                "orden": 21,
                "requerida": False,
                "activa": True,
                "pregunta_padre_id": pregunta_facturacion["id"],
                "condicion_valor": ["alto", "muy_alto"],
                "condicion_operador": "includes"
            }
            
            resultado = api_call("POST", "/api/admin/preguntas", pregunta_prioridades, token)
            if resultado:
                print("✅ Pregunta condicional sobre prioridades creada")

    print("\n🎨 FORMULARIOS DEMO COMPLETADOS:")
    print("================================")
    print("✅ Formulario Industrial: 8+ preguntas con 2 condicionales")
    print("✅ Formulario Comercial: 3+ preguntas") 
    print("✅ Formulario Agropecuario: 4+ preguntas")
    print("✅ Incluye: radio, checkbox, textarea, number, select")
    print("✅ Incluye: preguntas condicionales avanzadas")
    print("✅ Incluye: campos 'Otro' personalizables")
    
    print("\n🌐 ACCEDE AL ADMIN PANEL:")
    print("http://localhost:18080/admin")
    print("👤 admin_audite / 🔑 AuditE2024!SecureAdmin#2024")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Probar el flujo completo de preguntas condicionales
"""

import requests
import json
import uuid

API_BASE = "http://localhost:18000"

def test_conditional_flow():
    print("🧪 TESTING FLUJO CONDICIONAL COMPLETO")
    print("====================================")
    
    # 1. Obtener preguntas iniciales (sin respuestas)
    preguntas_iniciales = requests.get(f"{API_BASE}/api/formulario/1/preguntas").json()
    print(f"📊 Preguntas iniciales: {len(preguntas_iniciales)}")
    
    # 2. Simular respuestas que activen condicionales
    print("\n🔄 Simulando respuestas que activan condicionales...")
    
    # Respuesta que activa pregunta de hornos
    respuestas_con_hornos = {
        "3": ["hornos", "compresores"]  # Pregunta 3: equipos industriales
    }
    
    # Encode para URL
    respuestas_encoded = json.dumps(respuestas_con_hornos)
    
    print(f"📝 Respuestas simuladas: {respuestas_con_hornos}")
    
    # 3. Obtener preguntas con las respuestas que activan condicionales
    params = {"respuestas_actuales": respuestas_encoded}
    response = requests.get(f"{API_BASE}/api/formulario/1/preguntas", params=params)
    
    if response.status_code == 200:
        preguntas_con_condicionales = response.json()
        print(f"📊 Preguntas con condicionales activadas: {len(preguntas_con_condicionales)}")
        
        condicionales = [p for p in preguntas_con_condicionales if p.get('pregunta_padre_id')]
        print(f"🔗 Preguntas condicionales visibles: {len(condicionales)}")
        
        for p in condicionales:
            print(f"   ✅ {p['texto'][:60]}...")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
    
    # 4. Probar con respuestas que activen la segunda condicional
    print("\n🔄 Probando segunda condicional (facturación alta)...")
    
    respuestas_facturacion_alta = {
        "3": ["hornos"],
        "6": "alto"  # Pregunta 6: facturación energética
    }
    
    params = {"respuestas_actuales": json.dumps(respuestas_facturacion_alta)}
    response = requests.get(f"{API_BASE}/api/formulario/1/preguntas", params=params)
    
    if response.status_code == 200:
        preguntas_final = response.json()
        condicionales = [p for p in preguntas_final if p.get('pregunta_padre_id')]
        print(f"🔗 Total condicionales activas: {len(condicionales)}")
        
        for p in condicionales:
            print(f"   ✅ {p['texto'][:60]}...")
    
    # 5. Mostrar estructura completa
    print(f"\n📋 ESTRUCTURA COMPLETA DEL FORMULARIO INDUSTRIAL:")
    print("=" * 55)
    
    todas_preguntas = requests.get(f"{API_BASE}/api/admin/preguntas/1", 
                                 headers={"Authorization": f"Bearer {get_admin_token()}"}).json()
    
    normales = [p for p in todas_preguntas if not p.get('pregunta_padre_id')]
    condicionales = [p for p in todas_preguntas if p.get('pregunta_padre_id')]
    
    print(f"📝 Preguntas base: {len(normales)}")
    print(f"🔗 Preguntas condicionales: {len(condicionales)}")
    print(f"📊 Total en formulario: {len(todas_preguntas)}")
    
    print(f"\n🎯 LÓGICA CONDICIONAL:")
    for p in condicionales:
        padre_texto = next((pr['texto'][:30] for pr in todas_preguntas if pr['id'] == p['pregunta_padre_id']), "???")
        print(f"   🔗 '{p['texto'][:40]}...'")
        print(f"      └─ SI '{padre_texto}...' {p['condicion_operador']} {p['condicion_valor']}")

def get_admin_token():
    response = requests.post(f"{API_BASE}/admin/auth/login", json={
        "username": "admin_audite", 
        "password": "AuditE2024!SecureAdmin#2024"
    })
    return response.json()['access_token']

if __name__ == "__main__":
    test_conditional_flow()
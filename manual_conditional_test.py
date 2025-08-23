#!/usr/bin/env python3
"""
Testing manual de la lógica condicional
"""

import requests
import json

API_BASE = "http://localhost:18000"

def get_admin_token():
    response = requests.post(f"{API_BASE}/admin/auth/login", json={
        "username": "admin_audite", 
        "password": "AuditE2024!SecureAdmin#2024"
    })
    return response.json()['access_token']

def main():
    print("🔍 TESTING MANUAL DE CONDICIONALES")
    print("==================================")
    
    token = get_admin_token()
    
    # 1. Ver TODAS las preguntas desde admin
    todas_preguntas = requests.get(
        f"{API_BASE}/api/admin/preguntas/1",
        headers={"Authorization": f"Bearer {token}"}
    ).json()
    
    print(f"📊 Total preguntas en formulario: {len(todas_preguntas)}")
    
    normales = [p for p in todas_preguntas if not p.get('pregunta_padre_id')]
    condicionales = [p for p in todas_preguntas if p.get('pregunta_padre_id')]
    
    print(f"📝 Preguntas normales: {len(normales)}")
    print(f"🔗 Preguntas condicionales: {len(condicionales)}")
    
    print(f"\n🔗 PREGUNTAS CONDICIONALES CREADAS:")
    for p in condicionales:
        padre = next((pr for pr in todas_preguntas if pr['id'] == p['pregunta_padre_id']), None)
        padre_texto = padre['texto'][:25] if padre else "???"
        
        print(f"   ID {p['id']:2d}: {p['texto'][:45]}...")
        print(f"        └─ Depende de: '{padre_texto}...' (ID: {p['pregunta_padre_id']})")
        print(f"        └─ Condición: {p['condicion_valor']} {p['condicion_operador']}")
        print()

    # 2. Simular evaluación manual
    print("🧪 SIMULACIÓN MANUAL DE EVALUACIÓN:")
    print("===================================")
    
    # Simular respuesta que debería activar hornos
    print("Caso 1: Usuario selecciona 'hornos' en equipos...")
    respuesta_equipos = ["hornos", "compresores"]
    
    # Buscar pregunta condicional de hornos
    pregunta_hornos = next((p for p in condicionales if "combustible" in p['texto'].lower()), None)
    
    if pregunta_hornos:
        condicion = pregunta_hornos['condicion_valor']
        operador = pregunta_hornos['condicion_operador']
        
        print(f"   Pregunta condicional: {pregunta_hornos['texto'][:40]}...")
        print(f"   Condición configurada: {condicion} {operador}")
        
        # Evaluar manualmente
        if operador == "includes":
            valor_esperado = condicion.get('valor') if isinstance(condicion, dict) else condicion
            
            if isinstance(valor_esperado, str):
                cumple_condicion = valor_esperado in respuesta_equipos
            elif isinstance(valor_esperado, list):
                cumple_condicion = any(v in respuesta_equipos for v in valor_esperado)
            else:
                cumple_condicion = False
                
            print(f"   ✅ ¿Debería mostrarse? {cumple_condicion}")
            print(f"   📝 Lógica: '{valor_esperado}' in {respuesta_equipos} = {cumple_condicion}")

    # 3. Verificar endpoint con debugging
    print(f"\n🔍 DEBUGGING ENDPOINT:")
    respuestas_debug = {"3": ["hornos"]}
    
    # Hacer llamada con debug
    response = requests.get(
        f"{API_BASE}/api/formulario/1/preguntas",
        params={"respuestas_actuales": json.dumps(respuestas_debug)}
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        preguntas_resultado = response.json()
        print(f"   Preguntas devueltas: {len(preguntas_resultado)}")
        
        # Ver si alguna tiene pregunta_padre_id
        condicionales_en_respuesta = [p for p in preguntas_resultado if p.get('pregunta_padre_id')]
        print(f"   Condicionales en respuesta: {len(condicionales_en_respuesta)}")
    else:
        print(f"   Error: {response.text}")

if __name__ == "__main__":
    main()
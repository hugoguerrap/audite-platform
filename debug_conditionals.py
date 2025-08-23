#!/usr/bin/env python3
"""
Debug completo de la lógica condicional
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
    print("🔍 DEBUG COMPLETO - LÓGICA CONDICIONAL")
    print("======================================")
    
    token = get_admin_token()
    
    # 1. Obtener estructura completa
    todas_preguntas = requests.get(
        f"{API_BASE}/api/admin/preguntas/1",
        headers={"Authorization": f"Bearer {token}"}
    ).json()
    
    # Encontrar la pregunta de equipos y sus condicionales
    pregunta_equipos = next((p for p in todas_preguntas if p['id'] == 3), None)
    condicionales_hornos = [p for p in todas_preguntas if p.get('pregunta_padre_id') == 3]
    
    print(f"📊 Pregunta padre (equipos): ID {pregunta_equipos['id']}")
    print(f"🔗 Condicionales que dependen: {len(condicionales_hornos)}")
    
    for p in condicionales_hornos:
        print(f"   - ID {p['id']}: {p['texto'][:40]}...")
        print(f"     Condición: {p['condicion_valor']} {p['condicion_operador']}")
    
    print(f"\n🧪 TESTING DIFERENTES FORMATOS DE RESPUESTA:")
    
    # Test 1: Formato string
    test_cases = [
        {"description": "ID como string, valor como lista", "data": {"3": ["hornos"]}},
        {"description": "ID como int, valor como lista", "data": {3: ["hornos"]}},
        {"description": "ID como string, valor como string", "data": {"3": "hornos"}},
        {"description": "Valor exacto de la BD", "data": {"3": ["hornos", "compresores"]}},
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['description']}:")
        print(f"   Datos: {test['data']}")
        
        # Hacer llamada
        try:
            response = requests.get(
                f"{API_BASE}/api/formulario/1/preguntas",
                params={"respuestas_actuales": json.dumps(test['data'])}
            )
            
            if response.status_code == 200:
                preguntas = response.json()
                condicionales = [p for p in preguntas if p.get('pregunta_padre_id')]
                print(f"   ✅ Total preguntas: {len(preguntas)}")
                print(f"   🔗 Condicionales: {len(condicionales)}")
                
                if condicionales:
                    for p in condicionales:
                        print(f"      - {p['texto'][:35]}...")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test manual directo de la lógica
    print(f"\n🔬 TEST MANUAL DE LA LÓGICA:")
    
    # Simular evaluación
    respuesta_equipos = ["hornos", "compresores"]
    
    for condicional in condicionales_hornos:
        condicion_valor = condicional['condicion_valor']
        operador = condicional['condicion_operador']
        
        print(f"\nPregunta: {condicional['texto'][:40]}...")
        print(f"Condición en BD: {condicion_valor} {operador}")
        
        # Extraer valor esperado
        if isinstance(condicion_valor, dict) and 'valor' in condicion_valor:
            valor_esperado = condicion_valor['valor']
        else:
            valor_esperado = condicion_valor
            
        print(f"Valor esperado extraído: {valor_esperado}")
        print(f"Respuesta simulada: {respuesta_equipos}")
        
        # Evaluar includes manualmente
        if operador == "includes":
            if isinstance(valor_esperado, str):
                resultado = valor_esperado in respuesta_equipos
            elif isinstance(valor_esperado, list):
                resultado = any(v in respuesta_equipos for v in valor_esperado)
            else:
                resultado = False
                
            print(f"✅ Resultado manual: {resultado}")

if __name__ == "__main__":
    main()
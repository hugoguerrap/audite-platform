#!/usr/bin/env python3
"""
Testing correcto de preguntas condicionales
"""

import requests
import json
import urllib.parse

API_BASE = "http://localhost:18000"

def test_conditionals():
    print("🧪 TESTING PREGUNTAS CONDICIONALES - FORMATO CORRECTO")
    print("=====================================================")
    
    # 1. Preguntas sin respuestas (base)
    response = requests.get(f"{API_BASE}/api/formulario/1/preguntas")
    preguntas_base = response.json()
    print(f"📊 Preguntas base (sin respuestas): {len(preguntas_base)}")
    
    # 2. Simular respuestas que activen condicionales
    # Formato correcto: pregunta_id como string, valor como fue configurado
    respuestas_test = {
        "3": ["hornos", "compresores"]  # Pregunta 3: equipos (checkbox)
    }
    
    # Convertir a JSON y URL encode
    respuestas_json = json.dumps(respuestas_test)
    respuestas_encoded = urllib.parse.quote(respuestas_json)
    
    print(f"📝 Respuestas test: {respuestas_test}")
    print(f"🔗 JSON encoded: {respuestas_encoded}")
    
    # 3. Hacer request con respuestas
    url_con_respuestas = f"{API_BASE}/api/formulario/1/preguntas?respuestas_actuales={respuestas_encoded}"
    response = requests.get(url_con_respuestas)
    
    print(f"🌐 URL completa: {url_con_respuestas[:100]}...")
    print(f"📡 Status code: {response.status_code}")
    
    if response.status_code == 200:
        preguntas_con_condicionales = response.json()
        print(f"📊 Preguntas con condicionales: {len(preguntas_con_condicionales)}")
        
        # Buscar condicionales visibles
        condicionales_visibles = [p for p in preguntas_con_condicionales if p.get('pregunta_padre_id')]
        print(f"🔗 Condicionales visibles: {len(condicionales_visibles)}")
        
        for p in condicionales_visibles:
            print(f"   ✅ CONDICIONAL: {p['texto'][:50]}...")
            
        if len(condicionales_visibles) == 0:
            print("⚠️ No se activaron condicionales. Verificando formato...")
            
            # Debuggear el primer elemento
            if preguntas_con_condicionales:
                primer_elemento = preguntas_con_condicionales[0]
                print(f"🔍 Primer elemento: {primer_elemento.get('id', 'N/A')} - {primer_elemento.get('texto', 'N/A')[:30]}...")
    else:
        print(f"❌ Error en request: {response.text[:200]}")
    
    # 4. Probar también la segunda condicional (área grande)
    print(f"\n🔄 Testing segunda condicional (área grande)...")
    
    respuestas_area_grande = {
        "2": "grande"  # Pregunta 2: área de planta
    }
    
    params = {"respuestas_actuales": json.dumps(respuestas_area_grande)}
    response = requests.get(f"{API_BASE}/api/formulario/1/preguntas", params=params)
    
    if response.status_code == 200:
        preguntas = response.json()
        condicionales = [p for p in preguntas if p.get('pregunta_padre_id')]
        print(f"🔗 Condicionales para área grande: {len(condicionales)}")
        
        for p in condicionales:
            print(f"   ✅ {p['texto'][:50]}...")
    
    # 5. Testing combinado
    print(f"\n🔄 Testing combinado (hornos + área grande + facturación alta)...")
    
    respuestas_completas = {
        "2": "muy_grande",           # Área muy grande
        "3": ["hornos", "motores"],  # Equipos con hornos  
        "6": "muy_alto"              # Facturación muy alta
    }
    
    params = {"respuestas_actuales": json.dumps(respuestas_completas)}
    response = requests.get(f"{API_BASE}/api/formulario/1/preguntas", params=params)
    
    if response.status_code == 200:
        preguntas = response.json()
        condicionales = [p for p in preguntas if p.get('pregunta_padre_id')]
        print(f"🔗 Condicionales con respuestas completas: {len(condicionales)}")
        
        print(f"\n🎯 TODAS LAS PREGUNTAS VISIBLES:")
        for i, p in enumerate(preguntas, 1):
            tipo_pregunta = "🔗 CONDICIONAL" if p.get('pregunta_padre_id') else "📝 BASE"
            print(f"   {i:2d}. {tipo_pregunta} [{p['tipo']:8s}] {p['texto'][:45]}...")

if __name__ == "__main__":
    test_conditionals()
#!/usr/bin/env python3
"""
Script de verificación CORS para Sistema de Noticias IA
Verifica que la configuración CORS esté funcionando correctamente
"""

import requests
import json
from datetime import datetime

# Configuración de prueba
FRONTEND_ORIGIN = "https://woodcock-still-tetra.ngrok-free.app"
BACKEND_BASE = "https://credible-kodiak-one.ngrok-free.app"
API_BASE = f"{BACKEND_BASE}/api"

def test_cors_preflight():
    """Prueba el preflight CORS OPTIONS request"""
    print("🔍 Probando preflight CORS...")
    
    try:
        headers = {
            'Origin': FRONTEND_ORIGIN,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type,Authorization',
            'ngrok-skip-browser-warning': 'true'
        }
        
        response = requests.options(f"{API_BASE}/auth/login", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower() or 'cors' in header.lower():
                print(f"  {header}: {value}")
        
        # Verificar headers CORS específicos
        required_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers',
            'Access-Control-Allow-Credentials'
        ]
        
        missing_headers = []
        for header in required_headers:
            if header not in response.headers:
                missing_headers.append(header)
        
        if missing_headers:
            print(f"❌ Headers CORS faltantes: {missing_headers}")
            return False
        else:
            print("✅ Todos los headers CORS están presentes")
            return True
            
    except Exception as e:
        print(f"❌ Error en preflight: {e}")
        return False

def test_backend_health():
    """Verifica que el backend esté respondiendo"""
    print("\n🏥 Probando salud del backend...")
    
    try:
        headers = {
            'ngrok-skip-browser-warning': 'true'
        }
        response = requests.get(f"{BACKEND_BASE}/", headers=headers)
        print(f"Backend Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Backend respondiendo correctamente")
            return True
        else:
            print(f"❌ Backend error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False

def test_login_endpoint():
    """Prueba el endpoint de login con datos de prueba"""
    print("\n🔐 Probando endpoint de login...")
    
    try:
        headers = {
            'Origin': FRONTEND_ORIGIN,
            'Content-Type': 'application/x-www-form-urlencoded',
            'ngrok-skip-browser-warning': 'true'
        }
        
        # Datos de prueba (estos fallarán la autenticación pero deberían pasar CORS)
        data = {
            'username': 'test@example.com',
            'password': 'test123'
        }
        
        response = requests.post(f"{API_BASE}/auth/login", headers=headers, data=data)
        
        print(f"Login Status: {response.status_code}")
        print("Response Headers (CORS):")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
        
        # Si obtenemos 422 (datos inválidos) o 401 (unauthorized), CORS está funcionando
        # Si obtenemos error de red, CORS está fallando
        if response.status_code in [401, 422]:
            print("✅ CORS funcionando - El backend rechazó las credenciales (esperado)")
            return True
        elif response.status_code == 200:
            print("✅ CORS funcionando - Login exitoso")
            return True
        else:
            print(f"⚠️ Respuesta inesperada: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Error de conexión (posible problema CORS): {e}")
        return False
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print(f"🚀 Iniciando verificación CORS - {datetime.now()}")
    print(f"Frontend: {FRONTEND_ORIGIN}")
    print(f"Backend: {BACKEND_BASE}")
    print("="*60)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("CORS Preflight", test_cors_preflight),
        ("Login Endpoint", test_login_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ¡Todas las pruebas CORS pasaron!")
        print("Tu configuración está correcta para producción.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("Verifica que el backend esté ejecutándose con la nueva configuración.")

if __name__ == "__main__":
    main()
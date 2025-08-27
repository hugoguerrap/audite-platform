#!/bin/bash

# 🚀 DEPLOY COMPLETO EN RAILWAY - EJECUTAR PASO A PASO

echo "=========================================="
echo "🚀 DEPLOYMENT COMPLETO AUDITE A RAILWAY"
echo "=========================================="
echo ""
echo "IMPORTANTE: Ejecuta estos comandos UNO POR UNO:"
echo ""

# Paso 1: Login
echo "📌 PASO 1 - LOGIN:"
echo "railway login"
echo ""
echo "Presiona ENTER después de hacer login..."
read

# Paso 2: Crear proyecto
echo "📌 PASO 2 - CREAR PROYECTO:"
echo "railway init --name audite-platform"
echo ""
echo "Presiona ENTER después de crear el proyecto..."
read

# Paso 3: Configurar PostgreSQL
echo "📌 PASO 3 - AGREGAR POSTGRESQL:"
echo "railway add --plugin postgresql"
echo ""
echo "Presiona ENTER después de agregar PostgreSQL..."
read

# Paso 4: Configurar variables de entorno
echo "📌 PASO 4 - CONFIGURAR VARIABLES:"
cat << 'EOF' > set_vars.sh
railway variables set SECRET_KEY=$(openssl rand -hex 32)
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)
railway variables set ADMIN_USERNAME=admin
railway variables set ADMIN_PASSWORD=Audite2024SecurePass!
railway variables set NODE_ENV=production
railway variables set PORT=8000
EOF

echo "Ejecuta:"
echo "bash set_vars.sh"
echo ""
echo "Presiona ENTER después de configurar las variables..."
read

# Paso 5: Deploy Backend
echo "📌 PASO 5 - DEPLOY BACKEND:"
echo "cd audite"
echo "railway up"
echo ""
echo "Copia la URL del backend: _________________"
echo "Presiona ENTER después del deploy..."
read

# Paso 6: Deploy Frontend
echo "📌 PASO 6 - DEPLOY FRONTEND:"
echo "cd ../audite-frontend-explorer"
echo "railway up"
echo ""
echo "Copia la URL del frontend: _________________"
echo "Presiona ENTER después del deploy..."
read

# Paso 7: Configurar dominio
echo "📌 PASO 7 - CONFIGURAR DOMINIO EN GODADDY:"
echo ""
echo "1. Ve a GoDaddy DNS Management"
echo "2. Agrega un registro CNAME:"
echo "   Type: CNAME"
echo "   Host: www"
echo "   Points to: [tu-frontend-url].railway.app"
echo "   TTL: 600"
echo ""
echo "3. Para el dominio raíz (@):"
echo "   Type: A"
echo "   Host: @"
echo "   Points to: Usar Cloudflare para redirigir"
echo ""

echo "=========================================="
echo "✅ DEPLOYMENT COMPLETADO!"
echo "=========================================="
echo ""
echo "URLs de tu aplicación:"
echo "Frontend: https://[tu-app].railway.app"
echo "Backend: https://[tu-api].railway.app"
echo ""
echo "Tu dominio estará listo en 5-30 minutos"
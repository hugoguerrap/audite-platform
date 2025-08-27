#!/bin/bash

# Script de deployment rápido para Railway
# Autor: Audite Team
# Fecha: $(date)

echo "🚀 Iniciando deployment a Railway..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Verificar Railway CLI
echo -e "${BLUE}📦 Verificando Railway CLI...${NC}"
if ! command -v railway &> /dev/null; then
    echo -e "${YELLOW}⚠️  Railway CLI no encontrado. Instalando...${NC}"
    npm install -g @railway/cli
fi

# 2. Login a Railway
echo -e "${BLUE}🔐 Iniciando sesión en Railway...${NC}"
railway login

# 3. Crear proyecto si no existe
echo -e "${BLUE}📁 Configurando proyecto...${NC}"
railway link || railway init

# 4. Configurar servicios
echo -e "${GREEN}🔧 Configurando servicios...${NC}"

# Crear servicio de PostgreSQL
echo "Creando servicio PostgreSQL..."
railway add postgresql

# Crear servicio de Redis (opcional)
read -p "¿Necesitas Redis? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    railway add redis
fi

# 5. Configurar variables de entorno
echo -e "${BLUE}⚙️  Configurando variables de entorno...${NC}"
cat <<EOF > railway-env.txt
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_ACCESS_TOKEN_EXPIRES=43200
JWT_REFRESH_TOKEN_EXPIRES=604800
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Audite2024SecurePass!
ADMIN_EMAIL=admin@audite.com
EOF

echo "Variables de entorno configuradas en railway-env.txt"
echo -e "${YELLOW}⚠️  Importante: Configura estas variables en Railway Dashboard${NC}"

# 6. Deploy Backend
echo -e "${GREEN}🚀 Desplegando Backend...${NC}"
cd audite
railway up --service backend
cd ..

# 7. Deploy Frontend
echo -e "${GREEN}🚀 Desplegando Frontend...${NC}"
cd audite-frontend-explorer
railway up --service frontend
cd ..

# 8. Obtener URLs
echo -e "${BLUE}🌐 Obteniendo URLs de los servicios...${NC}"
railway status

# 9. Instrucciones finales
echo -e "${GREEN}✅ Deployment completado!${NC}"
echo
echo -e "${YELLOW}📋 PRÓXIMOS PASOS:${NC}"
echo "1. Ve a Railway Dashboard: https://railway.app/dashboard"
echo "2. Configura las variables de entorno del archivo railway-env.txt"
echo "3. Espera que los servicios estén listos (~2-3 minutos)"
echo "4. Configura tu dominio de GoDaddy:"
echo "   - Backend URL: $(railway status | grep backend | awk '{print $2}')"
echo "   - Frontend URL: $(railway status | grep frontend | awk '{print $2}')"
echo
echo -e "${BLUE}🌐 CONFIGURACIÓN DE DOMINIO EN GODADDY:${NC}"
echo "1. Ve a GoDaddy DNS Management"
echo "2. Agrega un registro CNAME:"
echo "   - Type: CNAME"
echo "   - Host: @ o www"
echo "   - Points to: [tu-app].railway.app"
echo "3. Espera 5-30 minutos para propagación DNS"

# Cleanup
rm -f railway-env.txt
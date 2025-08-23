#!/bin/bash

echo "🚀 CONFIGURANDO ENTORNO DE DESARROLLO AUDITE"
echo "============================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Verificar Docker
echo -e "${BLUE}🐳 Verificando Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no encontrado. Por favor instala Docker Desktop${NC}"
    echo "🔗 https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker no está corriendo. Inicia Docker Desktop${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker disponible${NC}"

# 2. Levantar PostgreSQL con Docker Compose
echo -e "${BLUE}🗄️ Levantando PostgreSQL...${NC}"
docker-compose -f docker-compose.dev.yml up -d postgres_dev

# Esperar a que PostgreSQL esté listo
echo -e "${YELLOW}⏳ Esperando PostgreSQL...${NC}"
for i in {1..30}; do
    if docker-compose -f docker-compose.dev.yml exec -T postgres_dev pg_isready -U audite_user -d audite_dev > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PostgreSQL listo${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# 3. Configurar variables de entorno
echo -e "${BLUE}⚙️ Configurando variables de entorno...${NC}"
if [ ! -f ".env" ]; then
    cp .env.dev .env
    echo -e "${GREEN}✅ Archivo .env creado desde .env.dev${NC}"
else
    echo -e "${YELLOW}⚠️ .env ya existe, usando configuración actual${NC}"
fi

# 4. Instalar dependencias Python
echo -e "${BLUE}🐍 Configurando Python...${NC}"
cd audite

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate
echo -e "${YELLOW}📥 Instalando dependencias...${NC}"
pip install -r requirements.txt

# 5. Ejecutar migraciones limpias
echo -e "${BLUE}🔧 Ejecutando migraciones...${NC}"
export DATABASE_URL="postgresql://audite_user:audite_password_dev@localhost:5433/audite_dev"

# Verificar qué migraciones tenemos
echo -e "${YELLOW}📋 Migraciones disponibles:${NC}"
alembic history --verbose | head -10

# Aplicar migraciones
alembic upgrade head

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migraciones aplicadas exitosamente${NC}"
else
    echo -e "${RED}❌ Error en migraciones${NC}"
    echo -e "${YELLOW}💡 Opciones de solución:${NC}"
    echo "   1. alembic stamp head  # Marcar como aplicadas"
    echo "   2. ./fix_migrations.sh # Script de reparación"
fi

# 6. Crear datos de prueba (opcional)
echo -e "${BLUE}📊 ¿Cargar datos de prueba? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python scripts/create_test_data.py 2>/dev/null || echo -e "${YELLOW}⚠️ Script de datos de prueba no encontrado${NC}"
fi

cd ..

# 7. Mostrar información final
echo ""
echo -e "${GREEN}🎉 ¡SETUP COMPLETO!${NC}"
echo "================================="
echo -e "${BLUE}📍 URLs importantes:${NC}"
echo "   🗄️ PostgreSQL: localhost:5433"
echo "   🌐 Adminer:    http://localhost:8080"
echo "   🚀 API:        http://localhost:8000"
echo ""
echo -e "${BLUE}🔧 Comandos útiles:${NC}"
echo "   Iniciar API:    cd audite && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   Ver logs DB:    docker-compose -f docker-compose.dev.yml logs -f postgres_dev"
echo "   Parar todo:     docker-compose -f docker-compose.dev.yml down"
echo ""
echo -e "${BLUE}🗄️ Acceso a PostgreSQL:${NC}"
echo "   Host: localhost:5433"
echo "   DB: audite_dev"
echo "   User: audite_user"
echo "   Pass: audite_password_dev"
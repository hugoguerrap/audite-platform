#!/bin/bash

# 🔍 VALIDACIÓN RÁPIDA CON NUEVOS PUERTOS

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}🔍 VALIDACIÓN STACK AUDITE - PUERTOS ALTOS${NC}"
echo "=============================================="

# URLs con nuevos puertos
POSTGRES_URL="localhost:15432"
BACKEND_URL="http://localhost:18000"  
FRONTEND_URL="http://localhost:18080"
ADMINER_URL="http://localhost:18081"

echo -e "${BLUE}📍 URLs configuradas:${NC}"
echo -e "   🗄️ PostgreSQL:   $POSTGRES_URL"
echo -e "   🚀 Backend:      $BACKEND_URL"
echo -e "   🌐 Frontend:     $FRONTEND_URL"  
echo -e "   🗄️ Adminer:      $ADMINER_URL"
echo ""

# Check servicios Docker
echo -e "${BLUE}🐳 Verificando servicios Docker...${NC}"
docker-compose -f docker-compose.testing.yml ps

echo ""
echo -e "${BLUE}📊 Estado de salud:${NC}"

# Test PostgreSQL
echo -n -e "${BLUE}🗄️ PostgreSQL:${NC} "
if docker-compose -f docker-compose.testing.yml exec -T postgres pg_isready -U audite_user -d audite_test > /dev/null 2>&1; then
    echo -e "${GREEN}✅ LISTO${NC}"
else
    echo -e "${RED}❌ NO RESPONDE${NC}"
fi

# Test Backend
echo -n -e "${BLUE}🚀 Backend:${NC} "
if curl -f -s $BACKEND_URL/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ LISTO${NC}"
else
    echo -e "${YELLOW}⏳ INICIANDO...${NC}"
fi

# Test Frontend  
echo -n -e "${BLUE}🌐 Frontend:${NC} "
if curl -f -s $FRONTEND_URL > /dev/null 2>&1; then
    echo -e "${GREEN}✅ LISTO${NC}"
else
    echo -e "${YELLOW}⏳ INICIANDO...${NC}"
fi

# Test Adminer
echo -n -e "${BLUE}🗄️ Adminer:${NC} "
if curl -f -s $ADMINER_URL > /dev/null 2>&1; then
    echo -e "${GREEN}✅ LISTO${NC}"
else
    echo -e "${YELLOW}⏳ INICIANDO...${NC}"
fi

echo ""
echo -e "${BLUE}🔧 Comandos útiles:${NC}"
echo -e "   Ver logs:         ${YELLOW}docker-compose -f docker-compose.testing.yml logs -f${NC}"
echo -e "   Estado servicios: ${YELLOW}docker-compose -f docker-compose.testing.yml ps${NC}"
echo -e "   Parar todo:       ${YELLOW}docker-compose -f docker-compose.testing.yml down${NC}"

echo ""
echo -e "${BLUE}🔐 Credenciales Admin:${NC}"
echo -e "   URL:  ${GREEN}$FRONTEND_URL/admin${NC}"
echo -e "   User: ${YELLOW}admin_audite${NC}"
echo -e "   Pass: ${YELLOW}AuditE2024!SecureAdmin#2024${NC}"

echo ""
echo -e "${BLUE}🗄️ Acceso BD (Adminer):${NC}"
echo -e "   URL:  ${GREEN}$ADMINER_URL${NC}"
echo -e "   Host: ${YELLOW}postgres${NC}"
echo -e "   DB:   ${YELLOW}audite_test${NC}"
echo -e "   User: ${YELLOW}audite_user${NC}"
echo -e "   Pass: ${YELLOW}audite_password_test_2024${NC}"
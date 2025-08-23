#!/bin/bash

# ============================================
# ✅ AUDITE - VALIDACIÓN RÁPIDA DEL STACK
# ============================================

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_test() {
    echo -n -e "${BLUE}Testing $1...${NC} "
}

print_ok() {
    echo -e "${GREEN}OK${NC}"
}

print_fail() {
    echo -e "${RED}FAIL${NC}"
}

echo -e "${YELLOW}🔍 VALIDACIÓN RÁPIDA DEL STACK AUDITE${NC}"
echo "========================================"

# 1. Verificar servicios Docker
print_test "Docker services"
if docker-compose -f docker-compose.testing.yml ps | grep -q "Up"; then
    print_ok
    echo -e "   Servicios activos: $(docker-compose -f docker-compose.testing.yml ps --services --filter status=running | wc -l)"
else
    print_fail
    echo -e "   ${RED}No hay servicios corriendo${NC}"
    exit 1
fi

# 2. Test PostgreSQL
print_test "PostgreSQL connection"
if docker-compose -f docker-compose.testing.yml exec -T postgres pg_isready -U audite_user -d audite_test > /dev/null 2>&1; then
    print_ok
else
    print_fail
    echo -e "   ${RED}PostgreSQL no responde${NC}"
fi

# 3. Test Backend Health
print_test "Backend health check"
if curl -f -s http://localhost:8000/health > /dev/null; then
    print_ok
else
    print_fail
    echo -e "   ${RED}Backend no responde en :8000${NC}"
fi

# 4. Test Frontend
print_test "Frontend availability"
if curl -f -s http://localhost:8080 > /dev/null; then
    print_ok
else
    print_fail
    echo -e "   ${RED}Frontend no responde en :8080${NC}"
fi

# 5. Test API Endpoints
print_test "API endpoints"
endpoints_ok=0
total_endpoints=0

# Test categorías
if curl -f -s http://localhost:8000/api/categorias-industria > /dev/null; then
    ((endpoints_ok++))
fi
((total_endpoints++))

# Test autodiagnóstico
if curl -f -s http://localhost:8000/autodiagnostico/preguntas > /dev/null; then
    ((endpoints_ok++))
fi
((total_endpoints++))

# Test docs
if curl -f -s http://localhost:8000/docs > /dev/null; then
    ((endpoints_ok++))
fi
((total_endpoints++))

if [ $endpoints_ok -eq $total_endpoints ]; then
    print_ok
    echo -e "   Endpoints funcionando: $endpoints_ok/$total_endpoints"
else
    print_fail
    echo -e "   ${YELLOW}Endpoints funcionando: $endpoints_ok/$total_endpoints${NC}"
fi

# 6. Test Admin Authentication
print_test "Admin authentication"
ADMIN_RESPONSE=$(curl -s -X POST http://localhost:8000/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin_audite", "password": "AuditE2024!SecureAdmin#2024"}' 2>/dev/null)

if echo "$ADMIN_RESPONSE" | grep -q "access_token"; then
    print_ok
else
    print_fail
    echo -e "   ${RED}Admin login falló${NC}"
fi

# 7. Test Database Data
print_test "Database test data"
DATA_CHECK=$(docker-compose -f docker-compose.testing.yml exec -T postgres psql -U audite_user -d audite_test -t -c "
SELECT 
    (SELECT COUNT(*) FROM categorias_industria) as categorias,
    (SELECT COUNT(*) FROM autodiagnostico_preguntas) as preguntas
" 2>/dev/null)

if echo "$DATA_CHECK" | grep -q -E "[0-9]+.*[0-9]+"; then
    print_ok
    CATEGORIAS=$(echo "$DATA_CHECK" | tr -d ' ' | cut -d'|' -f1)
    PREGUNTAS=$(echo "$DATA_CHECK" | tr -d ' ' | cut -d'|' -f2)
    echo -e "   Categorías: $CATEGORIAS | Preguntas: $PREGUNTAS"
else
    print_fail
    echo -e "   ${RED}No se pudieron verificar datos${NC}"
fi

echo ""
echo -e "${GREEN}🎯 RESUMEN DE LA VALIDACIÓN${NC}"
echo "=========================="

# URLs principales
echo -e "${BLUE}📍 URLs principales:${NC}"
echo -e "   Frontend:    http://localhost:8080"
echo -e "   Backend API: http://localhost:8000"
echo -e "   API Docs:    http://localhost:8000/docs"
echo -e "   Admin:       http://localhost:8080/admin"
echo -e "   Adminer:     http://localhost:8081"

# Credenciales
echo -e "${BLUE}🔐 Admin credentials:${NC}"
echo -e "   User: admin_audite"
echo -e "   Pass: AuditE2024!SecureAdmin#2024"

# Tests adicionales recomendados
echo -e "${BLUE}🧪 Tests manuales recomendados:${NC}"
echo -e "   1. Crear nueva categoría de industria desde admin"
echo -e "   2. Completar autodiagnóstico desde frontend"
echo -e "   3. Probar formulario especializado"
echo -e "   4. Verificar respuestas en admin panel"

# Estado final
if curl -f -s http://localhost:8000/health > /dev/null && curl -f -s http://localhost:8080 > /dev/null; then
    echo -e "${GREEN}✅ Stack completamente funcional${NC}"
    exit 0
else
    echo -e "${RED}❌ Algunos servicios tienen problemas${NC}"
    exit 1
fi
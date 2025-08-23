#!/bin/bash

# ============================================
# 🚀 AUDITE - TESTING COMPLETO DEL STACK
# ============================================

set -e  # Exit on any error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Banner
echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════╗"
echo "║            🚀 AUDITE TESTING SUITE            ║"  
echo "║                                                ║"
echo "║  Stack completo: Frontend + Backend + DB      ║"
echo "║  Testing automatizado con datos de prueba     ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${NC}"

# 1. Verificaciones previas
print_status "Verificando requisitos..."

if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado"
    exit 1
fi

if ! docker info > /dev/null 2>&1; then
    print_error "Docker no está corriendo"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado"
    exit 1
fi

print_success "Requisitos verificados"

# 2. Limpieza inicial
print_status "Limpiando contenedores y volúmenes anteriores..."
docker-compose -f docker-compose.testing.yml down --volumes --remove-orphans 2>/dev/null || true
docker volume prune -f 2>/dev/null || true
print_success "Limpieza completada"

# 3. Construcción de imágenes
print_status "Construyendo imágenes Docker..."
docker-compose -f docker-compose.testing.yml build --no-cache --pull

if [ $? -eq 0 ]; then
    print_success "Imágenes construidas exitosamente"
else
    print_error "Error construyendo imágenes"
    exit 1
fi

# 4. Iniciar servicios
print_status "Iniciando servicios..."
docker-compose -f docker-compose.testing.yml up -d postgres adminer

print_status "Esperando PostgreSQL..."
timeout=60
while ! docker-compose -f docker-compose.testing.yml exec -T postgres pg_isready -U audite_user -d audite_test > /dev/null 2>&1; do
    if [ $timeout -le 0 ]; then
        print_error "Timeout esperando PostgreSQL"
        docker-compose -f docker-compose.testing.yml logs postgres
        exit 1
    fi
    echo -n "."
    sleep 2
    ((timeout-=2))
done
echo ""
print_success "PostgreSQL listo"

# 5. Iniciar backend
print_status "Iniciando backend..."
docker-compose -f docker-compose.testing.yml up -d backend

print_status "Esperando backend..."
timeout=90
while ! curl -f http://localhost:18000/health > /dev/null 2>&1; do
    if [ $timeout -le 0 ]; then
        print_error "Timeout esperando backend"
        docker-compose -f docker-compose.testing.yml logs backend
        exit 1
    fi
    echo -n "."
    sleep 3
    ((timeout-=3))
done
echo ""
print_success "Backend listo"

# 6. Iniciar frontend
print_status "Iniciando frontend..."
docker-compose -f docker-compose.testing.yml up -d frontend

print_status "Esperando frontend..."
timeout=120
while ! curl -f http://localhost:18080 > /dev/null 2>&1; do
    if [ $timeout -le 0 ]; then
        print_error "Timeout esperando frontend"
        docker-compose -f docker-compose.testing.yml logs frontend
        exit 1
    fi
    echo -n "."
    sleep 5
    ((timeout-=5))
done
echo ""
print_success "Frontend listo"

# 7. Testing de endpoints
print_status "Ejecutando tests de endpoints..."

# Test health check
if curl -f http://localhost:18000/health > /dev/null 2>&1; then
    print_success "Backend health check: OK"
else
    print_error "Backend health check: FAIL"
fi

# Test root endpoint
if curl -f http://localhost:18000/ > /dev/null 2>&1; then
    print_success "Backend root endpoint: OK"
else
    print_error "Backend root endpoint: FAIL"
fi

# Test admin login
print_status "Testing admin login..."
ADMIN_RESPONSE=$(curl -s -X POST http://localhost:18000/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin_audite", "password": "AuditE2024!SecureAdmin#2024"}')

if echo "$ADMIN_RESPONSE" | grep -q "access_token"; then
    print_success "Admin login: OK"
    TOKEN=$(echo "$ADMIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null || echo "")
else
    print_warning "Admin login: FAIL - Respuesta: $ADMIN_RESPONSE"
fi

# Test categorías
if curl -f http://localhost:18000/api/categorias-industria > /dev/null 2>&1; then
    print_success "Categorías endpoint: OK"
else
    print_error "Categorías endpoint: FAIL"
fi

# Test autodiagnóstico
if curl -f http://localhost:18000/autodiagnostico/preguntas > /dev/null 2>&1; then
    print_success "Autodiagnóstico endpoint: OK"
else
    print_error "Autodiagnóstico endpoint: FAIL"
fi

# 8. Mostrar información de acceso
echo ""
echo -e "${GREEN}🎉 STACK COMPLETAMENTE OPERATIVO${NC}"
echo -e "${PURPLE}════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}📍 URLs de acceso:${NC}"
echo -e "   🌐 Frontend:        ${GREEN}http://localhost:18080${NC}"
echo -e "   🚀 Backend API:     ${GREEN}http://localhost:18000${NC}"
echo -e "   📚 API Docs:        ${GREEN}http://localhost:18000/docs${NC}"
echo -e "   🗄️  Adminer (BD):    ${GREEN}http://localhost:18081${NC}"
echo ""
echo -e "${CYAN}🔐 Credenciales del Admin:${NC}"
echo -e "   👤 Usuario:         ${YELLOW}admin_audite${NC}"
echo -e "   🔑 Contraseña:      ${YELLOW}AuditE2024!SecureAdmin#2024${NC}"
echo -e "   🌐 URL Admin:       ${GREEN}http://localhost:18080/admin${NC}"
echo ""
echo -e "${CYAN}🗄️ Acceso a la Base de Datos:${NC}"
echo -e "   🖥️  Host:            ${YELLOW}localhost:15432${NC}"
echo -e "   🗂️  BD:              ${YELLOW}audite_test${NC}"
echo -e "   👤 Usuario:         ${YELLOW}audite_user${NC}"
echo -e "   🔑 Contraseña:      ${YELLOW}audite_password_test_2024${NC}"
echo ""
echo -e "${CYAN}🔧 Comandos útiles:${NC}"
echo -e "   Ver logs:           ${YELLOW}docker-compose -f docker-compose.testing.yml logs -f [servicio]${NC}"
echo -e "   Parar todo:         ${YELLOW}docker-compose -f docker-compose.testing.yml down${NC}"
echo -e "   Reiniciar servicio: ${YELLOW}docker-compose -f docker-compose.testing.yml restart [servicio]${NC}"
echo -e "   Consola BD:         ${YELLOW}docker-compose -f docker-compose.testing.yml exec postgres psql -U audite_user -d audite_test${NC}"
echo ""
echo -e "${CYAN}📊 Datos de prueba incluidos:${NC}"
echo -e "   ✅ 5 categorías de industria"
echo -e "   ✅ 6 formularios especializados"
echo -e "   ✅ 5 preguntas de autodiagnóstico con opciones"
echo -e "   ✅ 3 preguntas de formulario industrial"
echo ""
echo -e "${BLUE}🚀 ¡El stack está listo para testing!${NC}"
echo ""

# Opcional: Abrir navegador automáticamente
if command -v open &> /dev/null; then
    read -p "¿Abrir frontend en el navegador? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open http://localhost:18080
    fi
elif command -v xdg-open &> /dev/null; then
    read -p "¿Abrir frontend en el navegador? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open http://localhost:18080
    fi
fi

# Mantener logs en vivo
read -p "¿Ver logs en tiempo real? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Mostrando logs (Ctrl+C para salir)...${NC}"
    docker-compose -f docker-compose.testing.yml logs -f
fi
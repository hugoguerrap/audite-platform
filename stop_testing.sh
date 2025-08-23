#!/bin/bash

# ============================================
# 🛑 AUDITE - DETENER STACK DE TESTING
# ============================================

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

echo -e "${YELLOW}"
echo "╔════════════════════════════════════════════════╗"
echo "║         🛑 DETENIENDO STACK DE TESTING        ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${NC}"

# Obtener opción del usuario
echo "Seleccione una opción:"
echo "1) Detener servicios (mantener datos)"
echo "2) Detener y limpiar todo (eliminar datos)"
echo "3) Solo mostrar estado"
echo ""
read -p "Opción [1-3]: " option

case $option in
    1)
        print_status "Deteniendo servicios..."
        docker-compose -f docker-compose.testing.yml down
        print_success "Servicios detenidos (datos conservados)"
        ;;
    2)
        print_status "Deteniendo servicios y limpiando datos..."
        docker-compose -f docker-compose.testing.yml down --volumes --remove-orphans
        
        # Limpiar imágenes huérfanas
        print_status "Limpiando imágenes no utilizadas..."
        docker image prune -f > /dev/null 2>&1
        
        # Limpiar volúmenes no utilizados
        print_status "Limpiando volúmenes no utilizados..."
        docker volume prune -f > /dev/null 2>&1
        
        print_success "Stack completamente limpiado"
        ;;
    3)
        print_status "Estado actual del stack:"
        echo ""
        echo -e "${YELLOW}Servicios activos:${NC}"
        docker-compose -f docker-compose.testing.yml ps
        echo ""
        echo -e "${YELLOW}Volúmenes:${NC}"
        docker volume ls | grep audite || echo "No hay volúmenes de audite"
        echo ""
        echo -e "${YELLOW}Imágenes:${NC}"
        docker images | grep audite || echo "No hay imágenes de audite"
        ;;
    *)
        print_status "Opción inválida"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}🔧 Comandos útiles:${NC}"
echo -e "   Reiniciar:    ${YELLOW}./run_full_testing.sh${NC}"
echo -e "   Solo backend: ${YELLOW}docker-compose -f docker-compose.testing.yml up -d backend${NC}"
echo -e "   Solo frontend:${YELLOW}docker-compose -f docker-compose.testing.yml up -d frontend${NC}"
echo -e "   Ver logs:     ${YELLOW}docker-compose -f docker-compose.testing.yml logs -f${NC}"
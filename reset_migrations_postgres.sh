#!/bin/bash

echo "🔄 RESET LIMPIO DE MIGRACIONES CON POSTGRESQL"
echo "============================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 1. Verificar Docker y levantar PostgreSQL si no está corriendo
echo -e "${BLUE}🐳 Verificando PostgreSQL...${NC}"
if ! docker ps | grep -q audite_postgres_dev; then
    echo -e "${YELLOW}📦 Levantando PostgreSQL...${NC}"
    docker-compose -f docker-compose.dev.yml up -d postgres_dev
    
    # Esperar a que esté listo
    echo -e "${YELLOW}⏳ Esperando PostgreSQL...${NC}"
    for i in {1..20}; do
        if docker-compose -f docker-compose.dev.yml exec -T postgres_dev pg_isready -U audite_user -d audite_dev > /dev/null 2>&1; then
            break
        fi
        echo -n "."
        sleep 1
    done
    echo ""
fi

# 2. Configurar entorno
cd audite
export DATABASE_URL="postgresql://audite_user:audite_password_dev@localhost:5433/audite_dev"
export ENVIRONMENT="development"

# Activar venv si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Entorno virtual activado${NC}"
fi

# 3. Limpiar base de datos completamente
echo -e "${BLUE}🧹 Limpiando base de datos...${NC}"
docker-compose -f ../docker-compose.dev.yml exec -T postgres_dev psql -U audite_user -d audite_dev -c "
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO audite_user;
    GRANT ALL ON SCHEMA public TO public;
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de datos limpia${NC}"
else
    echo -e "${RED}❌ Error limpiando base de datos${NC}"
    exit 1
fi

# 4. Aplicar migraciones limpias
echo -e "${BLUE}🚀 Aplicando migraciones...${NC}"
alembic upgrade head

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migraciones aplicadas exitosamente${NC}"
else
    echo -e "${RED}❌ Error aplicando migraciones${NC}"
    echo -e "${YELLOW}🔍 Verificando estado...${NC}"
    alembic current
    alembic heads
    exit 1
fi

# 5. Verificar estado final
echo -e "${BLUE}📊 Estado final:${NC}"
alembic current
echo ""

# 6. Crear datos de prueba básicos
echo -e "${BLUE}📊 ¿Crear datos de prueba básicos? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python -c "
from app.database import SessionLocal, engine
from app.models import CategoriaIndustria, FormularioIndustria, AutodiagnosticoPregunta, AutodiagnosticoOpcion
from sqlalchemy.orm import Session

db = SessionLocal()

try:
    # Crear categoría de ejemplo
    if not db.query(CategoriaIndustria).first():
        categoria = CategoriaIndustria(
            nombre='Industrial',
            descripcion='Sector industrial general',
            icono='🏭',
            color='#3b82f6',
            orden=1
        )
        db.add(categoria)
        db.commit()
        print('✅ Categoría de ejemplo creada')
    
    # Crear pregunta de autodiagnóstico básica
    if not db.query(AutodiagnosticoPregunta).first():
        pregunta = AutodiagnosticoPregunta(
            numero_orden=1,
            pregunta='¿Cuál es el sector de tu empresa?',
            tipo_respuesta='radio',
            es_obligatoria=True
        )
        db.add(pregunta)
        db.flush()
        
        # Opciones
        opciones = [
            AutodiagnosticoOpcion(pregunta_id=pregunta.id, texto_opcion='Industrial', valor='industrial', orden=1),
            AutodiagnosticoOpcion(pregunta_id=pregunta.id, texto_opcion='Comercial', valor='comercial', orden=2),
            AutodiagnosticoOpcion(pregunta_id=pregunta.id, texto_opcion='Servicios', valor='servicios', orden=3),
        ]
        db.add_all(opciones)
        db.commit()
        print('✅ Pregunta de ejemplo creada')
        
except Exception as e:
    print(f'❌ Error creando datos: {e}')
finally:
    db.close()
"
fi

echo ""
echo -e "${GREEN}🎉 ¡RESET COMPLETADO CON POSTGRESQL!${NC}"
echo "===================================="
echo -e "${BLUE}📍 Información:${NC}"
echo "   🗄️ Base de datos: PostgreSQL (audite_dev)"
echo "   🌐 Acceso:       localhost:5433"
echo "   📊 Adminer:      http://localhost:8080"
echo ""
echo -e "${BLUE}▶️ Próximos pasos:${NC}"
echo "   1. Iniciar API: uvicorn app.main:app --reload"
echo "   2. Probar endpoints en http://localhost:8000/docs"
echo "   3. Frontend en el puerto correspondiente"
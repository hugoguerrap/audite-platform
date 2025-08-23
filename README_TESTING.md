# 🚀 AUDITE - STACK COMPLETO DE TESTING

## 🎯 DESCRIPCIÓN

Stack completo Docker con **PostgreSQL + FastAPI + React** para testing y desarrollo de la plataforma AUDITE.

### **Incluye:**
- ✅ **Base de datos PostgreSQL** con datos de prueba
- ✅ **Backend FastAPI** con todas las APIs
- ✅ **Frontend React** con interfaz completa
- ✅ **Panel de administración** funcional
- ✅ **Datos de prueba** precargados
- ✅ **Adminer** para gestionar la BD
- ✅ **Scripts automatizados** de testing

---

## 🚀 INICIO RÁPIDO

### **1. Levantar todo el stack:**
```bash
./run_full_testing.sh
```

### **2. Acceder a la aplicación:**
- **Frontend:** http://localhost:8080
- **Admin Panel:** http://localhost:8080/admin
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Adminer (BD):** http://localhost:8081

### **3. Credenciales del Admin:**
- **Usuario:** `admin_audite`
- **Contraseña:** `AuditE2024!SecureAdmin#2024`

---

## 📋 COMANDOS PRINCIPALES

| Comando | Descripción |
|---------|-------------|
| `./run_full_testing.sh` | Inicia todo el stack completo |
| `./quick_test.sh` | Validación rápida de servicios |
| `./stop_testing.sh` | Detiene servicios (con opciones) |
| `docker-compose -f docker-compose.testing.yml logs -f` | Ver logs en tiempo real |
| `docker-compose -f docker-compose.testing.yml restart [servicio]` | Reiniciar un servicio |

---

## 🗄️ SERVICIOS INCLUIDOS

### **🐘 PostgreSQL Database**
- **Puerto:** 5432
- **Base de datos:** `audite_test`
- **Usuario:** `audite_user`
- **Contraseña:** `audite_password_test_2024`

### **🚀 Backend FastAPI**
- **Puerto:** 8000
- **Health check:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs
- **Migraciones:** Ejecutadas automáticamente

### **⚛️ Frontend React**
- **Puerto:** 8080
- **Vite dev server** con hot reload
- **TypeScript** habilitado
- **Tailwind CSS** configurado

### **🗄️ Adminer**
- **Puerto:** 8081
- **Acceso directo** a PostgreSQL
- **Interfaz web** para gestionar BD

---

## 📊 DATOS DE PRUEBA INCLUIDOS

### **Categorías de Industria:**
- Industrial (🏭)
- Comercial (🏢)
- Agropecuario (🚜)
- Servicios (💼)
- Hospitalario (🏥)

### **Formularios:**
- 6 formularios especializados por categoría
- Preguntas con lógica condicional
- Campos "Otro" personalizables

### **Autodiagnóstico:**
- 5 preguntas básicas con opciones
- Sugerencias personalizadas por respuesta
- Sistema de puntuación implementado

---

## 🧪 TESTING MANUAL

### **1. Testing del Frontend:**
```bash
# Navegar a http://localhost:8080
# ✅ Probar autodiagnóstico básico
# ✅ Seleccionar categoría de industria
# ✅ Completar formulario especializado
# ✅ Verificar navegación entre páginas
```

### **2. Testing del Admin Panel:**
```bash
# Navegar a http://localhost:8080/admin
# ✅ Login con credenciales
# ✅ Crear nueva categoría
# ✅ Diseñar formulario personalizado
# ✅ Añadir preguntas condicionales
# ✅ Ver respuestas de usuarios
```

### **3. Testing de APIs:**
```bash
# Endpoints principales
curl http://localhost:8000/health
curl http://localhost:8000/api/categorias-industria
curl http://localhost:8000/autodiagnostico/preguntas

# Admin login
curl -X POST http://localhost:8000/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin_audite", "password": "AuditE2024!SecureAdmin#2024"}'
```

---

## 🔧 DESARROLLO

### **Modificar código en vivo:**
Los volúmenes están configurados para desarrollo:
- Cambios en `./audite/app/` se reflejan automáticamente
- Cambios en `./audite-frontend-explorer/src/` activan hot reload
- Cambios en migraciones requieren reinicio del backend

### **Ver logs:**
```bash
# Todos los servicios
docker-compose -f docker-compose.testing.yml logs -f

# Servicio específico
docker-compose -f docker-compose.testing.yml logs -f backend
docker-compose -f docker-compose.testing.yml logs -f frontend
docker-compose -f docker-compose.testing.yml logs -f postgres
```

### **Acceso a la base de datos:**
```bash
# Consola PostgreSQL
docker-compose -f docker-compose.testing.yml exec postgres psql -U audite_user -d audite_test

# Via Adminer (más fácil)
# http://localhost:8081
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### **El stack no inicia:**
```bash
# Verificar Docker
docker info

# Limpiar completamente
./stop_testing.sh  # Opción 2
docker system prune -f

# Reiniciar
./run_full_testing.sh
```

### **Backend no responde:**
```bash
# Ver logs del backend
docker-compose -f docker-compose.testing.yml logs backend

# Verificar migraciones
docker-compose -f docker-compose.testing.yml exec backend alembic current

# Reiniciar solo backend
docker-compose -f docker-compose.testing.yml restart backend
```

### **Frontend no carga:**
```bash
# Ver logs del frontend
docker-compose -f docker-compose.testing.yml logs frontend

# Reinstalar dependencias
docker-compose -f docker-compose.testing.yml exec frontend npm install

# Reiniciar solo frontend
docker-compose -f docker-compose.testing.yml restart frontend
```

### **Base de datos con problemas:**
```bash
# Verificar estado
docker-compose -f docker-compose.testing.yml exec postgres pg_isready -U audite_user

# Recrear datos
docker-compose -f docker-compose.testing.yml down --volumes
./run_full_testing.sh
```

---

## 📈 MÉTRICAS Y MONITORING

### **Health Checks Incluidos:**
- **PostgreSQL:** `pg_isready` cada 5s
- **Backend:** `curl /health` cada 10s  
- **Frontend:** `curl localhost:3000` cada 15s

### **Logs Centralizados:**
Opcional: Activar con `--profile monitoring`
```bash
docker-compose -f docker-compose.testing.yml --profile monitoring up -d
# Ver logs en: http://localhost:8082
```

---

## 🔄 COMPARACIÓN CON OTROS SETUPS

| Feature | `docker-compose.testing.yml` | `docker-compose.full.yml` | Desarrollo local |
|---------|------------------------------|---------------------------|------------------|
| **Setup tiempo** | ⚡ 2-3 min | 🔄 5-8 min | ⏰ 15-30 min |
| **Datos de prueba** | ✅ Incluidos | ⚠️ Básicos | ❌ Manual |
| **Hot reload** | ✅ Completo | ✅ Completo | ✅ Nativo |
| **Aislamiento** | ✅ Completo | ✅ Completo | ⚠️ Parcial |
| **Limpieza** | ✅ Un comando | 🔄 Manual | ❌ Compleja |
| **PostgreSQL** | ✅ Optimizado | ✅ Básico | ⚠️ Instalación local |

---

## 💡 CASOS DE USO RECOMENDADOS

### **🧪 Testing Completo:**
```bash
./run_full_testing.sh
# Perfecto para QA, demos, validación completa
```

### **🔄 Desarrollo Iterativo:**
```bash
# Solo cambios de código (sin cambios de BD)
docker-compose -f docker-compose.testing.yml up -d
# Modificar código en vivo
```

### **🗄️ Testing de Migraciones:**
```bash
# Limpiar y probar migración desde cero
./stop_testing.sh  # Opción 2
./run_full_testing.sh
```

### **📊 Demo para Clientes:**
```bash
# Stack completo con datos realistas
./run_full_testing.sh
# Abrir http://localhost:8080
```

---

## ⚙️ CONFIGURACIÓN AVANZADA

### **Variables de Entorno:**
Modificar en `docker-compose.testing.yml`:
```yaml
environment:
  - DATABASE_URL=postgresql://...
  - ADMIN_PASSWORD=tu_password_personalizada
  - LOG_LEVEL=DEBUG  # INFO, WARNING, ERROR
  - CORS_ORIGINS=http://localhost:3000,...
```

### **Puertos Personalizados:**
```yaml
ports:
  - "8001:8000"  # Backend en puerto 8001
  - "3001:3000"  # Frontend en puerto 3001
  - "5433:5432"  # PostgreSQL en puerto 5433
```

### **Volúmenes Adicionales:**
```yaml
volumes:
  - ./custom_data:/app/data
  - ./logs:/app/logs
```

---

## 📞 SOPORTE

### **Archivos de Configuración:**
- `docker-compose.testing.yml` - Stack principal
- `init_test_data.sql` - Datos de prueba
- `nginx-testing.conf` - Proxy reverso
- `run_full_testing.sh` - Script principal

### **Logs Importantes:**
- Backend: `/app/logs/` (si configurado)
- Frontend: Console del navegador
- PostgreSQL: Docker logs

### **Comandos de Diagnóstico:**
```bash
./quick_test.sh                    # Validación rápida
docker-compose ps                  # Estado de servicios  
docker-compose logs [servicio]     # Logs específicos
docker system df                   # Uso de espacio
```

---

## 🎉 ¡LISTO PARA TESTING!

El stack está completamente configurado y listo para usar. Todos los servicios se levantan automáticamente con datos de prueba incluidos.

**¿Problemas?** Ejecuta `./quick_test.sh` para diagnosticar o revisa los logs de cada servicio.
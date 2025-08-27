# 🚀 INSTRUCCIONES DE DEPLOYMENT RÁPIDO - RAILWAY

## ⏱️ Tiempo estimado: 30 minutos

### PASO 1: Ejecutar el script automático
```bash
./deploy-railway.sh
```

### PASO 2: Configuración Manual en Railway Dashboard

1. Ve a https://railway.app/dashboard
2. Selecciona tu proyecto
3. Ve a "Variables" y agrega:
   - `PORT`: 8000 (para el backend)
   - `NODE_ENV`: production
   - Las variables del archivo `.env.railway`

### PASO 3: Configurar Dominio en GoDaddy

#### Opción A: Subdominio (api.tudominio.com)
1. Ve a DNS Management en GoDaddy
2. Agrega registro CNAME:
   - Type: **CNAME**
   - Host: **api**
   - Points to: **tu-backend.railway.app**
   - TTL: **600 seconds**

#### Opción B: Dominio principal (tudominio.com)
1. Agrega registro A:
   - Type: **A**
   - Host: **@**
   - Points to: IP de Railway (ver dashboard)
   - TTL: **600 seconds**

### PASO 4: Verificar Deployment

```bash
# Verificar backend
curl https://tu-backend.railway.app/health

# Verificar frontend
curl https://tu-frontend.railway.app
```

## 📱 URLs Finales

- **Frontend**: https://tudominio.com
- **Backend API**: https://api.tudominio.com
- **Admin Panel**: https://tudominio.com/admin

## 🔐 Credenciales Admin

- Usuario: `admin`
- Password: `Audite2024SecurePass!`

## ⚠️ IMPORTANTE PARA MAÑANA

1. **SSL**: Railway proporciona HTTPS automático
2. **Propagación DNS**: Puede tomar 5-30 minutos
3. **Monitoreo**: Railway Dashboard muestra logs en tiempo real
4. **Rollback**: Si algo falla, Railway permite rollback instantáneo

## 🆘 Troubleshooting Rápido

### Si el dominio no funciona:
```bash
# Verificar propagación DNS
nslookup tudominio.com
dig tudominio.com
```

### Si la API no responde:
```bash
# Ver logs en Railway
railway logs --service backend
```

### Si necesitas hacer cambios rápidos:
```bash
# Deploy rápido
railway up
```

## 📞 Soporte de Emergencia

- Railway Status: https://status.railway.app
- Railway Discord: https://discord.gg/railway
- GoDaddy Support: 24/7 disponible
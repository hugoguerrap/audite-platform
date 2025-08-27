# 🚀 DEPLOY RÁPIDO EN GCP - 15 MINUTOS

## 💰 Costo: GRATIS con tu crédito ($290K es suficiente para AÑOS)
- VM e2-micro: $5/mes (o GRATIS con free tier)
- IP estática: $2.88/mes
- **Total: ~$8/mes = 3 AÑOS GRATIS con tu crédito**

## 📋 PASOS RÁPIDOS:

### 1️⃣ **Crear VM desde la Consola GCP (5 min)**

1. Ve a: https://console.cloud.google.com/compute/instances
2. Click **"CREATE INSTANCE"**
3. Configuración:
   - **Name**: audite-vm
   - **Region**: us-central1 (Iowa)
   - **Machine type**: e2-micro (en Series E2)
   - **Boot disk**: 
     - Ubuntu 22.04 LTS
     - 30 GB Standard persistent disk
   - **Firewall**: ✅ Allow HTTP ✅ Allow HTTPS
4. Click **"CREATE"**

### 2️⃣ **Obtener IP Estática (2 min)**

1. Ve a: VPC network → IP addresses
2. Click **"RESERVE EXTERNAL STATIC ADDRESS"**
3. Name: audite-ip
4. Attach to: audite-vm
5. **COPIA LA IP**: _____________

### 3️⃣ **Conectar por SSH (1 min)**

En la consola GCP, click en **"SSH"** al lado de tu VM

### 4️⃣ **Ejecutar Script de Setup (5 min)**

Copia y pega estos comandos en SSH:

```bash
# Descargar script de setup
curl -O https://raw.githubusercontent.com/tu-usuario/audite/main/setup-vm.sh

# O crear el script manualmente:
cat > setup.sh << 'EOF'
#!/bin/bash
# Instalar Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clonar tu proyecto (CAMBIA ESTO A TU REPO)
git clone https://github.com/TU_USUARIO/audite-complete.git
cd audite-complete

# Crear docker-compose.yml production
cat > docker-compose.yml << 'COMPOSE'
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: audite
      POSTGRES_USER: audite_user
      POSTGRES_PASSWORD: audite_password_2024
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    build: ./audite
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://audite_user:audite_password_2024@postgres:5432/audite
      SECRET_KEY: your-secret-key-here
    depends_on:
      - postgres
    restart: always

  frontend:
    build: ./audite-frontend-explorer
    ports:
      - "80:5173"
    environment:
      VITE_API_URL: http://YOUR_IP:8000
    restart: always

volumes:
  postgres_data:
COMPOSE

# Iniciar servicios
sudo docker-compose up -d
EOF

# Ejecutar
chmod +x setup.sh
./setup.sh
```

### 5️⃣ **Configurar GoDaddy (2 min)**

1. Ve a tu dominio en GoDaddy → **DNS Management**
2. Editar registros:

**Registro A (principal):**
- Type: **A**
- Host: **@**
- Points to: **[TU IP DE GCP]**
- TTL: **600**

**Registro A (www):**
- Type: **A**
- Host: **www**
- Points to: **[TU IP DE GCP]**
- TTL: **600**

### 6️⃣ **SSL Gratis (opcional, después que funcione el dominio)**

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

---

## ✅ **VERIFICACIÓN FINAL**

```bash
# En tu VM:
sudo docker ps  # Ver contenedores corriendo
curl http://localhost  # Probar frontend
curl http://localhost:8000/health  # Probar backend
```

## 🆘 **TROUBLESHOOTING**

Si algo falla:
```bash
# Ver logs
sudo docker-compose logs

# Reiniciar servicios
sudo docker-compose restart

# Recrear todo
sudo docker-compose down
sudo docker-compose up -d
```

## 📱 **URLs FINALES**
- **Tu sitio**: http://[TU-IP-GCP] (inmediato)
- **Con dominio**: https://tudominio.com (5-30 min después de configurar DNS)

---

**⏰ TIEMPO TOTAL: 15-20 MINUTOS**
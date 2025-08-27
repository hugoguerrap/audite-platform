#!/bin/bash

# 🚀 SCRIPT PARA EJECUTAR DENTRO DE LA VM GCP
# Ejecutar después de conectarte con SSH

echo "======================================"
echo "🔧 CONFIGURANDO VM PARA AUDITE"
echo "======================================"

# 1. Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# 2. Instalar Docker si no está instalado
if ! command -v docker &> /dev/null; then
    echo "📦 Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# 3. Instalar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 4. Clonar el proyecto
echo "📥 Clonando proyecto..."
cd /home/$USER
git clone https://github.com/tu-usuario/audite-complete.git
cd audite-complete

# 5. Crear archivo .env
echo "🔐 Configurando variables de entorno..."
cat > .env << EOF
# Database
DATABASE_URL=postgresql://audite_user:audite_password_2024@postgres:5432/audite
POSTGRES_USER=audite_user
POSTGRES_PASSWORD=audite_password_2024
POSTGRES_DB=audite

# Security
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_ACCESS_TOKEN_EXPIRES=43200
JWT_REFRESH_TOKEN_EXPIRES=604800

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Audite2024SecurePass!
ADMIN_EMAIL=admin@audite.com

# Frontend
VITE_API_URL=http://$(curl -s ifconfig.me):8000
NODE_ENV=production
EOF

# 6. Iniciar servicios
echo "🚀 Iniciando servicios con Docker Compose..."
sudo docker-compose up -d

# 7. Verificar servicios
echo "✅ Verificando servicios..."
sleep 10
sudo docker-compose ps

# 8. Configurar Nginx como reverse proxy
echo "🌐 Configurando Nginx..."
sudo apt-get install -y nginx

# Configurar Nginx
sudo tee /etc/nginx/sites-available/audite << EOF
server {
    listen 80;
    server_name _;
    
    # Frontend
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # Backend API
    location /api {
        rewrite ^/api(.*) \$1 break;
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Activar configuración
sudo ln -sf /etc/nginx/sites-available/audite /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

echo ""
echo "======================================"
echo "✅ CONFIGURACIÓN COMPLETADA"
echo "======================================"
echo ""
echo "📋 INFORMACIÓN:"
echo "   Frontend: http://$(curl -s ifconfig.me)"
echo "   Backend API: http://$(curl -s ifconfig.me)/api"
echo "   Admin Panel: http://$(curl -s ifconfig.me)/admin"
echo ""
echo "🔐 CREDENCIALES ADMIN:"
echo "   Usuario: admin"
echo "   Password: Audite2024SecurePass!"
echo ""
echo "📌 IMPORTANTE:"
echo "   1. Configura tu dominio en GoDaddy apuntando a: $(curl -s ifconfig.me)"
echo "   2. Después de configurar el dominio, ejecuta:"
echo "      sudo certbot --nginx -d tudominio.com -d www.tudominio.com"
echo ""
echo "======================================"
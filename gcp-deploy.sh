#!/bin/bash

# 🚀 DEPLOY EN GCP - VM ECONÓMICA
# Costo estimado: $5-7/mes (e2-micro)

echo "======================================"
echo "🚀 DEPLOY AUDITE EN GOOGLE CLOUD"
echo "======================================"

# Variables
PROJECT_ID="audite-platform"
ZONE="us-central1-a"
INSTANCE_NAME="audite-vm"
MACHINE_TYPE="e2-micro"  # 2 vCPU, 1GB RAM - Gratis primeros 720h/mes

# 1. Crear VM con Docker pre-instalado
echo "📦 Creando VM con Docker..."
gcloud compute instances create $INSTANCE_NAME \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=30GB \
    --boot-disk-type=pd-standard \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar nginx y certbot para SSL
sudo apt-get update
sudo apt-get install -y nginx certbot python3-certbot-nginx git
'

# 2. Crear reglas de firewall
echo "🔥 Configurando firewall..."
gcloud compute firewall-rules create allow-http \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server

gcloud compute firewall-rules create allow-https \
    --allow tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --target-tags https-server

gcloud compute firewall-rules create allow-app \
    --allow tcp:8000,tcp:5173 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server

# 3. Reservar IP estática
echo "🌐 Reservando IP estática..."
gcloud compute addresses create audite-ip \
    --region us-central1

# Obtener la IP
IP=$(gcloud compute addresses describe audite-ip --region us-central1 --format="get(address)")
echo "✅ IP Estática: $IP"

# 4. Asignar IP a la instancia
gcloud compute instances delete-access-config $INSTANCE_NAME --zone=$ZONE
gcloud compute instances add-access-config $INSTANCE_NAME \
    --zone=$ZONE \
    --address=$IP

echo ""
echo "======================================"
echo "✅ VM CREADA EXITOSAMENTE"
echo "======================================"
echo ""
echo "📋 INFORMACIÓN DE TU VM:"
echo "   Nombre: $INSTANCE_NAME"
echo "   IP Externa: $IP"
echo "   Tipo: $MACHINE_TYPE (Free tier)"
echo "   Costo: ~$5/mes o GRATIS con free tier"
echo ""
echo "🔗 PRÓXIMOS PASOS:"
echo ""
echo "1. Conectate a la VM:"
echo "   gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo ""
echo "2. Clona tu proyecto:"
echo "   git clone https://github.com/tu-usuario/audite.git"
echo "   cd audite"
echo ""
echo "3. Ejecuta Docker Compose:"
echo "   sudo docker-compose up -d"
echo ""
echo "4. Configura GoDaddy:"
echo "   Type: A"
echo "   Host: @"
echo "   Points to: $IP"
echo ""
echo "   Type: A"
echo "   Host: www"
echo "   Points to: $IP"
echo ""
echo "5. SSL Gratis (después de configurar dominio):"
echo "   sudo certbot --nginx -d tudominio.com -d www.tudominio.com"
echo ""
echo "======================================"
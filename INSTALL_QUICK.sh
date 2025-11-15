#!/bin/bash
# Script de instalación rápida para TEA_Edition
# Uso: ./INSTALL_QUICK.sh

set -e  # Salir si hay error

echo "=== INSTALACIÓN RÁPIDA TEA_Edition ==="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Clonar repositorio
echo -e "${GREEN}[1/6]${NC} Clonando repositorio..."
if [ -d "TEA_Edition" ]; then
    echo -e "${YELLOW}⚠️  Directorio TEA_Edition ya existe. Saltando clonado...${NC}"
    cd TEA_Edition
    git pull origin master
else
    git clone https://github.com/shidalgo0925/TEA_Edition.git
    cd TEA_Edition
fi

# 2. Crear entorno virtual
echo -e "${GREEN}[2/6]${NC} Creando entorno virtual..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Entorno virtual ya existe.${NC}"
else
    python3 -m venv venv
fi
source venv/bin/activate

# 3. Instalar dependencias
echo -e "${GREEN}[3/6]${NC} Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verificar PostgreSQL
echo -e "${GREEN}[4/6]${NC} Verificando PostgreSQL..."
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✅ PostgreSQL está instalado${NC}"
else
    echo -e "${RED}❌ PostgreSQL NO está instalado${NC}"
    echo "   Instalar con: sudo apt install postgresql postgresql-contrib"
    exit 1
fi

# 5. Configurar base de datos
echo -e "${GREEN}[5/6]${NC} Configurando base de datos..."
echo -e "${YELLOW}⚠️  IMPORTANTE: Configurar manualmente:${NC}"
echo "   1. Crear base de datos PostgreSQL:"
echo "      sudo -u postgres psql"
echo "      CREATE DATABASE onepercent_db;"
echo "      CREATE USER onepercent_user WITH PASSWORD 'TU_PASSWORD';"
echo "      GRANT ALL PRIVILEGES ON DATABASE onepercent_db TO onepercent_user;"
echo ""
echo "   2. Editar config.py con tus credenciales"
echo "   3. Configurar variables de entorno si es necesario"

# 6. Ejecutar migraciones
echo -e "${GREEN}[6/6]${NC} Ejecutando migraciones..."
if [ -f "alembic.ini" ]; then
    echo "Ejecutando: flask db upgrade"
    flask db upgrade || echo -e "${YELLOW}⚠️  Asegúrate de configurar la base de datos primero${NC}"
else
    echo -e "${YELLOW}⚠️  No se encontró alembic.ini${NC}"
fi

echo ""
echo -e "${GREEN}✅ Instalación completada!${NC}"
echo ""
echo "Para iniciar la aplicación:"
echo "  cd TEA_Edition"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "La aplicación estará disponible en: http://localhost:5006/tea/"


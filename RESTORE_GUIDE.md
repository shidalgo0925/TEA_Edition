# 🔄 GUÍA DE RESTAURACIÓN RÁPIDA - TEA_Edition

## ✅ ¿Puede eliminarse y restaurarse fácilmente?

**SÍ**, TEA_Edition puede eliminarse y restaurarse fácilmente porque:

### ✅ Componentes Disponibles:

1. **✅ Repositorio Git completo** en GitHub
   - URL: https://github.com/shidalgo0925/TEA_Edition.git
   - Todos los archivos de código están versionados

2. **✅ requirements.txt** - Todas las dependencias Python
   - Flask 3.0.2
   - SQLAlchemy >= 2.0
   - psycopg2-binary >= 2.9
   - google-api-python-client
   - alembic >= 1.13

3. **✅ Migraciones de Base de Datos**
   - 5 migraciones disponibles en `migrations/versions/`
   - Sistema Alembic configurado

4. **✅ Configuración**
   - `config.py` con valores por defecto
   - Soporte para variables de entorno

5. **✅ README.md** con instrucciones completas

---

## 🚀 INSTALACIÓN RÁPIDA (3 métodos)

### Método 1: Script Automático (RECOMENDADO)

```bash
# Desde cualquier directorio
git clone https://github.com/shidalgo0925/TEA_Edition.git
cd TEA_Edition
chmod +x INSTALL_QUICK.sh
./INSTALL_QUICK.sh
```

### Método 2: Manual (Paso a paso)

```bash
# 1. Clonar repositorio
git clone https://github.com/shidalgo0925/TEA_Edition.git
cd TEA_Edition

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configurar base de datos (ver sección siguiente)

# 5. Ejecutar migraciones
flask db upgrade

# 6. Iniciar aplicación
python run.py
```

### Método 3: Con Docker (si se implementa)

```bash
docker-compose up -d
```

---

## 🗄️ CONFIGURACIÓN DE BASE DE DATOS

### 1. Crear Base de Datos PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE onepercent_db;
CREATE USER onepercent_user WITH PASSWORD 'TU_PASSWORD_FUERTE';
GRANT ALL PRIVILEGES ON DATABASE onepercent_db TO onepercent_user;
\q
```

### 2. Configurar config.py

Editar `/home/ubuntu/TEA_Edition/config.py`:

```python
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://onepercent_user:TU_PASSWORD@localhost:5432/onepercent_db"
)
```

O usar variable de entorno:

```bash
export DATABASE_URL="postgresql+psycopg2://onepercent_user:TU_PASSWORD@localhost:5432/onepercent_db"
```

### 3. Ejecutar Migraciones

```bash
cd TEA_Edition
source venv/bin/activate
flask db upgrade
```

---

## 🔐 CONFIGURACIÓN OPCIONAL

### Variables de Entorno Recomendadas

```bash
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/onepercent_db"
export SECRET_KEY="tu-clave-secreta-muy-segura"
export CLIENT_SECRETS_FILE="/ruta/a/client_secret.json"
export OAUTH_REDIRECT_URI="https://tu-dominio.com/oauth2callback"
export LOCAL_TZ="America/Panama"
```

### Google OAuth (Opcional)

Si usas Google Calendar:
1. Descargar `client_secret.json` de Google Cloud Console
2. Colocarlo en el directorio del proyecto
3. Configurar `OAUTH_REDIRECT_URI` en Google Cloud Console

---

## ⚠️ COMPONENTES QUE REQUIEREN CONFIGURACIÓN MANUAL

### 1. Base de Datos PostgreSQL
- ✅ Código de migraciones está en el repo
- ⚠️ Requiere crear BD y usuario manualmente

### 2. Credenciales OAuth (Google Calendar)
- ⚠️ Requiere archivo `client_secret.json` (no está en repo por seguridad)
- ⚠️ Requiere configuración en Google Cloud Console

### 3. Variables de Entorno
- ✅ Tiene valores por defecto en `config.py`
- ⚠️ Recomendado configurar para producción

---

## 📋 CHECKLIST DE RESTAURACIÓN

- [ ] Clonar repositorio de GitHub
- [ ] Crear entorno virtual
- [ ] Instalar dependencias (`pip install -r requirements.txt`)
- [ ] Instalar PostgreSQL (si no está)
- [ ] Crear base de datos y usuario
- [ ] Configurar `config.py` o variables de entorno
- [ ] Ejecutar migraciones (`flask db upgrade`)
- [ ] (Opcional) Configurar Google OAuth
- [ ] Iniciar aplicación (`python run.py`)

---

## 🎯 TIEMPO ESTIMADO DE RESTAURACIÓN

- **Con PostgreSQL ya instalado:** 5-10 minutos
- **Sin PostgreSQL:** 15-20 minutos (incluye instalación)
- **Con configuración completa (OAuth, etc.):** 20-30 minutos

---

## 💡 RECOMENDACIONES

1. **Guardar configuración de producción:**
   ```bash
   # Guardar config.py personalizado
   cp config.py config.py.production
   ```

2. **Documentar credenciales:**
   - Guardar en lugar seguro (no en Git)
   - Usar variables de entorno en producción

3. **Backup de base de datos:**
   ```bash
   pg_dump -U onepercent_user onepercent_db > backup.sql
   ```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "No module named 'flask'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "database does not exist"
```bash
sudo -u postgres createdb onepercent_db
```

### Error: "permission denied"
```bash
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE onepercent_db TO onepercent_user;"
```

---

**Última actualización:** $(date)


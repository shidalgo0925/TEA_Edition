# 1% Better Every Day: TEA Edition

## 🎯 Descripción
Aplicación educativa inclusiva diseñada especialmente para niños con Trastorno del Espectro Autista (TEA). Tiene como objetivo apoyar el desarrollo del lenguaje y habilidades cognitivas a través de un entorno interactivo guiado por un avatar tipo maestra virtual.

## 🚀 Características Principales

### 👨‍👩‍👧 Dashboard de Padres
- Monitoreo de progreso del niño
- Configuración de actividades
- Reportes de avance
- Configuración de voz del avatar

### 🧒 Dashboard del Niño
- Avatar virtual animado
- Actividades interactivas
- Sistema de recompensas
- Progreso visual

### 🎤 Sistema de Audio
- Síntesis de voz (Text-to-Speech)
- Reconocimiento de voz (Speech-to-Text)
- Configuración de voces
- Feedback auditivo

### 🎮 Actividades Interactivas
- Actividades de lenguaje
- Ejercicios de pronunciación
- Juegos educativos
- Seguimiento de progreso

## 🛠️ Tecnologías

- **Backend:** Flask 3.0.2
- **Base de Datos:** PostgreSQL
- **Frontend:** HTML5, CSS3, JavaScript
- **Audio:** Web Speech API
- **PWA:** Progressive Web App

## 📦 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/tea-edition.git
cd tea-edition
```

2. Crear entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar base de datos:
```bash
# Editar config.py con tu configuración de PostgreSQL
```

5. Ejecutar la aplicación:
```bash
python run.py
```

## 🌐 URLs

- **Local:** http://localhost:5006/tea/
- **Producción:** https://1bedkids.easytech.services/tea/

## 📱 PWA

La aplicación es una Progressive Web App (PWA) que puede ser instalada en dispositivos móviles.

## 🔧 Configuración

### Variables de Entorno
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `SECRET_KEY`: Clave secreta de Flask
- `DEBUG`: Modo debug (True/False)

### Base de Datos
- PostgreSQL 12+
- Usuario: onepercent_user
- Base de datos: onepercent_db

## 📊 Estado del Proyecto

- ✅ Sistema de autenticación
- ✅ Dashboard de padres
- ✅ Dashboard del niño
- ✅ Actividades interactivas
- ✅ Sistema de voz
- ✅ PWA funcional

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Equipo

- **Desarrollador:** Shidalgo ETS
- **Email:** shidalgo0925@gmail.com

## 📞 Soporte

Para soporte técnico, contactar a: shidalgo0925@gmail.com

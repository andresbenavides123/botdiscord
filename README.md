# 🚀 SyncBot - Virtual Office Management

SyncBot es un bot de Discord diseñado para gestionar la logística y productividad de equipos de trabajo remotos. Está construido con una arquitectura modular basada en **Cogs** (extensiones) para facilitar el desarrollo colaborativo.

## 🛠️ Estado Actual del Proyecto (Arquitectura Base)

Actualmente, los cimientos del bot están listos. El **Arquitecto Core & DevOps** ha completado las siguientes tareas:

- [x] **Estructura Modular:** Organización de carpetas lista (`cogs/`, `core/`, `db/`).
- [x] **Punto de Entrada:** `main.py` configurado para cargar automáticamente todas las extensiones de la carpeta `cogs/`.
- [x] **Seguridad:** Sistema de variables de entorno implementado para proteger el Token de Discord.
- [x] **Despliegue:** Archivos `requirements.txt` y `Procfile` listos para el despliegue en la nube (Railway).
- [x] **Gestión de Versiones:** Repositorio Git inicializado y sincronizado con GitHub.

## 📂 Estructura de Archivos

- `main.py`: El corazón del bot. Maneja la conexión y carga los módulos.
- `cogs/`: Carpeta donde residen las funcionalidades (Standups, Focus Mode, Soporte).
- `core/`: Configuraciones centrales y utilidades.
- `db/`: Espacio reservado para la lógica de base de datos.
- `Procfile`: Instrucciones para el servidor de despliegue.

## 🚀 Cómo empezar (Local)

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configurar el entorno:**
   - Renombra el archivo `.env.example` a `.env`.
   - Agrega tu `DISCORD_TOKEN` dentro del archivo `.env`.
3. **Ejecutar:**
   ```bash
   python main.py
   ```

## 👥 Equipo de Desarrollo
- **Arquitecto Core & DevOps:** Encargado de los cimientos y el despliegue.
- **Data Master:** (En desarrollo) Gestión de bitácoras y bases de datos.
- **Time Keeper:** (En desarrollo) Gestión de tiempos y modo enfoque.
- **Support Engineer:** (En desarrollo) Comandos de ayuda y soporte técnico.

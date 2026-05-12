# 🚀 SyncBot - Virtual Office Management

SyncBot es un bot de Discord diseñado para gestionar la logística y productividad de equipos de trabajo remotos. Está construido con una arquitectura modular basada en **Cogs** (extensiones) para facilitar el desarrollo colaborativo.

## 🛠️ Estado Actual del Proyecto (Arquitectura Base)

Actualmente, los cimientos del bot están listos. El **Arquitecto Core & DevOps** ha completado las siguientes tareas:

- [x] **Estructura Modular:** Organización de carpetas lista (`cogs/`, `core/`, `db/`).
- [x] **Punto de Entrada:** `main.py` configurado para cargar automáticamente todas las extensiones de la carpeta `cogs/`.
- [x] **Seguridad:** Sistema de variables de entorno implementado para proteger el Token de Discord.
- [x] **Despliegue:** Archivos `requirements.txt` y `Procfile` listos para el despliegue en la nube (Railway).
- [x] **Gestión de Versiones:** Repositorio Git inicializado y sincronizado con GitHub.

### 📊 Desarrollo de Módulos (Cogs)

**El Data Master** ha completado su reto del Stand-up asíncrono:

- [x] **Base de Datos (`db/database.py`):** Configuración de SQLite creando la tabla `standups` que guarda: Usuario, Tarea de hoy, y Fecha.
- [x] **Comando `!daily` (`cogs/standup.py`):** El bot recibe reportes diarios mediante `!daily [texto]`.
- [x] **Limpieza:** El bot borra el mensaje original del usuario para mantener el chat ordenado.
- [x] **Embeds y Canal `#bitacora`:** El bot genera un mensaje con formato bonito (Embed color verde y avatar) y lo envía automáticamente al canal específico `#bitacora`.

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
- **Data Master:** ✅ (Completado) Gestión de bitácoras y bases de datos (`!daily`).
- **Time Keeper:** (En desarrollo) Gestión de tiempos y modo enfoque.
- **Support Engineer:** ✅ (Completado) Comandos de ayuda y soporte técnico.

# SyncBot - Modulo Time Keeper

Este repositorio contiene la implementacion del modulo de productividad "Time Keeper" (Integrante 3) para SyncBot, un bot de Discord modular.

## Estado Actual del Proyecto

El Time Keeper ha completado el desarrollo del sistema Pomodoro para trabajo profundo.

- [x] **Comando de Enfoque:** Implementacion del comando `!focus [minutos]` listo para su uso.
- [x] **Gestion de Permisos y Roles:** Asignacion automatica del rol "En la Zona" al inicio de la sesion y su retiro al final.
- [x] **Temporizadores asincronos:** Integracion de `asyncio.sleep()` en las funciones del bot para pausar sesiones sin afectar a otros usuarios.
- [x] **Notificaciones directas:** Avisos via Mensaje Directo (DM) a los usuarios cuando completan su sesion de trabajo profundo.

## Estructura de Archivos

- `cogs/focus.py`: Archivo principal del Integrante 3. Contiene la clase `FocusCog` con toda la logica del temporizador y control de roles.

## Como probar el modulo de Focus

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configurar el entorno:**
   - Renombra el archivo `.env.example` a `.env`
   - Agrega tu `DISCORD_TOKEN` dentro del archivo `.env`
3. **Ejecutar el bot:**
   ```bash
   python main.py
   ```
4. **Comandos disponibles en Discord:**
   - Escribe `!focus 25` en cualquier canal para iniciar un Pomodoro de 25 minutos.

## Responsabilidades del Integrante 3 (Time Keeper)

- Crear el sistema de tareas asincronas para el trabajo profundo.
- Manipular los permisos y roles de los usuarios en el servidor en tiempo real.
- Gestionar las notificaciones por DM a los usuarios.

## Nota profesional para despliegue y permisos

Por favor, siga estas indicaciones antes de desplegar o probar el módulo **Time Keeper** en un servidor de producción:

- **Permisos mínimos requeridos para el bot:** `Manage Roles`, `Send Messages`, `Read Message History`, `View Channels`. Si el bot borra mensajes (funcionalidad `!daily`), también necesitará `Manage Messages`.
- **Posición del rol del bot:** Asegúrese de que el rol del bot esté por encima del rol `En la Zona 🎧` en la jerarquía de roles del servidor para que pueda asignarlo y retirarlo correctamente.
- **Seguridad del token:** Use el archivo `.env` para la variable `DISCORD_TOKEN`. Nunca suba su token a repositorios públicos.
- **Pruebas recomendadas:**
  1.  Crear un servidor de pruebas y otorgar al bot los permisos arriba mencionados.

2.  Ejecutar `!focus 1` y verificar que el rol `En la Zona 🎧` se crea (si no existe), se asigna y se retira tras 1 minuto.
3.  Comprobar que el usuario recibe un DM al finalizar (y que existe el fallback al canal si el DM falla).

- **Resiliencia y mejoras sugeridas:** Actualmente las sesiones activas se mantienen en memoria; si el bot se reinicia durante una sesión, esta información se pierde. Para mayor robustez, considere persistir sesiones en `db/`.

Si todo está correcto, ya se han subido los cambios al branch `main`. Si desea, puedo crear un archivo adicional con instrucciones específicas para el administrador del servidor o abrir un Pull Request con una descripción formal de los cambios.

# SyncBot - Módulo Support Engineer

Este repositorio incluye la implementación del módulo de soporte "Support Engineer" (Integrante 4) para SyncBot.

## Estado Actual del Proyecto

El Support Engineer ha completado el desarrollo del panel de ayuda y el botón de pánico para Pair Programming.

- [x] **Panel de Ayuda (`!help`):** Reemplazo del comando `help` por defecto por un panel personalizado (Embed) con instrucciones claras.
- [x] **Botón de Pánico (`!sos`):** Comando `!sos [problema]` que notifica a los miembros disponibles del equipo.
- [x] **Filtro de Disponibilidad:** Integración inteligente que omite notificar a usuarios con el rol "En la Zona 🎧" (respetando al Time Keeper).
- [x] **Buenas Prácticas:** Código estructurado en inglés, comentarios en inglés y UI/textos en español.

## Estructura de Archivos (Integrante 4)

- `cogs/help.py`: Archivo principal del Integrante 4. Contiene la clase `SupportCog` con los comandos `help` y `sos`.

## Cómo probar el módulo de Soporte

1. **Comando Help:**
   - Escribe `!help` en cualquier canal para ver la lista de comandos disponibles.
2. **Comando SOS:**
   - Escribe `!sos Error en el servidor` en cualquier canal para pedir ayuda. El bot notificará a quienes no estén concentrados.

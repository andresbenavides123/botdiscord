# 🚨 Módulo de Soporte — `cogs/support.py`
> **Integrante:** Han (The Support Engineer)
> **Rama de trabajo:** `han`

---

## 📋 Misión

Crear el sistema de **pair programming bajo demanda** y el **manual de usuario** del bot.  
Este módulo es responsable de la comunicación de emergencia y la experiencia de usuario del equipo virtual.

---

## 📁 Archivo a cargo

```
cogs/support.py  →  Clase SupportCog
```

---

## ✅ Tareas implementadas

### 1. 🚨 Comando `!sos [problema]`

**¿Qué hace?**  
Cuando un integrante del equipo está bloqueado o necesita ayuda urgente, escribe `!sos` seguido de la descripción del problema. El bot automáticamente:

1. Detecta quiénes **no tienen** el rol `En la Zona 🎧` (es decir, quiénes están disponibles).
2. Envía un **mensaje privado (DM)** a cada persona disponible con un embed de alerta rojo.
3. Confirma en el canal quiénes fueron notificados y los menciona para mayor visibilidad.
4. Si todos están en modo concentración, avisa que no hay nadie disponible.

**Uso:**
```
!sos No me corre el servidor, error 500
!sos No entiendo cómo conectar la base de datos
```

**Lógica clave:**
- Filtra `ctx.guild.members` excluyendo bots, el autor del SOS y quienes tengan el rol `En la Zona 🎧`.
- Usa `member.send()` para notificar por DM.
- Maneja el caso en que un usuario tenga los DMs cerrados (`discord.Forbidden`).

---

### 2. 📖 Comando `!help` personalizado

**¿Qué hace?**  
Sobrescribe el comando `!help` que trae Discord por defecto (ya desactivado en `main.py` con `help_command=None`) y lo reemplaza con un **embed estilizado** que lista todos los comandos del bot con descripción y ejemplo de uso.

**Uso:**
```
!help
```

**Comandos documentados en el embed:**

| Comando | Descripción |
|---|---|
| `!daily [tarea]` | Registra el standup diario del integrante |
| `!focus` | Activa/desactiva el modo concentración (`En la Zona 🎧`) |
| `!sos [problema]` | Envía alerta de emergencia al equipo disponible |
| `!help` | Muestra este manual de comandos |

**Diseño:**
- Color morado `rgb(88, 101, 242)` (estilo Discord).
- Thumbnail con el avatar del bot.
- Separadores visuales entre comandos.
- Footer con el nombre del bot.

---

## 🔧 Requisitos técnicos

Para que los comandos funcionen correctamente, el bot necesita:

- ✅ **Members Intent** activado — configurado en `main.py` con `intents.members = True`.
- ✅ **Message Content Intent** activado — configurado en `main.py` con `intents.message_content = True`.
- ✅ Permiso para **enviar DMs** a los miembros del servidor.
- ✅ El rol `En la Zona 🎧` debe existir en el servidor para que `!sos` lo detecte.

---

## 📦 Dependencias instaladas

```bash
pip install -r requirements.txt
```

Incluye `discord.py==2.3.2` que provee `discord.ext.commands` y todos los módulos utilizados.

---

## 📝 Historial de commits

| Commit | Descripción |
|---|---|
| `e943014` | `implementar comandos !sos y !help personalizados` |

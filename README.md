# Hotel API - Arquitectura Hexagonal con Autenticación OAuth2, JWT y Chat en Tiempo Real (WebSockets)

## Arquitectura Hexagonal
Este proyecto está estructurado bajo los principios de la **Arquitectura Hexagonal (Puertos y Adaptadores)**. El objetivo principal de este patrón es **aislar el núcleo del negocio (la lógica de aplicación y dominio)** de cualquier factor o tecnología externa (bases de datos, frameworks web, librerías de seguridad).

- **Dominio (Domain):** Es el corazón de la aplicación. Contiene las reglas puras del negocio y las interfaces (**Puertos**) que definen cómo se comunicará el sistema con el exterior. No depende de ninguna librería ni tecnología externa. Aquí residen la nueva entidad `MensajeChat` junto a los contratos de persistencia e inteligencia del bot (`MensajeRepository` y `FAQPort`).
- **Aplicación (Application/Casos de Uso):** Orquesta los flujos de la aplicación implementando las reglas del negocio. Utiliza e inyecta los puertos del dominio, permaneciendo totalmente agnóstica a si los datos provienen de una base de datos local o de un servicio en la nube. En esta capa, el `ChatService` define las políticas de control para decidir si una consulta la responde el asistente automatizado o si requiere la intervención directa de soporte.
- **Infraestructura y Adaptadores (Infrastructure / Adapters):** Son las implementaciones técnicas y herramientas externas necesarias para que el sistema funcione (FastAPI para la API HTTP, SQLAlchemy para la conexión a MySQL, y Bcrypt/PyJWT para la seguridad criptográfica). Se conectan a la aplicación a través de los puertos definidos. Se complementa con un enrutador bidireccional por WebSockets (`chat_router`) y un buscador de respuestas preestablecidas indexado en memoria (`InMemoryFAQRepository`).

---

## Organización final de carpetas para el patrón hexagonal:

app/
├── domain/
│   ├── models/            # Entidades puras de datos (Usuario, Cuarto, Huesped, Reserva, MensajeChat)
│   ├── ports/             # Contratos e interfaces (PasswordHasher, UsuarioRepository, FAQPort, MensajeRepository)
│   └── exceptions/        # Excepciones de negocio personalizadas
├── application/
│   └── services/          # Casos de uso y lógica de negocio (AuthService, CuartoService, ChatService, etc.)
├── infrastructure/
│   ├── security/          # Adaptadores técnicos de seguridad (BcryptHasher, JWTManager)
│   ├── db/mysql/          # Adaptadores de persistencia con SQLAlchemy orientados a MySQL (Mapeo e historial de soporte)
│   └── faq/               # Proveedor de almacenamiento técnico para respuestas automáticas (FAQ)
└── adapters/
    ├── api/
    │   ├── routers/       # Controladores y enrutadores HTTP de FastAPI
    │   ├── schemas/       # Esquemas de validación de datos con Pydantic
    │   └── dependencies/  # Inyectores de dependencias para validar tokens de sesión
    └── realtime/
        └── chat_router.py # Adaptador de comunicación bidireccional por WebSockets y control de conexiones por rol JWT

---

## Pruebas del Chat en Tiempo Real (WebSockets)

1. **Levantar el Servidor Backend:**
   ```bash
   venv\Scripts\activate
   uvicorn main:app --reload
2. **Obtener Tokens de Acceso (JWT):**
   ```bash
   Accede al swagger en http://127.0.0.1:8000/docs.
   Autentícate en el endpoint /api/auth/login y genera un token con credenciales de un usuario de rol "Cliente" (Huésped) y otro con rol "Administrador".
3. **Simular Conversación**
   ```bash
   Panel del Administrador (chat_admin.html): Ábrelo en el navegador, introduce el token de Administrador
   Lado del Huésped (chat_huesped.html): Ábrelo en otra ventana paralela, ingresa el token del Cliente y envía un mensaje.
   Si el texto contiene palabras clave indexadas (check-in, mascotas, pagos, desayuno), el Bot responderá de forma automática.
   Si la duda no coincide con ninguna palabra clave, igualmente el administrador podrá ver el chat ay responder al huesped.
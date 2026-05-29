# Hotel API - Arquitectura Hexagonal con Autenticación OAuth2 y JWT

## Arquitectura Hexagonal
Este proyecto está estructurado bajo los principios de la **Arquitectura Hexagonal (Puertos y Adaptadores)**. El objetivo principal de este patrón es **aislar el núcleo del negocio (la lógica de aplicación y dominio)** de cualquier factor o tecnología externa (bases de datos, frameworks web, librerías de seguridad).

- **Dominio (Domain):** Es el corazón de la aplicación. Contiene las reglas puras del negocio y las interfaces (**Puertos**) que definen cómo se comunicará el sistema con el exterior. No depende de ninguna librería ni tecnología externa.
- **Aplicación (Application/Casos de Uso):** Orquesta los flujos de la aplicación implementando las reglas del negocio. Utiliza e inyecta los puertos del dominio, permaneciendo totalmente agnóstica a si los datos provienen de una base de datos local o de un servicio en la nube.
- **Infraestructura y Adaptadores (Infrastructure / Adapters):** Son las implementaciones técnicas y herramientas externas necesarias para que el sistema funcione (FastAPI para la API HTTP, SQLAlchemy para la conexión a MySQL, y Bcrypt/PyJWT para la seguridad criptográfica). Se conectan a la aplicación a través de los puertos definidos.

---

## La organización final de para el patrón hexagonal:

app/
├── domain/
│   ├── models/            # Entidades puras de datos (Usuario, Cuarto, Huesped, Reserva)
│   ├── ports/             # Contratos e interfaces (PasswordHasher, UsuarioRepository, etc.)
│   └── exceptions/        # Excepciones de negocio personalizadas
├── application/
│   └── services/          # Casos de uso y lógica de negocio (AuthService, CuartoService, etc.)
├── infrastructure/
│   ├── security/          # Adaptadores técnicos de seguridad (BcryptHasher, JWTManager)
│   └── db/mysql/          # Adaptadores de persistencia con SQLAlchemy orientados a MySQL
└── adapters/
    └── api/
        ├── routers/       # Controladores y enrutadores HTTP de FastAPI
        ├── schemas/       # Esquemas de validación de datos con Pydantic
        └── dependencies/  # Inyectores de dependencias para validar tokens de sesión

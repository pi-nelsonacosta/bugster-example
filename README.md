# Bugster API 📋🐞

## Descripción del Proyecto

**Bugster API** es una aplicación desarrollada en **FastAPI** que captura eventos de interacción de usuario provenientes de aplicaciones web, los agrupa en **historias de usuario** y genera automáticamente **tests E2E en Playwright**. Esto facilita la creación de tests automatizados basados en interacciones reales de los usuarios, ayudando a mantener una suite de pruebas robusta y actualizada.

---

## Características Principales 🛠️

1. **Recepción de Eventos**:
   - Recibe eventos de interacción de usuario desde aplicaciones web.
   - Valida y almacena estos eventos en la base de datos.

2. **Agrupación en Historias de Usuario**:
   - Agrupa eventos relacionados en historias de usuario.
   - Detecta patrones comunes y organiza los eventos de manera lógica.

3. **Generación Automática de Tests**:
   - Genera tests E2E usando Playwright a partir de las historias de usuario.
   - Los tests incluyen validaciones y capturas de pantalla para facilitar el debugging.

4. **Ejecución de Tests Dinámica**:
   - Permite ejecutar tests almacenados directamente desde la API.

---

## Requisitos Previos ✅

- **Python 3.11**
- **Docker y Docker Compose**
- **MongoDB** (o cualquier base de datos compatible)

### Instalación de Herramientas

1. **Instalar Docker**:  
   [Guía oficial de instalación de Docker](https://docs.docker.com/get-docker/)

2. **Instalar Docker Compose**:  
   [Guía oficial de instalación de Docker Compose](https://docs.docker.com/compose/install/)

---

## Instalación 🚀

Clona el repositorio del proyecto:

```bash
git clone https://github.com/pi-nelsonacosta/bugster-example.git
cd bugster-example
```

Instala las dependencias y descarga los navegadores:

```bash
pip install -r requirements.txt
playwright install
```

Inicia el servidor de desarrollo:

```bash
uvicorn main:app --reload
```
## Despliegue con Docker

Para desplegar el proyecto con Docker, sigue los siguientes pasos:

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2. Abre una terminal y navega hasta la carpeta del proyecto.
3. Ejecuta el siguiente comando para construir la imagen Docker:


```bash
cd docker/develop
docker-compose up --build

```

. Para verificar que el servidor de producción está funcionando, puedes ejecutar el siguiente comando en la terminal:

```bash
docker-compose ps
```

. Si todo está funcionando correctamente, deberías ver un mensaje similar al siguiente:

```
      Name                     Command               State           Ports
--------------------------------------------------------------------------------
bugster-api_bugster-api_1   uvicorn main:app       Up      0.0.0.0:8000->8000/tcp
```

. Para detener el servidor de producción, puedes ejecutar el siguiente comando en la terminal:

```bash
docker-compose down
```

## Estructura del Proyecto 📂

bugster-api/
│-- app/
│   ├── api/
│   │   └── routers/
│   │       └── events.py          # Endpoints de la API
│   ├── db/
│   │   └── repository/
│   │       └── event_repository.py  # Funciones de base de datos
│   ├── schemas/
│   │   └── event.py               # Esquemas Pydantic
│   └── services/
│       └── event_service.py       # Lógica de negocio
│-- docker/
│   └── develop/
│       └── Dockerfile             # Dockerfile para desarrollo
│-- main.py                        # Punto de entrada de FastAPI
│-- requirements.txt               # Dependencias del proyecto
└-- README.md                      # Documentación del proyecto

## Decisiones de Diseño

El diseño de Bugster API tiene como objetivo capturar eventos de interacción de usuarios y convertirlos automáticamente en tests E2E con Playwright. A continuación, se resumen las decisiones de diseño clave y su justificación:

  * FastAPI como Framework de la API
  * Rendimiento eficiente con Starlette y Pydantic.
  * Validación de datos automática con Pydantic.
  * Documentación automática con Swagger UI.
  * Soporte para asincronía (async/await) para operaciones I/O.
  * MongoDB para Almacenamiento
  * Flexibilidad de esquema al ser una base NoSQL.
  * Facilita el escalado horizontal para grandes volúmenes de eventos.
  * Documentos JSON-like, alineados con los datos de la API.
  * Agrupación de Eventos en Historias de Usuario
  * Permite identificar patrones de uso.
  * Facilita la modularidad y generación de tests específicos.
  * Proporciona claridad en los flujos de interacción del usuario.
  * Generación Automática de Tests con Playwright
  * Soporte para múltiples navegadores (Chrome, Firefox, WebKit).
  * Capturas de pantalla y control detallado de elementos.
  * API intuitiva para generar tests dinámicamente.
  * Ejecución en modo headless/headful.
  * Despliegue con Docker y Docker Compose
  * Funciones auxiliares (add_click_step, add_input_step) para reutilización de código.
  * Manejo de errores con try/except para robustez.

  Trade-offs Considerados ⚖️
  * MongoDB vs SQL: Se eligió MongoDB por su flexibilidad y escalabilidad frente a una base de datos relacional.
 

  Áreas de Mejora 🚀
  * Optimización de consultas a MongoDB para mejorar el rendimiento con grandes volúmenes de datos.
  * Seguridad: Implementar autenticación y autorización en los endpoints.
  * Mejora de Logs: Añadir más detalles en los logs para facilitar el debugging.
  * Pruebas Unitarias: Aumentar la cobertura de pruebas unitarias para garantizar la estabilidad del código.

## Para contribuir al proyecto

1. Fork el repositorio.
2. Crea una nueva rama con tus cambios.
3. Envía un pull request al repositorio.

## Licencia

Este proyecto está bajo la licencia MIT. Para más información, consulta el archivo [LICENSE](LICENSE).
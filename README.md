# Bugster API 📋🐞

## Descripción del Proyecto

**Bugster API** es una aplicación desarrollada en **FastAPI** que captura eventos de interacción de usuario provenientes de aplicaciones web, los agrupa en **historias de usuario** y genera automáticamente **tests E2E en Playwright**. Esto facilita la creación de tests automatizados basados en interacciones reales de los usuarios, ayudando a mantener una suite de pruebas robusta y actualizada.

---

## Tabla de Contenidos

1. [Características Principales](#características-principales)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
4. [Ejecución del Proyecto](#ejecución-del-proyecto)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Endpoints de la API](#endpoints-de-la-api)
7. [Base de Datos](#base-de-datos)
8. [Ejemplo de Uso](#ejemplo-de-uso)
9. [Decisiones de Diseño](#decisiones-de-diseño)
10. [Trade-offs Considerados](#trade-offs-considerados)
11. [Áreas de Mejora](#áreas-de-mejora)
12. [Despliegue con Docker](#despliegue-con-docker)

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
git clone https://github.com/tu-usuario/bugster-api.git
cd bugster-api
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

## Ejecución del Proyecto
Usando Docker:

```bash
docker-compose up
```

Usando Python:
Para ejecutar el proyecto en producción, ejecuta el siguiente comando:

```bash
uvicorn main:app
```

## Despliegue con Docker

Para desplegar el proyecto con Docker, sigue los siguientes pasos:

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2. Abre una terminal y navega hasta la carpeta del proyecto.
3. Ejecuta el siguiente comando para construir la imagen Docker:


```bash
docker-compose build
```

4. Ejecuta el siguiente comando para iniciar el servidor de desarrollo:

```bash
docker-compose up
```

5. Abre una nueva terminal y ejecuta el siguiente comando para iniciar el servidor de producción: 

```bash
docker-compose up -d
```

6. Para verificar que el servidor de producción está funcionando, puedes ejecutar el siguiente comando en la terminal:

```bash
docker-compose ps
```

7. Si todo está funcionando correctamente, deberías ver un mensaje similar al siguiente:

```
      Name                     Command               State           Ports
--------------------------------------------------------------------------------
bugster-api_bugster-api_1   uvicorn main:app       Up      0.0.0.0:8000->8000/tcp
```

8. Para detener el servidor de producción, puedes ejecutar el siguiente comando en la terminal:

```bash
docker-compose down
```

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
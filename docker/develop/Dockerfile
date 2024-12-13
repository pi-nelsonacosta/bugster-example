# Imagen base oficial de Python
FROM python:3.11

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY ../../requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright y descargar los navegadores con sus dependencias
RUN pip install playwright
RUN playwright install --with-deps

# Instalar pytest si no está en requirements.txt
RUN pip install pytest

# Establecer permisos en /tmp para permitir escritura/ejecución
RUN chmod 777 /tmp

# Copiar todo el contenido del proyecto al contenedor
COPY ../../ .

# Exponer el puerto en el que corre FastAPI
EXPOSE 8000

# Comando para ejecutar el servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]





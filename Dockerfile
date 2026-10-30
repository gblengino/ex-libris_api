# 1. Sistema Operativo y entorno de Python base
FROM python:3.12-slim

# 2. Instalar el gestor uv de forma ultra rápida desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Definir la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar los archivos de configuración de dependencias
COPY pyproject.toml uv.lock ./

# 5. Instalar todas las dependencias con uv de forma reproducible
RUN uv sync --frozen --no-cache

# 6. Copiar todo el código fuente del proyecto a la imagen
COPY . .

# 7. Documentar el puerto de Django
EXPOSE 8000

# 8. Comando por defecto cuando el contenedor arranca
CMD ["uv", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]
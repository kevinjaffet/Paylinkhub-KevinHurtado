# PayLinkHub

PayLinkHub es un servicio de agregación de pagos. Esta versión expone una API REST con un contrato canónico de dashboard y un endpoint de salud. El dashboard responde con datos fijos de prueba.

Proyecto del examen Desarrollo, Integración e Innovación en el Ecosistema de Pagos.

## Stack tecnológico

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- Python-dotenv
- HTTPX
- Tenacity
- Pytest

## Requisitos previos

- Python 3.12
- pip, incluido con esa instalación de Python
- PowerShell

Los comandos siguientes se ejecutan en el directorio que contiene `app/`, `requirements.txt` y `.env.example`.

## Instalación

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

El entorno virtual del proyecto es la carpeta `venv`.

## Configuración

Crea el archivo local `.env` a partir del ejemplo:

```powershell
Copy-Item .env.example .env
```

`.env.example` define estas variables:

- `APP_NAME`
- `APP_VERSION`
- `API_PREFIX`

## Ejecución

Con el entorno virtual activo, en el mismo directorio:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

La API queda disponible en `http://127.0.0.1:8000`.

## Endpoints actuales

- `GET /health`: indica que el servicio está operativo.
- `GET /api/v1/dashboard/{customerId}`: devuelve el dashboard canónico del cliente. `customerId` se refleja en el identificador del cliente y el resto de la respuesta usa datos fijos de prueba.

## Documentación API

Con el servidor en ejecución, la documentación interactiva está en:

`http://127.0.0.1:8000/docs`

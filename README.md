# PayLinkHub

PayLinkHub es un servicio de agregación de pagos. Esta versión expone una API REST con un contrato canónico de dashboard y un endpoint de salud.

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
- `GET /api/v1/dashboard/{customerId}`: devuelve el dashboard canónico del cliente.

## Contrato canónico

Ejemplo de `GET /api/v1/dashboard/{customerId}` cuando CORE, PAGOS y FX responden:

```json
{
  "customer": {
    "id": "1",
    "full_name": "Emily Johnson",
    "email": "emily.johnson@x.dummyjson.com",
    "phone": "+81 965-431-3024"
  },
  "transactions": [
    {
      "id": "1",
      "products": ["iPhone 9"],
      "quantity": 1,
      "total_usd": "549.00"
    }
  ],
  "partial": false,
  "warnings": [],
  "providers": {
    "core": "ok",
    "pagos": "ok",
    "fx": "ok"
  },
  "exchange_rates": {
    "base": "USD",
    "EUR": 0.92,
    "GBP": 0.78
  }
}
```

`total_usd` se serializa como texto para conservar los decimales. `EUR` y `GBP` se serializan como números. Si FX falla o su respuesta no trae `base`, `EUR` y `GBP`, `exchange_rates` es `null`, `partial` es `true`, `providers.fx` es `unavailable` y `warnings` incluye `FX is unavailable`.

## Documentación API

Con el servidor en ejecución, la documentación interactiva está en:

`http://127.0.0.1:8000/docs`

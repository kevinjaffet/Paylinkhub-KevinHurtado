Luego de haber creado la estructura de arquitectura del proyecto, paso a utilizar un agente de Cursor para generar el primer requisito con el siguiente prompt: 

"Configuración inicial del backend PayLinkHub

Actúa como un desarrollador backend senior especializado en Python y FastAPI.

Debes implementar exclusivamente la **Fase 1 del roadmap de PayLinkHub: configuración inicial del backend**.

## 1. Contexto del proyecto

PayLinkHub es un servicio de agregación de pagos que posteriormente integrará proveedores externos (CORE, PAGOS y FX), expondrá un contrato canónico mediante una API REST y ofrecerá un panel web de monitoreo.

Stack definido:
- Python.
- FastAPI.
- Uvicorn.
- HTTPX.
- Tenacity.
- Pydantic.
- Pydantic Settings.
- Python-dotenv.
- Pytest.

Las dependencias ya están instaladas en el entorno virtual del proyecto.

## 2. Objetivos de esta tarea

Implementar:

1. `app/main.py`
2. `app/config.py`
3. `.env.example`
4. `.gitignore`

Configurar FastAPI y dejar el servidor funcionando localmente.

## 3. Requisitos técnicos

### A. app/config.py

Implementar la configuración centralizada utilizando Pydantic Settings.

Requisitos:
- Utilizar `BaseSettings`.
- Leer variables de entorno.
- Soportar archivo `.env`.
- Configurar un nombre para la aplicación.
- Configurar el prefijo de la API, inicialmente `/api/v1`.
- Evitar credenciales y secretos incrustados en el código.
- Mantener una estructura sencilla y extensible.

### B. app/main.py

Crear la aplicación FastAPI.

Requisitos:
- Instanciar FastAPI utilizando la configuración centralizada.
- Definir título y versión de la aplicación.
- Incorporar un endpoint `GET /health` que devuelva HTTP 200.
- La respuesta debe ser JSON e indicar que el servicio está operativo.
- Mantener el código organizado y preparado para incorporar routers posteriormente.

No implementar todavía el dashboard ni las integraciones externas.

### C. .env.example

Crear un archivo de ejemplo con las variables de configuración necesarias.

No incluir credenciales reales ni secretos.

### D. .gitignore

Asegurar que se excluyan, como mínimo:

- `venv/`
- `.venv/`
- `.env`
- `__pycache__/`
- `*.py[cod]`
- `.pytest_cache/`
- `.idea/`
- `.vscode/`

No excluir `.env.example`.

## 4. Restricciones

- No instalar nuevas dependencias.
- No modificar la estructura de directorios existente.
- No implementar funcionalidades correspondientes a fases posteriores.
- No modificar `requirements.txt`.
- No modificar archivos de documentación.
- No implementar frontend.
- No introducir patrones arquitectónicos innecesarios.
- Mantener compatibilidad con Windows y PowerShell.

## 5. Validación obligatoria

Después de implementar:

1. Verificar que los imports funcionan.
2. Iniciar Uvicorn.
3. Comprobar que `GET /health` devuelve HTTP 200.
4. Comprobar que `/docs` carga correctamente.
5. Identificar y corregir cualquier error encontrado.

Utilizar el entorno virtual existente.

## 6. Entrega

Al terminar, proporciona:

1. Lista de archivos creados o modificados.
2. Explicación breve de las decisiones técnicas.
3. Comandos exactos para ejecutar el servidor desde PowerShell.
4. Resultado de las verificaciones realizadas.
5. Cualquier problema pendiente.

**IMPORTANTE:** No realices commits ni ejecutes comandos Git. Esa operación la controlaré manualmente.

Implementa exclusivamente esta tarea. No avances a la siguiente fase del roadmap."


y me dio esta respuesta: 
cd "C:\Users\kevin\OneDrive\Documents\Documents\Software Development\DIPLOMA\bank2.0\Paylinkhub-KevinHurtado\PayLinkHub"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

\Paylinkhub-KevinHurtado\\PayLinkHub'
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [42988] using StatReload
INFO:     Started server process [38476]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:62424 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:58055 - "GET /json/version HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:56983 - "GET /health?utm_source=chatgpt.com HTTP/1.1"
 200 OK
INFO:     127.0.0.1:56983 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:56334 - "GET /docs?utm_source=chatgpt.com HTTP/1.1" 200 OK
INFO:     127.0.0.1:56334 - "GET /openapi.json HTTP/1.1" 200 OK

######################################################################

prompt #2: 

Implementa exclusivamente la Fase 2 de PayLinkHub.

**Objetivo:** definir el contrato canónico mediante modelos Pydantic y crear el endpoint:

`GET /api/v1/dashboard/{customerId}`

### 1. Modelos Pydantic

En `app/models/dashboard.py`, implementa estos modelos:

- `Customer`
  - `id`
  - `full_name`
  - `email`
  - `phone`

- `Transaction`
  - `id`
  - `products: list[str]`
  - `quantity: int`
  - `total_usd: Decimal`

- `ProvidersStatus`
  - `core: Literal["ok", "degraded", "unavailable"]`
  - `pagos: Literal["ok", "degraded", "unavailable"]`
  - `fx: Literal["ok", "degraded", "unavailable"]`

- `Dashboard`
  - `customer: Customer | None`
  - `transactions: list[Transaction]`
  - `partial: bool`
  - `warnings: list[str]`
  - `providers: ProvidersStatus`

### 2. Endpoint

En `app/routes/dashboard.py`:

- Implementa `GET /{customerId}`.
- Devuelve una instancia del modelo `Dashboard`.
- Utiliza datos fijos de prueba.
- El ID del cliente debe corresponder al `customerId` recibido.
- Utiliza `response_model=Dashboard`.

### 3. Integración

En `app/main.py`:

- Registra el router bajo el prefijo `/api/v1/dashboard`.
- Conserva el endpoint `/health` existente.

### 4. Restricciones

- No conectes proveedores externos todavía.
- No implementes lógica de reintentos, caché ni circuit breaker.
- No modifiques la estructura del proyecto.
- No instales dependencias adicionales.
- No modifiques archivos fuera de los indicados, salvo que sea estrictamente necesario para integrar el router.
- Mantén el contrato independiente de las estructuras originales de los proveedores.

### 5. Validación

Comprueba:

1. La aplicación inicia correctamente.
2. `/health` continúa respondiendo HTTP 200.
3. `/api/v1/dashboard/123` responde HTTP 200.
4. La respuesta cumple exactamente el modelo canónico.
5. `/docs` muestra el endpoint y su esquema.

Al terminar, informa los archivos modificados y los resultados de las pruebas. No hagas commits ni avances a la siguiente fase.

##############################################################################

Contrato canonico: 

Decisiones de diseño

Conservo únicamente los datos necesarios del cliente y sus transacciones, descartando información sensible como contraseñas, números de seguro social y datos bancarios.

También incorporé partial y warnings para informar cuándo algún proveedor falla sin impedir que se entreguen los datos disponibles. Finalmente, providers permite identificar individualmente el estado de cada integración.

propuesta de contrato: 
{
  "customer": {
    "id": 1,
    "full_name": "Emily Johnson",
    "email": "emily.johnson@example.com",
    "phone": "555-123-4567"
  },
  "transactions": [
    {
      "id": 1,
      "products": [
        "Essence Mascara Lash Princess",
        "Eyeshadow Palette"
      ],
      "quantity": 3,
      "total_usd": 25.98
    }
  ],
  "partial": false,
  "warnings": [],
  "providers": {
    "core": "ok",
    "pagos": "ok",
    "fx": "ok"
  }
}
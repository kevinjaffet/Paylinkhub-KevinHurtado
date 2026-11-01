# PayLinkHub

# PayLinkHub — Guía rápida de instalación y ejecución

Esta guía explica cómo instalar, configurar y ejecutar PayLinkHub localmente en Windows, Linux o macOS.

## 1. Requisitos previos

Antes de comenzar, asegúrate de tener instalados:

- **Git:** para clonar el repositorio.
- **Python:** para ejecutar la aplicación.
- **Conexión a Internet:** necesaria para instalar dependencias y consultar los proveedores externos.
- **Terminal:** PowerShell, CMD, Bash o Zsh.

Verifica las instalaciones:

```bash
git --version
python --version
```

En Windows también puedes utilizar:

```powershell
py --version
```

## 2. Clonar el repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/kevinjaffet/Paylinkhub-KevinHurtado.git
cd Paylinkhub-KevinHurtado
```

## 3. Crear un entorno virtual

El entorno virtual mantiene las dependencias del proyecto aisladas de las demás instalaciones de Python.

**Windows (PowerShell):**

```powershell
py -m venv .venv
```

**Linux / macOS:**

```bash
python3 -m venv .venv
```

## 4. Activar el entorno virtual

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, puedes ejecutar Python directamente desde el entorno virtual.

**Linux / macOS:**

```bash
source .venv/bin/activate
```

## 5. Instalar las dependencias

Con el entorno virtual activado:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Esto instalará las dependencias necesarias para ejecutar el backend y las pruebas.

## 6. Configurar las variables de entorno

Crea el archivo `.env` utilizando `.env.example` como plantilla.

**Windows:**

```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**

```bash
cp .env.example .env
```

Revisa el archivo `.env` y verifica que las URL de los proveedores y demás configuraciones estén correctamente definidas.

No publiques ni compartas el archivo `.env`. Este contiene la configuración local del proyecto.

## 7. Ejecutar la aplicación

Desde la carpeta raíz del proyecto, ejecuta:

```bash
python -m uvicorn app.main:app --reload
```

Si la aplicación inicia correctamente, estará disponible en:

| Servicio | Dirección |
|---|---|
| Panel web | http://127.0.0.1:8000/ |
| API Dashboard | http://127.0.0.1:8000/api/v1/dashboard/1 |
| Documentación interactiva de la API | http://127.0.0.1:8000/docs |

Mantén abierta la terminal mientras utilizas la aplicación.

## 8. Probar el endpoint

Abre una segunda terminal y ejecuta:

```bash
curl http://127.0.0.1:8000/api/v1/dashboard/1
```

La API debe devolver una respuesta JSON con:

- Información del cliente.
- Transacciones.
- Estado de los proveedores CORE, PAGOS y FX.
- Indicador de respuesta parcial y advertencias, cuando corresponda.
- Tasas de cambio EUR y GBP cuando FX esté disponible.

## 9. Ejecutar las pruebas automatizadas

Desde la carpeta raíz del proyecto:

```bash
python -m pytest tests -v
```

Verifica que todas las pruebas finalicen correctamente.

## 10. Detener la aplicación

Para detener el servidor, presiona:

```text
CTRL + C
```

Para salir del entorno virtual:

```bash
deactivate
```

---

## Solución de problemas

| Problema | Solución recomendada |
|---|---|
| Python no se reconoce | Instalar Python y habilitar su integración con PATH |
| Git no se reconoce | Instalar Git |
| Falla la instalación de dependencias | Verificar Python, conexión a Internet y `requirements.txt` |
| Falta la configuración | Comprobar que `.env` existe y corresponde a `.env.example` |
| El puerto 8000 está ocupado | Detener el proceso que lo utiliza o configurar otro puerto |
| La API devuelve datos parciales | Revisar la disponibilidad de los proveedores y los logs |
| El panel no carga | Verificar que el servidor FastAPI inició correctamente |

## Notas importantes

- No se requiere instalar una base de datos.
- Las integraciones con proveedores externos necesitan conexión a Internet.
- Las tasas de cambio dependen de la disponibilidad del proveedor FX.
- INESTABLE se utiliza para simular fallos de proveedores.
- El proyecto está diseñado para ejecutarse localmente con la configuración proporcionada.

Para consultar la arquitectura, las decisiones técnicas y los ejemplos completos de la API, revisa `README.md`.

#########################################################################

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

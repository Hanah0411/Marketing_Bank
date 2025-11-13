# Bank Marketing Predictor

Sistema de predicción para campañas bancarias con dashboard interactivo y API REST.

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema de predicción para determinar si un cliente aceptará un depósito a plazo fijo en una campaña bancaria. Incluye:

- API REST con FastAPI
- Dashboard interactivo con Dash
- Base de datos PostgreSQL
- Modelo de machine learning pre-entrenado
- Sistema de logging y monitoreo

## 🛠️ Requisitos del Sistema

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)
- Sistema operativo: Windows/Linux/MacOS

## ⚙️ Instalación

1. Clonar el repositorio:

    ```bash
    git clone [URL_DEL_REPOSITORIO]
    cd bank_marketing_local
    ```

2. Crear y activar un entorno virtual:

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/MacOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Instalar dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configurar la base de datos:
    
    - Crear una base de datos PostgreSQL llamada 'bank_marketing'
    - Ejecutar el script de inicialización:

    ```bash
    psql -U postgres -d bank_marketing -f app/database/bank_marketing_schema.sql
    ```

5. Configurar las variables de entorno:
    
    - Copiar el archivo `config.py` y ajustar los valores según tu entorno:

    ```python
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'tu_contraseña',
        'dbname': 'bank_marketing',
        'port': 5432
    }
```

## 🚀 Ejecución del Proyecto

### Iniciar el Backend (API)

```bash
# Desde la raíz del proyecto
uvicorn app.main:app --reload --port 8000
```

La API estará disponible en:

- API: [http://localhost:8000](http://localhost:8000)
- Documentación: [http://localhost:8000/docs](http://localhost:8000/docs)

### Iniciar el Frontend (Dashboard)

```bash
# En otra terminal, desde la raíz del proyecto
python -m app.dashboards.dashboard
```

El dashboard estará disponible en:

- [http://localhost:8050](http://localhost:8050)

## 🧪 Tests

Para ejecutar los tests:

```bash
# Desde la raíz del proyecto
pytest
```

Tests específicos:

```bash
# Tests de API
pytest app/tests/test_api.py

# Tests de conexión a base de datos
pytest app/tests/test_db_connection.py
```

## 📁 Estructura del Proyecto

```
bank_marketing_local/
├── app/
│   ├── controllers/     # Lógica de negocio
│   ├── dashboards/      # Dashboard y visualizaciones
│   ├── data/           # Datos y recursos
│   ├── database/       # Scripts SQL y modelos
│   ├── models/         # Schemas y modelos de datos
│   ├── routes/         # Endpoints de la API
│   ├── services/       # Servicios (preprocesamiento, entrenamiento)
│   ├── static/         # Recursos estáticos
│   ├── templates/      # Plantillas HTML
│   └── tests/          # Tests unitarios e integración
├── logs/               # Archivos de log
├── config.py           # Configuración global
├── conftest.py        # Configuración de tests
└── requirements.txt    # Dependencias del proyecto
```

## 🔍 Uso de la API

### Realizar una Predicción

```python
import requests

url = "http://localhost:8000/api/predict"
data = {
    "age": 45,
    "job": "management",
    "marital": "married",
    "education": "tertiary",
    "default": "no",
    "balance": 1200.0,
    "housing": "yes",
    "loan": "no",
    "contact": "cellular",
    "day": 12,
    "month": "may",
    "duration": 300,
    "campaign": 2,
    "pdays": -1,
    "previous": 0,
    "poutcome": "unknown"
}

response = requests.post(url, json=data)
prediction = response.json()
print(prediction)
```

## 📊 Uso del Dashboard

El dashboard incluye:

- Métricas en tiempo real
- Matriz de confusión
- Distribución de edades
- Histórico de predicciones
- Tabla de últimas predicciones
- Actualización automática cada 30 segundos

## 👥 Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## 📧 Contacto

Equipo de ML - [URL_DEL_REPOSITORIO]

```powershell
# instalar dependencias si es necesario
pip install -r requirements.txt

# ejecutar todos los tests
pytest -q

# ejecutar un test específico
pytest app/tests/test_db_connection.py -q
```

Alternativa (ejecución de un único archivo como módulo):

```powershell
python -m app.tests.test_db_connection
```

Si por alguna razón los imports fallan, una solución temporal desde PowerShell es exportar
la raíz del proyecto en `PYTHONPATH` para esa invocación:

```powershell
$env:PYTHONPATH = '.'; pytest -q
```

Nota: Añadimos un archivo `conftest.py` en la raíz del proyecto que inserta
la raíz en `sys.path` para ayudar a que pytest detecte el paquete `app`.

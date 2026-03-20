# Biotica Nexus 🌿

**Plataforma de Monitoreo de Sensores Ambientales en Tiempo Real**

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Interactivo-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Chart.js](https://img.shields.io/badge/Charts-Chart.js-yellow)

## 📋 Descripción

Biotica Nexus es una plataforma completa para la gestión y monitoreo de sensores ambientales en campo. Incluye un backend robusto con API RESTful y un dashboard interactivo para visualización en tiempo real.

## 🚀 Características Principales

### Backend (FastAPI + SQLAlchemy)
- ✅ API RESTful con documentación automática (Swagger/Redoc)
- ✅ Modelos de datos: Sensores y Lecturas
- ✅ Operaciones CRUD completas
- ✅ Validación de datos con Pydantic v2
- ✅ Base de datos SQLite con relaciones
- ✅ Manejo de errores y respuestas HTTP apropiadas

### Frontend (Dashboard Interactivo)
- ✅ Dashboard moderno con Tailwind CSS
- ✅ Gráficos en tiempo real con Chart.js
- ✅ Tarjetas de resumen de métricas
- ✅ Tabla interactiva de sensores
- ✅ Actualización automática cada 30 segundos
- ✅ Diseño responsive y mobile-friendly

## 🏗️ Arquitectura del Proyecto

```
biotica_nexus/
├── app/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── database.py          # Configuración de base de datos
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Esquemas Pydantic
│   └── crud.py              # Operaciones CRUD
├── static/
│   ├── index.html           # Dashboard HTML
│   └── dashboard.js         # Lógica JavaScript del dashboard
├── test_data.py             # Script de datos de prueba
├── biotica_nexus.db         # Base de datos SQLite
├── requirements.txt         # Dependencias Python
└── README.md                # Este archivo
```

## 🛠️ Instalación y Configuración

### 1. Requisitos Previos
- Python 3.8+
- Git

### 2. Clonar el Repositorio
```bash
git clone https://github.com/hashernom/Prueba-roo.git
cd Prueba-roo
```

### 3. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install fastapi uvicorn sqlalchemy
```

### 5. Inicializar Base de Datos
```bash
# Crear tablas y datos de prueba
python test_data.py
```

### 6. Ejecutar Servidor
```bash
# Iniciar servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Acceso a la Aplicación

Una vez ejecutado el servidor, accede a:

- **Dashboard Interactivo**: http://localhost:8000/dashboard
- **Documentación API (Swagger)**: http://localhost:8000/docs
- **Documentación API (Redoc)**: http://localhost:8000/redoc
- **Endpoint de Salud**: http://localhost:8000/health
- **API Raíz**: http://localhost:8000/

## 📊 Endpoints de la API

### Sensores
- `GET /sensores/` - Listar todos los sensores
- `GET /sensores/{id}` - Obtener sensor específico
- `POST /sensores/` - Crear nuevo sensor
- `PUT /sensores/{id}` - Actualizar sensor
- `DELETE /sensores/{id}` - Eliminar sensor
- `GET /sensores/{id}/lecturas/` - Lecturas de un sensor
- `GET /sensores/{id}/estadisticas/` - Estadísticas del sensor

### Lecturas
- `GET /lecturas/` - Listar todas las lecturas
- `POST /lecturas/` - Registrar nueva lectura
- `GET /lecturas/{id}` - Obtener lectura específica

## 🎨 Características del Dashboard

### 1. Tarjetas de Resumen
- **Total de Sensores**: Número de sensores registrados
- **Lecturas Recientes**: Cantidad de lecturas en últimas 24h
- **Tipos de Sensores**: Diversidad de categorías
- **Valor Promedio**: Media de todas las lecturas

### 2. Gráficos Interactivos
- **Gráfico de Líneas**: Últimas 20 lecturas en tiempo real
- **Gráfico de Dona**: Distribución de sensores por estado

### 3. Tabla de Sensores
- Lista completa con ID, tipo, ubicación y estado
- Indicadores visuales de estado (activo, mantenimiento, inactivo)
- Conteo de lecturas por sensor
- Tiempo desde última lectura

### 4. Funcionalidades Avanzadas
- **Actualización Automática**: Cada 30 segundos
- **Refresco Manual**: Botón de actualización
- **Filtros Temporales**: Día, semana, mes (gráficos)
- **Manejo de Errores**: Mensajes descriptivos

## 🧪 Datos de Prueba

El proyecto incluye un script `test_data.py` que crea automáticamente:
- 3 sensores de diferentes tipos (temperatura, humedad, presión)
- 10 lecturas distribuidas aleatoriamente
- Estadísticas calculadas automáticamente

Para ejecutar:
```bash
python test_data.py
```

## 🔧 Personalización

### Agregar Nuevos Tipos de Sensores
1. Modificar `app/models.py` para agregar nuevos campos
2. Actualizar `app/schemas.py` con validaciones
3. Extender `app/crud.py` con operaciones específicas

### Modificar el Dashboard
1. Editar `static/index.html` para cambios en la estructura
2. Modificar `static/dashboard.js` para lógica personalizada
3. Actualizar estilos en el mismo HTML (Tailwind CSS)

## 📈 Roadmap Futuro

- [ ] Autenticación y autorización (JWT)
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Exportación de datos (CSV, Excel)
- [ ] Panel de administración avanzado
- [ ] Integración con sensores IoT reales
- [ ] Alertas y umbrales configurables
- [ ] Dashboard multi-usuario

## 🤝 Contribución

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Hashernom** - *Desarrollo inicial* - [@hashernom](https://github.com/hashernom)

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) por el increíble framework
- [Tailwind CSS](https://tailwindcss.com/) por los estilos utilitarios
- [Chart.js](https://www.chartjs.org/) por las visualizaciones interactivas
- [SQLAlchemy](https://www.sqlalchemy.org/) por el ORM poderoso

---

**Biotica Nexus** - Monitoreo ambiental inteligente para un futuro sostenible 🌍
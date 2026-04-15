# Fayni - Gestión Financiera Familiar

---

Aplicación web para registrar, visualizar y controlar ingresos, egresos, donaciones y saldos compartidos dentro de un entorno familiar.

## Nota de privacidad

La versión pública del proyecto no debe incluir datos financieros reales ni secretos locales. Para subirlo a GitHub, usa variables de entorno y credenciales de demostración.

## Credenciales de ejemplo para documentación

| Servicio        | Usuario / Email          | Contraseña                 |
|-----------------|--------------------------|----------------------------|
| **pgAdmin**     | `demo.admin@fayni.app`   | `definida en .env`         |
| **App Admin**   | `demo.admin@fayni.app`   | `DemoAdmin123!`            |
| **App Familia** | `demo.family@fayni.app`  | `DemoFamily123!`           |

---

## Levantar con Docker

```bash
cd /Users/camex/telefonica-applications/app-fayni
cp .env.example .env
docker-compose up --build
```

| Servicio   | URL                          | Descripción           |
|------------|------------------------------|-----------------------|
| Frontend   | http://localhost:3000        | App VueJS             |
| API docs   | http://localhost:8000/docs   | Swagger FastAPI       |
| pgAdmin    | http://localhost:5050        | Gestor de BD          |

---

## Vista rápida

### Flujo principal

![Fayni App](docs/fayni-app.gif)

### Registro de movimientos

![Operación Movimiento](docs/OperaciónMovimiento.gif)

### Exportación de reportes

![Exportación de Ingresos](docs/Exportación%20de%20Ingresos.gif)

---

## Desarrollo local Backend (sin Docker)

```bash
cd backend
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt

DATABASE_URL=postgresql://fayni_user:change-me-demo-password@localhost:5432/fayni_db \
  uvicorn app.main:app --reload
```

---

## Arquitectura

**Stack:** FastAPI + VueJS 3 + PostgreSQL 15 + Docker

### Backend (FastAPI)

| Módulo          | Descripción                                       |
|-----------------|---------------------------------------------------|
| `auth/jwt.py`   | Autenticación JWT con bcrypt                      |
| `models/`       | Usuario, Grupo, Tipo, Movimiento (SQLAlchemy ORM) |
| `routers/auth`  | Login, crear/listar/desactivar usuarios           |
| `routers/movimientos` | CRUD de movimientos + recalculo de saldo    |
| `routers/catalogos`  | CRUD de Grupos y Tipos                       |
| `routers/dashboard` | KPIs, evolución mensual, por grupo, servicios casa, top egresos |
| `seeds/seed.py` | Carga inicial de tipos, grupos, usuarios y movimientos base |

### Base de Datos (normalizada)

| Tabla        | Campos clave                                       |
|--------------|----------------------------------------------------|
| `usuarios`   | id, nombre, email, password_hash, rol, activo      |
| `tipos`      | id, nombre → INGRESO / EGRESO / DONACIÓN           |
| `grupos`     | id, nombre, descripcion, icono, color              |
| `movimientos`| id, fecha, descripcion, monto_ingreso, monto_egreso, saldo, grupo_id, tipo_id |

### Grupos / Categorías cargados

| Icono | Nombre             | Descripción                    |
|-------|--------------------|--------------------------------|
| 🎁    | Donación           | Donaciones recibidas           |
| 🏦    | CuentaAhorro       | BBVA, BCP, Banco Nación        |
| 🏥    | ClínicaNiños       | Atención médica de los niños   |
| 💡    | ServicioCasa       | Luz, agua y servicios del hogar|
| 🪦    | Mausoleo           | Gastos de mausoleo/cementerio  |
| ⛪    | MisaMes            | Gastos de misa mensual         |
| 🧠    | AtenciónPsicóloga  | Consultas psicológicas         |
| 🚌    | Movilidad          | Transporte / movilidad         |
| 🛒    | Alimentos          | Compras de alimentos y víveres |
| 💊    | AtenciónClínica    | Atención médica general        |
| 📚    | Escolaridad        | Colegios, útiles, mensualidades|
| ⚽    | Deporte            | Deportes y actividades físicas |
| ❤️    | Salud              | Salud general                  |
| 💰    | MensualidadGuanilo | Mensualidad de Guanilo p/niños |
| ⚖️    | Abogado            | Gastos legales                 |
| 👕    | Vestimenta         | Ropa y vestimenta              |

### Frontend (VueJS 3)

**Rol Administrador:**
- Dashboard con filtro de fechas
- Gráfico de barras: Evolución mensual ingresos vs egresos
- Gráfico donut: Egresos por categoría
- Gráfico de línea: Servicios de casa (luz y agua)
- Tabla: Top 5 categorías de egreso
- Tabla: Resumen por grupo con balance
- Gestión completa de movimientos (filtros, crear, editar, eliminar)
- Gestión de usuarios (crear, desactivar, asignar rol)
- Catálogo de grupos (icono, color, descripción)

**Rol Familia:**
- Dashboard con KPIs: ingresos, egresos, balance, saldo actual
- Gráfico de línea: Evolución ingresos vs egresos
- Gráfico de torta: ¿En qué gasté más?
- Tabla: Últimos 10 movimientos
- Historial de movimientos con filtros
- Formulario para registrar nuevo movimiento

---

## Estructura de archivos

```
app-fayni/
├── docker-compose.yml
├── .env
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── venv/                    ← virtualenv Python (activar para desarrollo local)
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── auth/jwt.py          ← JWT + bcrypt
│       ├── models/              ← Usuario, Grupo, Tipo, Movimiento
│       ├── schemas/             ← Pydantic schemas
│       ├── routers/             ← auth, movimientos, catalogos, dashboard
│       └── seeds/seed.py        ← datos iniciales de carga
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.js
        ├── router/index.js      ← rutas con guards por rol
        ├── stores/auth.js       ← Pinia store JWT
        ├── services/api.js      ← Axios con interceptor
        ├── views/
        │   ├── Login.vue
        │   ├── Layout.vue       ← sidebar + topbar
        │   ├── admin/
        │   │   ├── Dashboard.vue
        │   │   ├── Movimientos.vue
        │   │   ├── Usuarios.vue
        │   │   └── Catalogos.vue
        │   └── familia/
        │       ├── Dashboard.vue
        │       ├── Movimientos.vue
        │       └── NuevoMovimiento.vue
        └── components/
            └── movimientos/MovimientoForm.vue
```

---

## Ideas para agregar a futuro

1. **Presupuesto mensual por categoría** — alertas cuando superas el límite (ej: Alimentos > S/500)
2. **Notificaciones/recordatorios** — vencimiento de pagos fijos (agua, luz, mensualidad)
3. **Exportar a PDF/Excel** — reporte mensual descargable
4. **Adjuntar comprobantes** — foto de boleta o recibo por movimiento
5. **Metas de ahorro** — "Queremos ahorrar S/1000 para diciembre" con barra de progreso
6. **Notas por movimiento** — campo libre para contexto adicional

"""
Script de seed: crea datos iniciales y carga un dataset de demostración.
Ejecutar: python -m app.seeds.seed
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import date
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models import Usuario, Grupo, Tipo, Movimiento
from app.auth.jwt import hash_password

# ── Crear tablas ────────────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

TIPOS = ["INGRESO", "EGRESO", "DONACIÓN"]

GRUPOS = [
    {"nombre": "Donación",          "descripcion": "Donaciones recibidas",              "icono": "🎁",  "color": "#6366f1"},
    {"nombre": "CuentaAhorro",      "descripcion": "Cuentas de ahorro (BBVA, BCP...)",  "icono": "🏦",  "color": "#0ea5e9"},
    {"nombre": "ClínicaNiños",      "descripcion": "Atención médica de los niños",      "icono": "🏥",  "color": "#f43f5e"},
    {"nombre": "ServicioCasa",      "descripcion": "Luz, agua y servicios del hogar",   "icono": "💡",  "color": "#f59e0b"},
    {"nombre": "Mausoleo",          "descripcion": "Gastos de mausoleo/cementerio",     "icono": "🪦",  "color": "#78716c"},
    {"nombre": "MisaMes",           "descripcion": "Gastos de misa mensual",            "icono": "⛪",  "color": "#a78bfa"},
    {"nombre": "AtenciónPsicóloga", "descripcion": "Consultas psicológicas",            "icono": "🧠",  "color": "#34d399"},
    {"nombre": "Movilidad",         "descripcion": "Movilidad / transporte",            "icono": "🚌",  "color": "#fb923c"},
    {"nombre": "Alimentos",         "descripcion": "Compras de alimentos y víveres",    "icono": "🛒",  "color": "#22c55e"},
    {"nombre": "AtenciónClínica",   "descripcion": "Atención médica general",           "icono": "💊",  "color": "#ec4899"},
    {"nombre": "Escolaridad",       "descripcion": "Colegios, útiles, mensualidades",   "icono": "📚",  "color": "#3b82f6"},
    {"nombre": "Deporte",           "descripcion": "Deportes y actividades físicas",    "icono": "⚽",  "color": "#14b8a6"},
    {"nombre": "Salud",             "descripcion": "Salud general",                     "icono": "❤️",  "color": "#ef4444"},
    {"nombre": "MensualidadGuanilo","descripcion": "Mensualidad de Guanilo p/ los niños","icono":"💰", "color": "#84cc16"},
    {"nombre": "Abogado",           "descripcion": "Gastos legales / abogado",          "icono": "⚖️",  "color": "#64748b"},
    {"nombre": "Vestimenta",        "descripcion": "Ropa y vestimenta de los niños",    "icono": "👕",  "color": "#f472b6"},
]

DATOS_DEMO = [
    ("2025-10-03", "Aporte familiar inicial", 1200, 0, "CuentaAhorro", "INGRESO"),
    ("2025-10-04", "Donacion de apoyo vecinal", 350, 0, "Donación", "DONACIÓN"),
    ("2025-10-05", "Compra quincenal de viveres", 0, 185.40, "Alimentos", "EGRESO"),
    ("2025-10-06", "Pago de agua", 0, 42.00, "ServicioCasa", "EGRESO"),
    ("2025-10-08", "Pago de luz", 0, 68.50, "ServicioCasa", "EGRESO"),
    ("2025-10-10", "Recarga de transporte escolar", 0, 120.00, "Movilidad", "EGRESO"),
    ("2025-10-12", "Mensualidad de apoyo familiar", 700, 0, "MensualidadGuanilo", "INGRESO"),
    ("2025-10-14", "Utiles y materiales escolares", 0, 96.70, "Escolaridad", "EGRESO"),
    ("2025-10-18", "Revision medica general", 0, 85.00, "Salud", "EGRESO"),
    ("2025-10-22", "Compra de ropa para temporada", 0, 140.00, "Vestimenta", "EGRESO"),
    ("2025-10-28", "Ingreso extraordinario de ahorro", 500, 0, "CuentaAhorro", "INGRESO"),
    ("2025-11-02", "Compra mensual de mercado", 0, 214.60, "Alimentos", "EGRESO"),
    ("2025-11-04", "Pago de internet y servicios", 0, 89.90, "ServicioCasa", "EGRESO"),
    ("2025-11-05", "Aporte solidario de familia amiga", 280, 0, "Donación", "DONACIÓN"),
    ("2025-11-08", "Control pediatrico", 0, 75.00, "ClínicaNiños", "EGRESO"),
    ("2025-11-10", "Mensualidad de apoyo familiar", 700, 0, "MensualidadGuanilo", "INGRESO"),
    ("2025-11-12", "Pago de movilidad del mes", 0, 200.00, "Movilidad", "EGRESO"),
    ("2025-11-16", "Material escolar complementario", 0, 48.00, "Escolaridad", "EGRESO"),
    ("2025-11-20", "Consulta psicologica de seguimiento", 0, 60.00, "AtenciónPsicóloga", "EGRESO"),
    ("2025-11-25", "Cuota actividad deportiva", 0, 70.00, "Deporte", "EGRESO"),
    ("2025-12-01", "Transferencia a cuenta de ahorro", 900, 0, "CuentaAhorro", "INGRESO"),
    ("2025-12-03", "Compra de viveres y limpieza", 0, 245.80, "Alimentos", "EGRESO"),
    ("2025-12-05", "Pago de agua", 0, 39.20, "ServicioCasa", "EGRESO"),
    ("2025-12-06", "Pago de luz", 0, 72.40, "ServicioCasa", "EGRESO"),
    ("2025-12-09", "Donacion para cierre de anio", 450, 0, "Donación", "DONACIÓN"),
    ("2025-12-12", "Mensualidad de apoyo familiar", 700, 0, "MensualidadGuanilo", "INGRESO"),
    ("2025-12-14", "Consulta medica general", 0, 95.00, "AtenciónClínica", "EGRESO"),
    ("2025-12-18", "Ropa y calzado escolar", 0, 180.00, "Vestimenta", "EGRESO"),
    ("2025-12-21", "Pago de asesoria legal administrativa", 0, 180.00, "Abogado", "EGRESO"),
    ("2025-12-27", "Compra para reunion familiar", 0, 130.00, "Alimentos", "EGRESO"),
    ("2026-01-03", "Aporte familiar de inicio de anio", 1100, 0, "CuentaAhorro", "INGRESO"),
    ("2026-01-05", "Pago de servicios del hogar", 0, 115.30, "ServicioCasa", "EGRESO"),
    ("2026-01-08", "Matricula escolar", 0, 320.00, "Escolaridad", "EGRESO"),
    ("2026-01-10", "Mensualidad de apoyo familiar", 800, 0, "MensualidadGuanilo", "INGRESO"),
    ("2026-01-12", "Compra de alimentos del mes", 0, 228.50, "Alimentos", "EGRESO"),
    ("2026-01-15", "Movilidad escolar", 0, 200.00, "Movilidad", "EGRESO"),
    ("2026-01-19", "Chequeo de salud preventiva", 0, 88.00, "Salud", "EGRESO"),
    ("2026-01-24", "Donacion de apoyo comunitario", 300, 0, "Donación", "DONACIÓN"),
    ("2026-02-02", "Deposito en cuenta de ahorro", 950, 0, "CuentaAhorro", "INGRESO"),
    ("2026-02-04", "Pago de agua y luz", 0, 121.70, "ServicioCasa", "EGRESO"),
    ("2026-02-07", "Compra semanal de mercado", 0, 176.20, "Alimentos", "EGRESO"),
    ("2026-02-09", "Mensualidad de apoyo familiar", 800, 0, "MensualidadGuanilo", "INGRESO"),
    ("2026-02-11", "Uniforme y utiles", 0, 210.00, "Escolaridad", "EGRESO"),
    ("2026-02-15", "Consulta dental", 0, 65.00, "Salud", "EGRESO"),
    ("2026-02-18", "Inscripcion deportiva", 0, 80.00, "Deporte", "EGRESO"),
    ("2026-02-22", "Aporte solidario de familiar", 240, 0, "Donación", "DONACIÓN"),
    ("2026-02-25", "Traslado y movilidad", 0, 200.00, "Movilidad", "EGRESO"),
    ("2026-03-01", "Ingreso mensual a ahorro", 1000, 0, "CuentaAhorro", "INGRESO"),
    ("2026-03-03", "Pago de servicios", 0, 118.40, "ServicioCasa", "EGRESO"),
    ("2026-03-06", "Compra de alimentos y limpieza", 0, 236.90, "Alimentos", "EGRESO"),
    ("2026-03-09", "Mensualidad de apoyo familiar", 800, 0, "MensualidadGuanilo", "INGRESO"),
    ("2026-03-12", "Consulta medica y medicamentos", 0, 142.50, "AtenciónClínica", "EGRESO"),
    ("2026-03-15", "Pago de asesoria documentaria", 0, 120.00, "Abogado", "EGRESO"),
    ("2026-03-18", "Material escolar adicional", 0, 52.00, "Escolaridad", "EGRESO"),
    ("2026-03-21", "Apoyo extraordinario de donante", 380, 0, "Donación", "DONACIÓN"),
    ("2026-03-24", "Compra de ropa y articulos personales", 0, 155.00, "Vestimenta", "EGRESO"),
    ("2026-03-28", "Movilidad del cierre de mes", 0, 200.00, "Movilidad", "EGRESO"),
]


def seed():
    db: Session = SessionLocal()
    try:
        # Tipos
        tipo_objs = {}
        for nombre in TIPOS:
            t = db.query(Tipo).filter(Tipo.nombre == nombre).first()
            if not t:
                t = Tipo(nombre=nombre)
                db.add(t)
                db.flush()
            tipo_objs[nombre] = t

        # Grupos
        grupo_objs = {}
        for g in GRUPOS:
            obj = db.query(Grupo).filter(Grupo.nombre == g["nombre"]).first()
            if not obj:
                obj = Grupo(**g)
                db.add(obj)
                db.flush()
            grupo_objs[g["nombre"]] = obj

        # Usuarios
        admin = db.query(Usuario).filter(Usuario.email == "demo.admin@fayni.app").first()
        if not admin:
            db.add(Usuario(
                nombre="Demo Admin",
                email="demo.admin@fayni.app",
                password_hash=hash_password("DemoAdmin123!"),
                rol="admin",
            ))

        familia = db.query(Usuario).filter(Usuario.email == "demo.family@fayni.app").first()
        if not familia:
            db.add(Usuario(
                nombre="Demo Familia",
                email="demo.family@fayni.app",
                password_hash=hash_password("DemoFamily123!"),
                rol="familia",
            ))

        db.commit()

        # Movimientos — solo inserta si la tabla está vacía (primera vez)
        conteo_actual = db.query(Movimiento).count()
        if conteo_actual == 0:
            saldo = 0.0
            for row in DATOS_DEMO:
                fecha_str, desc, ingreso, egreso, grupo_nombre, tipo_nombre = row
                saldo += ingreso - egreso
                m = Movimiento(
                    fecha=date.fromisoformat(fecha_str),
                    descripcion=desc,
                    monto_ingreso=float(ingreso),
                    monto_egreso=float(egreso),
                    saldo=round(saldo, 2),
                    grupo_id=grupo_objs[grupo_nombre].id,
                    tipo_id=tipo_objs[tipo_nombre].id,
                )
                db.add(m)
            db.commit()
            # Recalcular saldos en orden de inserción (id ASC)
            movs = db.query(Movimiento).order_by(Movimiento.id).all()
            saldo_acc = 0.0
            for mv in movs:
                saldo_acc += mv.monto_ingreso - mv.monto_egreso
                mv.saldo = round(saldo_acc, 2)
            db.commit()
            print(f"  → {len(DATOS_DEMO)} movimientos demo insertados. Saldo final: S/ {round(saldo_acc, 2)}")

        print("✅ Seed completado correctamente.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error en seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()

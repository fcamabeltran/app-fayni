from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, movimientos, catalogos, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fayni - Gestión de Gastos Familiares",
    description="API para gestión de ingresos, egresos y donaciones familiares",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movimientos.router)
app.include_router(catalogos.router)
app.include_router(dashboard.router)


@app.on_event("startup")
async def startup():
    from app.seeds.seed import seed
    try:
        seed()
    except Exception as e:
        print(f"Seed omitido: {e}")


@app.get("/")
def root():
    return {"message": "Fayni API v1.0 - OK"}

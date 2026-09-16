from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.database import Base, engine
from app.routers import auth, vehiculos

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MotoLab API",
    description="API RESTful para la gestion de taller de motocicletas y mantenimiento vehicular",
    version="1.0.0",
)


# Excepcion personalizada de dominio
class MotoLabDomainError(Exception):
    def __init__(self, mensaje: str):
        self.mensaje = mensaje


@app.exception_handler(MotoLabDomainError)
async def motolab_domain_exception_handler(
    request: Request, exc: MotoLabDomainError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Error de Dominio", "detalle": exc.mensaje},
    )


# Manejador generico catch-all para evitar exponer tracebacks
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Error interno del servidor",
            "detalle": "Ocurrio un error inesperado. Intente mas tarde.",
        },
    )


# Configuracion de plantillas
templates = Jinja2Templates(directory="app/templates")

# Routers de la API
app.include_router(auth.router)
app.include_router(vehiculos.router)


# Vista Principal (Home)
@app.get("/", response_class=HTMLResponse)
def vista_home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={}
    )


# Vista de Login
@app.get("/login", response_class=HTMLResponse)
def vista_login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )


# Vista de Dashboard / Gestion de Vehiculos
@app.get("/dashboard", response_class=HTMLResponse)
def vista_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={}
    )
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.database import Base, engine
from app.routers import auth, motos


# Crear las tablas de la base de datos al iniciar la aplicación.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="MotoLab API",
    description=(
        "Sistema de gestión de vehículos "
        "con autenticación JWT y roles"
    ),
    version="1.0.0",
)

templates = Jinja2Templates(
    directory="app/templates"
)


# Routers de la API REST.
app.include_router(
    auth.router,
    prefix="/api",
)

app.include_router(
    motos.router,
    prefix="/api",
)


# Vista de login.
@app.get(
    "/",
    tags=["Vistas Web"],
)
def view_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


# Vista principal.
@app.get(
    "/home",
    tags=["Vistas Web"],
)
def view_home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )


# Vista del dashboard.
@app.get(
    "/dashboard",
    tags=["Vistas Web"],
)
def view_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
    )


# Manejador general de errores inesperados.
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": (
                "Ocurrió un error inesperado "
                "en el servidor."
            )
        },
        status_code=500,
    )
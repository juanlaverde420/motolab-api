from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.database import Base, engine
from app.routers import auth, vehiculos

# Crear las tablas en la base de datos de forma automatica
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MotoLab API",
    description="API RESTful para la gestion de taller de motocicletas y mantenimiento vehicular",
    version="1.0.0",
)

# Configuracion de plantillas HTML con Jinja2
templates = Jinja2Templates(directory="app/templates")

# Incluir los routers de la API
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
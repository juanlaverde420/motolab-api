from app.database.database import Base, engine
from app.routers import auth, vehiculos
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# Crear las tablas en la base de datos de manera automática
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MotoLab API",
    description="Backend para la gestión de taller de motocicletas",
    version="1.0.0",
)

templates = Jinja2Templates(directory="app/templates")

# Incluir Routers
app.include_router(auth.router)
app.include_router(vehiculos.router)


# Ruta para Renderizar el Login
@app.get("/login", response_class=HTMLResponse, tags=["Interfaz"])
def vista_login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )


# Manejador genérico de excepciones
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
  return JSONResponse(
      status_code=500,
      content={
          "message": (
              "Ocurrió un error interno en el servidor. Intente más tarde."
          )
      },
  )
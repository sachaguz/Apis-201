
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import comics
from app.routers.comics import comics_db

app = FastAPI(
    title="API de Gestión de Ventas de Comics",
    description="Sistema para gestionar productos de cómics, sus ventas y sus disponibilidades",
    version="1.0.0"
)

# Montar archivos estáticos (CSS, JS, imágenes)
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/js", StaticFiles(directory="static/js"), name="js")

# Configurar motor de templates Jinja2
templates = Jinja2Templates(directory="templates")

# Incluir routers de la API
app.include_router(comics.router, prefix="/api/v1")


@app.get("/", tags=["Inicio"])
async def home(request: Request):
    """
    Página de inicio del sistema con estadísticas en tiempo real
    """
    # Importar base de datos de estudiantes
    from app.routers.comics import comics_db
   
    # Calcular estadísticas
    total = len(comics_db)
    activos = len([e for e in comics_db if e.get("activo", True)])
   
    # Calcular promedio general
    if total > 0:
        suma_promedios = sum([e.get("promedio", 0) for e in comics_db])
        promedio = suma_promedios / total
    else:
        promedio = 0
   
    # Datos que se pasan al template
    context = {
        "request": request,  # Obligatorio para Jinja2
        "titulo": "Sistema de Gestión de Ventas de Cómics",
        "descripcion": "API REST desarrollada con FastAPI",
        "stock_disponible": total,
        "proov_afiliados": activos,
        "prom_gen_ventas": f"${promedio:.2f}",
        "features": [
            {
                "icono": "[STK]",
                "titulo": "Stock",
                "descripcion": "Gestión completa de stock"
            },
            {
                "icono": "[SELL]",
                "titulo": "Ventas",
                "descripcion": "Control de Ventas"
            },
            {
                "icono": "[PROV]",
                "titulo": "Proveedores",
                "descripcion": "Proveedores que trabajan con nosotros"
            },
            {
                "icono": "[STATS]",
                "titulo": "Estadísticas",
                "descripcion": "Métricas de ventas mensuales"
            }
        ]
    }
   
    # Renderizar template con los datos
    return templates.TemplateResponse("home.html", context)
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/comics",
    tags=["Cómics"]
)

# Base de datos simulada de Cómics
comics_db = [
    {
        "id": 1, 
        "titulo": "The Amazing Spider-Man #1", 
        "stock": 15, 
        "precio": 4.99,
        "proveedores": ["Marvel Dist", "Diamond Comics"]
    },
    {
        "id": 2, 
        "titulo": "Batman: Year One", 
        "stock": 8, 
        "precio": 19.99,
        "proveedores": ["DC Entertainment"]
    },
    {
        "id": 3, 
        "titulo": "Saga Vol. 1", 
        "stock": 12, 
        "precio": 14.99,
        "proveedores": ["Image Distribution", "Global Books"]
    },  
    {
        "id": 4, 
        "titulo": "Watchmen", 
        "stock": 5, 
        "precio": 25.00,
        "proveedores": ["DC Entertainment"]
    },
    {
        "id": 5, 
        "titulo": "Invincible Ultimate Collection #1", 
        "stock": 3, 
        "precio": 35.50,
        "proveedores": ["Skybound", "Diamond Comics"]
    },
]

@router.get("/")
def listar_comics(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Lista el catálogo de cómics con paginación.
    """
    return {
        "total_catalogo": len(comics_db),
        "skip": skip,
        "limit": limit,
        "items": comics_db[skip : skip + limit]
    }

@router.get("/{comic_id}")
def obtener_comic(comic_id: int):
    """
    Busca un cómic específico por su ID.
    """
    # Usamos next para una búsqueda más eficiente en la lista
    for comic in comics_db:
        if comic["id"] == comic_id:
            return comic
    return {"error": "Cómic no encontrado"}
    
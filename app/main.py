from fastapi import FastAPI
from starlette.responses import RedirectResponse

# Importar los Routers
from .routes.order_router import order_route
from .routes.product_order_route import order_product_route

app = FastAPI()

# Evento de inicio del servidor
@app.on_event("startup")
async def startup_event():
    print("El servidor ha iniciado")

# Evento de cierre del servidor
@app.on_event("shutdown")
async def shutdown_event():
    print("El servidor se ha detenido")

# Ruta para redirigir a la documentación
@app.get("/")
async def docs():
    return RedirectResponse(url="/docs")




# Routers
app.include_router(order_route,prefix="/order", tags=["Orders"])
app.include_router(order_product_route,prefix="/order_product", tags=["Order Products"]) 





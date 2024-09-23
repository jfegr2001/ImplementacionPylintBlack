"""
Main application module for FastAPI.
Includes routes for orders and order products.
"""

# pylint: disable=E0401,W0613

# Standard imports
from contextlib import asynccontextmanager

# Third-party imports
from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse

# Local imports
from routes.order_router import order_route
from routes.product_order_route import order_product_route
from config.database import database as connection
from helpers.api_key_auth import get_api_key

app = FastAPI(
    title="Pylint microservice implementation",
    version="2.0",
    contact={
        "name": "Juan Felipe Giraldo",
    },
)

@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    """
    Handles the lifespan of the application, ensuring
    the database connection is open during the app's lifecycle.
    """
    if connection.is_closed():
        connection.connect()
    try:
        yield
    finally:
        if not connection.is_closed():
            connection.close()

# Create the FastAPI app instance with custom lifespan management
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def docs():
    """
    Redirects to the API documentation.
    """
    return RedirectResponse(url="/docs")

# Include routers for orders and order products
app.include_router(
    order_route, prefix="/order", tags=["Orders"], dependencies=[Depends(get_api_key)]
)
app.include_router(
    order_product_route,
    prefix="/product_order_route",
    tags=["Order Products"],
    dependencies=[Depends(get_api_key)],
)

# Ensure a final newline to comply with PEP 8

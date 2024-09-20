# pylint: disable=import-error

"""
This module defines the CRUD operations for the OrderProduct entity.
It includes routes to create, retrieve, update, and delete order-product relationships.
"""

from fastapi import APIRouter, Body

from ..models.product_order import ProductOrder  # Asegúrate de que el nombre sea correcto
from ..database import ProductOrderModel# Asegúrate de que el nombre sea correcto

order_product_route = APIRouter()

@order_product_route.get("/order_products", response_model=list[ProductOrder])
def get_order_products():
    """
    Retrieve all order-product relationships.
    """
    order_products = list(ProductOrderModel.select())
    return [ProductOrder(**order) for order in order_products]  # Convierte a instancias de ProductOrder

@order_product_route.get("/order_products/{order_product_id}", response_model=ProductOrder)
def get_order_product(order_product_id: int):
    """
    Retrieve an order-product relationship by its ID.
    """
    order_product = ProductOrderModel.get(ProductOrderModel.id == order_product_id)
    return ProductOrder(**order_product)  # Asegúrate de que devuelves un modelo de Pydantic

@order_product_route.post("/order_products", response_model=ProductOrder)
def create_order_product(order_product: ProductOrder = Body(...)):
    """
    Create a new order-product relationship.
    """
    new_order_product = ProductOrderModel.create(
        order_id=order_product.order_id,
        product_id=order_product.product_id,
        quantity=order_product.quantity
    )
    return ProductOrder(**new_order_product.__data__)  # Accede a los datos como diccionario

@order_product_route.put("/order_products/{order_product_id}", response_model=ProductOrder)
def update_order_product(order_product_id: int, order_product_data: ProductOrder):
    """
    Update an existing order-product relationship.
    """
    ProductOrderModel.update(**order_product_data.dict()).where(
        ProductOrderModel.id == order_product_id
    ).execute()
    updated_order_product = ProductOrderModel.get(ProductOrderModel.id == order_product_id)
    return ProductOrder(**updated_order_product)

@order_product_route.delete("/order_products/{order_product_id}")
def delete_order_product(order_product_id: int):
    """
    Delete an order-product relationship by its ID.
    """
    ProductOrderModel.delete().where(
        ProductOrderModel.id == order_product_id
    ).execute()
    return {"message": "Order-product relationship deleted"}

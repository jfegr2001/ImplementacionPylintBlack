"""
This module defines the routes for handling order-product relationships in the API.
"""

from fastapi import APIRouter, Body, HTTPException
from app.models.product_order import ProductOrder
from app.services.product_order_service import OrderProductService  # type: ignore

order_product_route = APIRouter()
# pylint: disable=no-value-for-parameter


@order_product_route.get("/order_products", response_model=list[ProductOrder])
def get_order_products():
    """
    Retrieve all order-product relationships.
    """
    try:
        order_products = OrderProductService.get_order_products()
        return {"order_products": order_products}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@order_product_route.get("/order_products/{order_product_id}", response_model=ProductOrder)
def get_order_product(order_product_id: int):
    """
    Retrieve an order-product relationship by its ID.
    """
    try:
        order_product = OrderProductService.get_order_product_by_id(order_product_id)
        if not order_product:
            raise HTTPException(
                status_code=404, detail="Order-product relationship not found"
            )
        return order_product
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid order-product ID"
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the order-product relationship"
        ) from exc


@order_product_route.post("/order_products", response_model=ProductOrder)
def create_order_product(order_product: ProductOrder = Body(...)):
    """
    Create a new order-product relationship.
    """
    try:
        order_product_instance = OrderProductService.create_order_product(
            order_id=order_product.order_id,
            product_id=order_product.product_id,
            quantity=order_product.quantity
        )
        return {
            "message": "Order-product relationship created",
            "order_product": order_product_instance,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the order-product relationship"
        ) from exc


@order_product_route.put("/order_products/{order_product_id}", response_model=ProductOrder)
def update_order_product(order_product_id: int, order_product_data: ProductOrder):
    """
    Update an existing order-product relationship.
    """
    try:
        updated_order_product = OrderProductService.update_order_product(
            order_product_id,
            order_id=order_product_data.order_id,
            product_id=order_product_data.product_id,
            quantity=order_product_data.quantity
        )
        if not updated_order_product:
            raise HTTPException(
                status_code=404, detail="Order-product relationship not found"
            )
        return {
            "message": "Order-product relationship updated",
            "order_product": updated_order_product,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while updating the order-product relationship"
        ) from exc


@order_product_route.delete("/order_products/{order_product_id}")
def delete_order_product(order_product_id: int):
    """
    Delete an order-product relationship by its ID.
    """
    try:
        success = OrderProductService.delete_order_product(order_product_id)
        if not success:
            raise HTTPException(
                status_code=404, detail="Order-product relationship not found"
            )
        return {"message": "Order-product relationship deleted"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid order-product ID") from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the order-product relationship"
        ) from exc

"""
This module defines the routes for handling orders in the API.
"""

# pylint: disable=E0401

from fastapi import APIRouter, Body, HTTPException
from models.order import Order
from services.order_service import OrderService  # type: ignore

order_route = APIRouter()
# pylint: disable=no-value-for-parameter


@order_route.get("/orders")
def get_all_orders():
    """
    Retrieves all orders from the database.
    """
    try:
        orders = OrderService.get_all_orders()
        return {"orders": orders}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@order_route.get("/orders/{order_id}")
def get_order_by_id(order_id: int):
    """
    Retrieves an order by ID.
    """
    try:
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid order ID"
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving the order"
        ) from exc


@order_route.post("/orders")
def create_order(order: Order = Body(...)):
    """
    Creates a new order.
    """
    try:
        order_instance = OrderService.create_order(
            user_id=order.user_id, date=order.date, total=order.total
        )
        return {"message": "Order created", "order": order_instance}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the order"
        ) from exc


@order_route.put("/orders/{order_id}")
def update_order(order_id: int, order: Order = Body(...)):
    """
    Updates an order.
    """
    try:
        updated_order = OrderService.update_order(
            order_id, user_id=order.user_id, date=order.date, total=order.total
        )
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order updated", "order": updated_order}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the order"
        ) from exc


@order_route.delete("/orders/{order_id}")
def delete_order(order_id: int):
    """
    Deletes an order by ID.
    """
    try:
        success = OrderService.delete_order(order_id)
        if not success:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order deleted"}
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid order ID"
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the order"
        ) from exc

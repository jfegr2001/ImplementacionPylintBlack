from fastapi import APIRouter, Body
from ..models.order import Order  # Asegúrate de importar el modelo de Pydantic correctamente
from ..database import OrderModel  # type: ignore

order_route = APIRouter()

@order_route.get("/orders", response_model=list[Order])
def get_orders():
    """
    Retrieve all orders.
    """
    orders = list(OrderModel.select())
    return [Order(**order) for order in orders]  # Convierte los datos a instancias de Order

@order_route.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    """
    Retrieve an order by its ID.
    """
    order = OrderModel.get(OrderModel.id == order_id)
    return Order(**order)  # Asegúrate de que devuelves un modelo de Pydantic

@order_route.post("/orders", response_model=Order)
def create_order(order_data: Order = Body(...)):  
    """
    Create a new order.
    """
    new_order = OrderModel.create(
        user_id=order_data.user_id, 
        date=order_data.date, 
        total=order_data.total
    )     
    return Order(**new_order.__data__)  # Accede a los datos como diccionario si estás usando peewee


@order_route.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order_data: Order):
    """
    Update an existing order.
    """
    OrderModel.update(**order_data.dict()).where(OrderModel.id == order_id).execute()
    updated_order = OrderModel.get(OrderModel.id == order_id)
    return Order(**updated_order)

@order_route.delete("/orders/{order_id}")
def delete_order(order_id: int):
    """
    Delete an order by its ID.
    """
    OrderModel.delete().where(OrderModel.id == order_id).execute()
    return {"message": "Order deleted"}

"""
This module provides services to manage orders, including
retrieving, creating, updating, and deleting orders in the database.
"""

# pylint: disable=E0401

from peewee import IntegrityError, DoesNotExist
from models.order import Order
from config.database import OrderModel


class OrderService:
    """
    A service class to manage orders in the database.
    """

    @staticmethod
    def get_all_orders():
        """
        Retrieve all orders from the database.
        """
        try:
            orders = list(OrderModel.select())
            return [Order(**order.__data__) for order in orders]
        except Exception as exc:
            raise RuntimeError("Error retrieving orders") from exc

    @staticmethod
    def get_order_by_id(order_id: int):
        """
        Retrieve a specific order by its ID.

        :param order_id: ID of the order to retrieve
        :raises ValueError: if the order_id is invalid
        :return: The order object or None if not found
        """
        if order_id <= 0:
            raise ValueError("Invalid order ID")
        try:
            order = OrderModel.get(OrderModel.id == order_id)
            return Order(**order.__data__)
        except DoesNotExist:
            return None
        except Exception as exc:
            raise RuntimeError("Error retrieving the order") from exc

    @staticmethod
    def create_order(user_id: int, date: str, total: float):
        """
        Create a new order in the database.

        :param user_id: ID of the user placing the order
        :param date: The date of the order
        :param total: The total amount of the order
        :raises ValueError: if the total is negative
        :return: The created order object
        """
        if total < 0:
            raise ValueError("Total must be positive")
        try:
            new_order = OrderModel.create(user_id=user_id, date=date, total=total)
            return Order(**new_order.__data__)
        except IntegrityError as exc:
            raise ValueError("Error creating the order") from exc

    @staticmethod
    def update_order(order_id: int, user_id: int, date: str, total: float):
        """
        Update an existing order in the database.

        :param order_id: ID of the order to update
        :param user_id: Updated user ID for the order
        :param date: Updated date of the order
        :param total: Updated total amount for the order
        :raises ValueError: if total is negative or order_id is invalid
        :return: The updated order object or None if not found
        """
        if total < 0:
            raise ValueError("Total must be positive")
        if order_id <= 0:
            raise ValueError("Invalid order ID")
        try:
            rows_updated = (
                OrderModel.update(user_id=user_id, date=date, total=total)
                .where(OrderModel.id == order_id)
                .execute()
            )
            if rows_updated == 0:
                return None
            updated_order = OrderModel.get(OrderModel.id == order_id)
            return Order(**updated_order.__data__)
        except IntegrityError as exc:
            raise ValueError("Error updating the order") from exc

    @staticmethod
    def delete_order(order_id: int):
        """
        Delete an order from the database by its ID.

        :param order_id: ID of the order to delete
        :raises ValueError: if the order_id is invalid
        :return: True if the order was deleted, False otherwise
        """
        if order_id <= 0:
            raise ValueError("Invalid order ID")
        try:
            rows_deleted = (
                OrderModel.delete().where(OrderModel.id == order_id).execute()
            )
            return rows_deleted > 0
        except Exception as exc:
            raise RuntimeError("Error deleting the order") from exc

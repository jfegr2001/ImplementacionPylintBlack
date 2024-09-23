"""
This module provides services to manage the order-product relationships,
including retrieving, creating, updating, and deleting these relationships
in the database.
"""


# pylint: disable=E0401

from peewee import IntegrityError, DoesNotExist
from models.product_order import ProductOrder
from config.database import ProductOrderModel  # type: ignore


class OrderProductService:
    """
    Service class to manage order-product relationships in the database.
    """

    @staticmethod
    def get_order_products():
        """
        Retrieve all order-product relationships from the database.

        :return: List of order-product relationships
        """
        try:
            order_products = list(ProductOrderModel.select())
            return [ProductOrder(**order.__data__) for order in order_products]
        except Exception as exc:
            raise RuntimeError("Error retrieving order-product relationships") from exc

    @staticmethod
    def get_order_product_by_id(order_product_id: int):
        """
        Retrieve an order-product relationship by its ID.

        :param order_product_id: ID of the order-product relationship to retrieve
        :raises ValueError: if the order_product_id is invalid
        :return: The order-product relationship or None if not found
        """
        if order_product_id <= 0:
            raise ValueError("Invalid order-product ID")
        try:
            order_product = ProductOrderModel.get(ProductOrderModel.id == order_product_id)
            return ProductOrder(**order_product.__data__)
        except DoesNotExist:
            return None
        except Exception as exc:
            raise RuntimeError("Error retrieving the order-product relationship") from exc

    @staticmethod
    def create_order_product(order_id: int, product_id: int, quantity: int):
        """
        Create a new order-product relationship in the database.

        :param order_id: ID of the order
        :param product_id: ID of the product
        :param quantity: Quantity of the product in the order
        :raises ValueError: if the quantity is zero or less
        :return: The created order-product relationship
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        try:
            new_order_product = ProductOrderModel.create(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity
            )
            return ProductOrder(**new_order_product.__data__)
        except IntegrityError as exc:
            raise ValueError("Error creating the order-product relationship") from exc

    @staticmethod
    def update_order_product(order_product_id: int, order_id: int, product_id: int, quantity: int):
        """
        Update an existing order-product relationship.

        :param order_product_id: ID of the order-product relationship to update
        :param order_id: Updated order ID
        :param product_id: Updated product ID
        :param quantity: Updated quantity of the product
        :raises ValueError: if the quantity is zero or less or the order_product_id is invalid
        :return: The updated order-product relationship or None if not found
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if order_product_id <= 0:
            raise ValueError("Invalid order-product ID")
        try:
            rows_updated = ProductOrderModel.update(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity
            ).where(ProductOrderModel.id == order_product_id).execute()
            if rows_updated == 0:
                return None
            updated_order_product = ProductOrderModel.get(ProductOrderModel.id == order_product_id)
            return ProductOrder(**updated_order_product.__data__)
        except IntegrityError as exc:
            raise ValueError("Error updating the order-product relationship") from exc

    @staticmethod
    def delete_order_product(order_product_id: int):
        """
        Delete an order-product relationship from the database by its ID.

        :param order_product_id: ID of the order-product relationship to delete
        :raises ValueError: if the order_product_id is invalid
        :return: True if the order-product relationship was deleted, False otherwise
        """
        if order_product_id <= 0:
            raise ValueError("Invalid order-product ID")
        try:
            rows_deleted = ProductOrderModel.delete().where(
                ProductOrderModel.id == order_product_id
            ).execute()
            return rows_deleted > 0
        except Exception as exc:
            raise RuntimeError("Error deleting the order-product relationship") from exc

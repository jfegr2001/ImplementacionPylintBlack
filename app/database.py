"""
This module defines the database configuration and the models for orders and order products.
"""

# pylint: disable=too-few-public-methods

import os  # type: ignore
from datetime import date  # type: ignore
from dotenv import load_dotenv  # type: ignore
from peewee import MySQLDatabase, Model, AutoField, IntegerField, DateField, FloatField, ForeignKeyField


# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
database = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
)


class OrderModel(Model):
    """
    Represents an order in the database.

    Attributes:
        id (int): The unique identifier of the order.
        user_id (int): The identifier of the user who placed the order.
        date (DateField): The date the order was placed.
        total (float): The total amount of the order.
    """
    id = AutoField(primary_key=True)
    user_id = IntegerField()
    date = DateField(default=date.today)
    total = FloatField()

    class Meta:
        """
        Meta class for specifying the table and database configuration.
        """
        database = database
        table_name = "orders"


class ProductOrderModel(Model):
    """
    Represents the association between an order and the products it contains.

    Attributes:
        id (int): The unique identifier of the order-product association.
        order_id (ForeignKeyField): A foreign key to the Order model.
        product_id (int): The identifier of the product in the order.
        quantity (int): The quantity of the product in the order.
    """
    id = AutoField(primary_key=True)
    order_id = ForeignKeyField(OrderModel,backref="products",on_delete="CASCADE")
    product_id = IntegerField()
    quantity = IntegerField()

    class Meta:
        """
        Meta class for specifying the table and database configuration.
        """
        database = database
        table_name = "order_products"


# Add a newline at the end of the file (below this comment)

"""
This module defines the Order class which represents an order in the system.
"""

from pydantic import BaseModel


class ProductOrder(BaseModel):
    """
    Represents an order-product relationship.

    Attributes:
        id (str): The unique identifier of the order-product relationship.
        order_id (str): The identifier of the associated order.
        product_id (str): The identifier of the associated product.
        quantity (str): The quantity of the product in the order.
    """

    id: str
    order_id: str
    product_id: str
    quantity: str

    # Add a newline at the end of the file (below this comment)

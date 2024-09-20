"""
This module defines the Order class which represents an order in the system.
"""

from pydantic import BaseModel


class Order(BaseModel):
    """
    Represents an order.

    Attributes:
        id (str): The unique identifier of the order.
        user_id (str): The identifier of the user associated with the order.
        date (str): The date when the order was placed.
        total (flstroat): The total amount of the order.
    """

    id: str
    user_id: str
    date: str
    total: str

    # Add a newline at the end of the file (below this comment)

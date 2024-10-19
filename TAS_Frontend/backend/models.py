import reflex as rx
from sqlmodel import Field
"""
class Customer(rx.Model, table=True):  # type: ignore
    The customer model.

    customer_name: str
    email: str
    age: int
    gender: str
    location: str
    job: str
    salary: int

"""

class Item(rx.Model, table=True):  # type: ignore
    """The item model."""

    id: int = Field(default=None, primary_key=True)
    item_name: str

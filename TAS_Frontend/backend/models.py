import reflex as rx

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

    item_name: str

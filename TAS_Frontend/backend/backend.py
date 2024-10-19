import os
import openai

import reflex as rx
from sqlmodel import select, asc, desc, or_, func

from .models import Item


products: dict[str, dict] = {
    "T-shirt": {
        "description": "A plain white t-shirt made of 100% cotton.",
        "price": 10.99,
    },
    "Jeans": {
        "description": "A pair of blue denim jeans with a straight leg fit.",
        "price": 24.99,
    },
    "Hoodie": {
        "description": "A black hoodie made of a cotton and polyester blend.",
        "price": 34.99,
    },
    "Cardigan": {
        "description": "A grey cardigan with a V-neck and long sleeves.",
        "price": 36.99,
    },
    "Joggers": {
        "description": "A pair of black joggers made of a cotton and polyester blend.",
        "price": 44.99,
    },
    "Dress": {"description": "A black dress made of 100% polyester.", "price": 49.99},
    "Jacket": {
        "description": "A navy blue jacket made of 100% cotton.",
        "price": 55.99,
    },
    "Skirt": {
        "description": "A brown skirt made of a cotton and polyester blend.",
        "price": 29.99,
    },
    "Shorts": {
        "description": "A pair of black shorts made of a cotton and polyester blend.",
        "price": 19.99,
    },
    "Sweater": {
        "description": "A white sweater with a crew neck and long sleeves.",
        "price": 39.99,
    },
}

_client = None

def get_openai_client():
    global _client
    if _client is None:
        _client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    return _client


class State(rx.State):
    """The app state."""

    current_item: Item = Item()
    users: list[Item] = []
    products: dict[str, str] = {}

    def load_entries(self) -> list[Item]:
        """Get all users from the database."""
        with rx.session() as session:
            query = select(Item)
            if self.search_value:
                search_value = f"%{str(self.search_value).lower()}%"
                query = query.where(
                    or_(
                        *[
                            getattr(Item, field).ilike(search_value)
                            for field in Item.get_fields()
                        ],
                    )
                )

            if self.sort_value:
                sort_column = getattr(Item, self.sort_value)
                if self.sort_value == "salary":
                    order = desc(sort_column) if self.sort_reverse else asc(
                        sort_column)
                else:
                    order = desc(func.lower(sort_column)) if self.sort_reverse else asc(
                        func.lower(sort_column))
                query = query.order_by(order)

            self.users = session.exec(query).all()

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def get_user(self, user: Item):
        self.current_user = user

    def add_Item_to_db(self, form_data: dict):
        self.current_item = form_data

        with rx.session() as session:
            if session.exec(
                select(Item).where(
                    Item.item_name == self.current_item["item_name"])
            ).first():
                return rx.window_alert("Item already exists.")
            session.add(Item(**self.current_item))
            session.commit()
        self.load_entries()
        return rx.toast.info(f"User {self.current_user['item_name']} has been added.", position="bottom-right")

    def update_Item_to_db(self, form_data: dict):
        pass

    def delete_Item(self, id: int):
        pass

    @rx.background
    async def call_openai(self):
        return "pass"

    def generate_email(self, user: Item):
        return "pass"

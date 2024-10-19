import os
import openai
import reflex as rx
from sqlmodel import select, asc, desc, or_, func
from .models import Item

_client = None

def get_openai_client():
    global _client
    if _client is None:
        _client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client

class State(rx.State):
    """The app state."""

    current_item: Item = Item()
    items: list[Item] = []
    sort_value: str = "item_name"
    sort_reverse: bool = False
    search_value: str = ""

    def load_entries(self) -> list[Item]:
        """Get all items from the database."""
        with rx.session() as session:
            query = select(Item)
            if self.search_value:
                search_value = f"%{str(self.search_value).lower()}%"
                query = query.where(Item.item_name.ilike(search_value))

            if self.sort_value:
                sort_column = getattr(Item, self.sort_value)
                order = desc(func.lower(sort_column)) if self.sort_reverse else asc(func.lower(sort_column))
                query = query.order_by(order)

            self.items = session.exec(query).all()
        return self.items

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def get_item(self, item: Item):
        self.current_item = item

    def add_item_to_db(self, form_data: dict):
        with rx.session() as session:
            if session.exec(select(Item).where(Item.item_name == form_data["item_name"])).first():
                return rx.window_alert("Item already exists.")
            new_item = Item(**form_data)
            session.add(new_item)
            session.commit()
            session.refresh(new_item)
        self.load_entries()
        return rx.toast.success(f"Item {new_item.item_name} has been added.", position="bottom-right")

    def update_item_to_db(self, form_data: dict):
        with rx.session() as session:
            item = session.exec(select(Item).where(Item.id == self.current_item.id)).one()
            for key, value in form_data.items():
                setattr(item, key, value)
            session.commit()
            session.refresh(item)
        self.load_entries()
        return rx.toast.success(f"Item {item.item_name} has been updated.", position="bottom-right")

    def delete_item(self, item: Item):
        with rx.session() as session:
            item_to_delete = session.exec(select(Item).where(Item.id == item.id)).one()
            session.delete(item_to_delete)
            session.commit()
        self.load_entries()
        return rx.toast.success(f"Item {item.item_name} has been deleted.", position="bottom-right")

    @rx.background
    async def call_openai(self):
        # Implement OpenAI API call if needed
        pass

    def generate_item_description(self, item: Item):
        # Implement item description generation if needed
        pass
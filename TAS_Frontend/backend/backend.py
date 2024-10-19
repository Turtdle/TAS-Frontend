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
    email_content_data: str = "Click 'Generate Email' to generate a personalized sales email."
    gen_response = False
    tone: str = "😊 Formal"
    length: str = "1000"
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

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
        return rx.toast.info(f"User {self.current_user['Item_name']} has been added.", position="bottom-right")

    def update_Item_to_db(self, form_data: dict):
        self.current_user.update(form_data)
        with rx.session() as session:
            Item = session.exec(
                select(Item).where(Item.id == self.current_user["id"])
            ).first()
            for field in Item.get_fields():
                if field != "id":
                    setattr(Item, field, self.current_user[field])
            session.add(Item)
            session.commit()
        self.load_entries()
        return rx.toast.info(f"User {self.current_user['Item_name']} has been modified.", position="bottom-right")

    def delete_Item(self, id: int):
        """Delete a Item from the database."""
        with rx.session() as session:
            Item = session.exec(
                select(Item).where(Item.id == id)).first()
            session.delete(Item)
            session.commit()
        self.load_entries()
        return rx.toast.info(f"User {Item.Item_name} has been deleted.", position="bottom-right")

    @rx.background
    async def call_openai(self):
        session = get_openai_client().chat.completions.create(
            user=self.router.session.client_token,
            stream=True,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a salesperson at Reflex, a company that sells clothing. You have a list of products and Item data. Your task is to write a sales email to a Item recommending one of the products. The email should be personalized and include a recommendation based on the Item's data. The email should be {self.tone} and {self.length} characters long."},
                {"role": "user", "content": f"Based on these {products} write a sales email to {self.current_user.Item_name} and email {self.current_user.email} who is {self.current_user.age} years old and a {self.current_user.gender} gender. {self.current_user.Item_name} lives in {self.current_user.location} and works as a {self.current_user.job} and earns {self.current_user.salary} per year. Make sure the email recommends one product only and is personalized to {self.current_user.Item_name}. The company is named Reflex its website is https://reflex.dev."},
            ]
        )
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                response_text = item.choices[0].delta.content
                async with self:
                    if response_text is not None:
                        self.email_content_data += response_text
                yield

        async with self:
            self.gen_response = False

    def generate_email(self, user: Item):
        self.current_user = Item(**user)
        self.gen_response = True
        self.email_content_data = ""
        return State.call_openai

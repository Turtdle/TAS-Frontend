


import os
import openai
import reflex as rx
from firebase_admin import credentials, firestore, initialize_app
from typing import List, Dict, Any
from typing import TypedDict, List

# Initialize Firebase
current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, "..", "PRIVATE_KEY", "tashopping-c8efa-firebase-adminsdk-mnohm-a4ed75205a.json")
cred = credentials.Certificate(key_path)
initialize_app(cred)
db = firestore.client()

_client = None



class Item(TypedDict):
    id: str
    item_name: str

def get_openai_client():
    global _client
    if _client is None:
        _client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client

class State(rx.State):
    """The app state."""

    current_item: Item = Item(id="", item_name="")
    items: List[Item] = []
    sort_value: str = "item_name"
    sort_reverse: bool = False
    search_value: str = ""
    map_image_url: str = "/path/to/default/map/image.png"
    
    def update_map(self, new_url: str):
        self.map_image_url = new_url

    def load_entries(self) -> None:
        """Get all items from Firebase."""
        items_ref = db.collection('items')
        query = items_ref

        if self.search_value:
            query = query.where('item_name', '>=', self.search_value).where('item_name', '<=', self.search_value + '\uf8ff')

        if self.sort_value:
            query = query.order_by(self.sort_value, direction=firestore.Query.DESCENDING if self.sort_reverse else firestore.Query.ASCENDING)

        docs = query.stream()
        self.items = [Item(id=doc.id, item_name=doc.to_dict().get('item_name', '')) for doc in docs]


    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def filter_values(self, search_value: str):
        self.search_value = search_value
        self.load_entries()

    def get_item(self, item: Item):
        self.current_item = item

    def add_item_to_db(self, form_data: Item):
        items_ref = db.collection('items')
        existing_item = items_ref.where('item_name', '==', form_data['item_name']).limit(1).get()
        if len(existing_item) > 0:
            return rx.window_alert("Item already exists.")
        
        new_item_ref = items_ref.document()
        new_item_ref.set(form_data)
        self.load_entries()
        return rx.toast.success(f"Item {form_data['item_name']} has been added.", position="bottom-right")

    def update_item_to_db(self, form_data: Item):
        if not self.current_item.get('id'):
            return rx.window_alert("No item selected for update.")
        
        item_ref = db.collection('items').document(self.current_item['id'])
        item_ref.update(form_data)
        self.load_entries()
        return rx.toast.success(f"Item {form_data['item_name']} has been updated.", position="bottom-right")

    def delete_item(self, item: Item):
        db.collection('items').document(item['id']).delete()
        self.load_entries()
        return rx.toast.success(f"Item {item['item_name']} has been deleted.", position="bottom-right")

    @rx.background
    async def call_openai(self):
        # Implement OpenAI API call if needed
        pass

    def generate_item_description(self, item: Item):
        # Implement item description generation if needed
        pass
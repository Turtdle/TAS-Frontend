import reflex as rx
from ..backend.backend import State

def map_component() -> rx.Component:
    return rx.box(
        rx.text(State.status, size="2xl"),
        rx.image(
            src=State.map_image_url,
            width="100%",
            height="100%",
            object_fit="contain",
        ),
        width="100%",
        height="100%",
        flex_grow="1",
        overflow="hidden",
    )

class MapState(rx.State):
    map_image_url: str = "/path/to/default/map/image.png"
    status = "idle"
    def update_map(self, new_url: str):
        self.map_image_url = new_url
    
    def update_status(self, new_status: str):
        self.status = new_status
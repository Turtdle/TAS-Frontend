import reflex as rx
from ..backend.backend import State

def map_component() -> rx.Component:
    print(State.map_image_url)
    return rx.box(
        rx.image(
            src=State.map_image_url,  # Use rx.State to access the state
            width="100%",
            height="100%",
            object_fit="cover",
        ),
        width="100%",
        height="100%",
        bg="gray.100",
    )
class MapState(rx.State):
    map_image_url: str = "/path/to/default/map/image.png"

    def update_map(self, new_url: str):
        self.map_image_url = new_url
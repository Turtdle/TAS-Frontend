import reflex as rx
from .views.navbar import navbar
from .views.table import main_table
from .backend.backend import State
from .components.map_component import map_component
from .views.table import route_form
def index() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            navbar(),
            route_form(),
            rx.box(
                main_table(),
                width="100%",
            ),
            width="70%",
            height="100vh",
            bg=rx.color("accent", 1),
            spacing="6",
            padding_x=["1.5em", "1.5em", "3em"],
            padding_y=["1em", "1em", "2em"],
        ),
        rx.box(
            map_component(),
            width="30%",
            height="100vh",
        ),
        width="100%",
        height="100vh",
    )

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="blue"
    ),
)

app.add_page(
    index,
    on_load=State.load_entries,
    title="TAS App",
    description="Manage your items efficiently.",
)
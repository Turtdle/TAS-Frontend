import reflex as rx
from .views.navbar import navbar
from .views.table import main_table
from .backend.backend import State
from .components.map_component import map_component
from .views.table import route_form, _make_route_button
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import functools
import json
import jwt
from .react_oauth_google import (
    GoogleOAuthProvider,
    GoogleLogin,
)
CLIENT_ID = "1076152994401-nfap05ojv7ajctp3ss2m9vpi2qv48t1f.apps.googleusercontent.com"

def user_info(tokeninfo: dict) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.avatar(
                name=tokeninfo["name"],
                src=tokeninfo["picture"],
                size="lg",
            ),
            rx.vstack(
                rx.heading(tokeninfo["name"], size="md"),
                rx.text(State.user_email),  # Display the email here
                align_items="flex-start",
            ),
            padding="10px",
        ),
        rx.button("Logout", on_click=State.logout),
    )
def login() -> rx.Component:
    return rx.vstack(
        GoogleLogin.create(onSuccess=State.onSuccess),
    )
def require_google_login(page) -> rx.Component:
    @functools.wraps(page)
    def _auth_wrapper() -> rx.Component:
        return GoogleOAuthProvider.create(
            rx.cond(
                State.is_hydrated,
                rx.cond(
                    State.token_is_valid, page(), login()
                ),
                rx.spinner(),
            ),
            client_id=CLIENT_ID,
        )

    return _auth_wrapper
@rx.page(route="/protected")
@require_google_login
def protected() -> rx.Component:
    return rx.vstack(
        user_info(State.tokeninfo),
        rx.text(State.protected_content),
        rx.link("Home", href="/"),
    )

def index() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            GoogleOAuthProvider.create(
            GoogleLogin.create(onSuccess=State.onSuccess),
            client_id=CLIENT_ID,
            ),
            navbar(),
            route_form(),
            rx.box(
                main_table(),
                width="100%",
            ),
            width="50%",
            height="100vh",
            bg=rx.color("accent", 1),
            spacing="6",
            padding_x=["1.5em", "1.5em", "3em"],
            padding_y=["1em", "1em", "2em"],
        ),
        rx.box(
            map_component(),
            width="50%",
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

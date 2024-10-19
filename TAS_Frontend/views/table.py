import reflex as rx
from ..backend.backend import State, Item
from ..components.form_field import form_field
from typing import TypedDict
def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _show_item(item: Item):
    return rx.table.row(
        rx.table.cell(item["item_name"]),
        rx.table.cell(
            rx.hstack(
                _update_item_dialog(item),
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    color_scheme="red",
                    size="2",
                    variant="solid",
                    on_click=lambda: State.delete_item(item),
                ),
                spacing="2",
            )
        ),
    )

#i hate this shit
 
def route_form():
    return rx.vstack(
        rx.input(
            placeholder="State",
            on_change=State.set_state,
        ),
        rx.input(
            placeholder="Address",
            on_change=State.set_address,
        ),
        rx.button("Generate Route", on_click=State.generate_route),
        width="100%",
        spacing="4",
    )
def _make_route_button():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("map-pin", size=26),
                rx.text("Generate Route", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title("Generate Route", size="lg"),
                rx.dialog.description(
                    "Enter your location details and we'll generate a route for your shopping list."
                ),
                rx.input(
                    placeholder="State",
                    id="state",
                    on_change=State.set_state,
                ),
                rx.input(
                    placeholder="Address",
                    id="address",
                    on_change=State.set_address,
                ),
                rx.button("Generate Route", on_click=State._generate_route),
                width="100%",
                spacing="4",
            ),
            width="100%",
            max_width="400px",
        ),
    )

def _add_item_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Item", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="box", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add Item",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the item's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.form.root(
                rx.flex(
                    rx.hstack(
                        form_field(
                            "Name",
                            "Item Name",
                            "text",
                            "item_name",
                            "box",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Submit Item"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    width="100%",
                    direction="column",
                    spacing="4",
                ),
                on_submit=State.add_item_to_db,
                reset_on_submit=True,
            ),
            width="100%",
            max_width="450px",
            justify=["end", "end", "start"],
            padding="1.5em",
            border=f"2.5px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def _update_item_dialog(item: Item):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.icon_button(
                rx.icon("square-pen", size=22),
                color_scheme="green",
                size="2",
                variant="solid",
                on_click=lambda: State.get_item(item),
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Edit Item",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Edit the item's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.form.root(
                rx.flex(
                    rx.hstack(
                        form_field(
                            "Name",
                            "Item Name",
                            "text",
                            "item_name",
                            "box",
                            str(item["item_name"]),  # Cast to string here
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Update Item"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    width="100%",
                    direction="column",
                    spacing="4",
                ),
                on_submit=State.update_item_to_db,
                reset_on_submit=False,
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )

def main_table():
    return rx.fragment(
        rx.flex(
            _add_item_button(),
            rx.spacer(),
            rx.cond(
                State.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
            ),
            rx.select(
                ["item_name"],
                placeholder="Sort By: Name",
                size="3",
                on_change=lambda sort_value: State.sort_values(sort_value),
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                placeholder="Search here...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                on_change=lambda value: State.filter_values(value),
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Name", "box"),
                    _header_cell("Actions", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(State.items, _show_item)),
            variant="surface",
            size="3",
            width="100%",
        ),
    )
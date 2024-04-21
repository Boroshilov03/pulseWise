
import reflex as rx
from reflexer.styles import FONT_FAMILY
from reflex_motion import motion

class State(rx.State):
    pass

def navbar(pageName: str) -> rx.Component:
    return rx.hstack(
        motion(
            rx.link(
                rx.heading("♡ Pulsewise", font_family=FONT_FAMILY, size="7", color="white"),
                href="/",
            ),
            while_hover={"scale": 1.05},
            while_tap={"scale": 0.9},
            transition={"type": "spring", "stiffness": 400, "damping": 17},
        ),

        rx.text(pageName, color="white",weight="bold", font_size="md", size="5"),

        rx.hstack(

            motion(
                rx.link(
                    rx.text("❔ Profile", color="red", weight="bold", font_size="md", size="5", padding="0.3em",
                            bg="white", border_radius="7px"),
                    href="/questions"
                ),
                while_hover={"scale": 1.1},
                while_tap={"scale": 0.9},
                transition={"type": "spring", "stiffness": 400, "damping": 17},
            ),
            motion(
                rx.link(
                    rx.text("📊 Dashboard", color="red", weight="bold", font_size="md", size="5", padding="0.3em", bg="white", border_radius="7px"),
                    href="/dashboard"
                ),
                while_hover={"scale": 1.1},
                while_tap={"scale": 0.9},
                transition={"type": "spring", "stiffness": 400, "damping": 17},
            ),

            motion(
                rx.link(
                    rx.text("🩺 Doctor Chat", color="red", weight="bold", font_size="md", size="5", padding="0.3em", bg="white", border_radius="7px"),
                    href="/aichat"
                ),
                while_hover={"scale": 1.1},
                while_tap={"scale": 0.9},
                transition={"type": "spring", "stiffness": 400, "damping": 17},
            ),
            spacing="7",
        ),

        position="fixed",
        top="0px",
        z_index="5",
        padding_bottom="6em",
        width="100%",
        padding="1em",
        background_color="red",
        justify="between",
        justify_content="space-between",
        align_items="center",
        padding_right="5em",
        padding_left="5em"

    )

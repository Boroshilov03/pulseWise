
import reflex as rx
from reflex_motion import motion

def alert():

    return rx.container(
            rx.heading(
                "⚕️ Complete Your Medical Profile",
                size="8",
                align="center",
                margin="1em 0",
            ),
            rx.text(
                "Before you can access this page, please complete your medical profile.",
                align="center",
                margin="0 0 2em 0",
                weight="bold",
            ),
            rx.center(
                motion(
                    rx.link(
                        rx.text(
                            "Complete Medical Profile",
                            color="white",
                            weight="bold",
                            font_size="md",
                            padding="1em 2em",
                            bg="orange",
                            border_radius="5px",
                        ),
                        href="/questions",
                    ),
                    while_hover={"scale": 1.05},
                    while_tap={"scale": 0.95},
                    transition={"type": "spring", "stiffness": 400, "damping": 17},
                ),
            ),
        padding_top="9em",
    )

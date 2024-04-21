
import reflex as rx
from reflexer.navigation import navbar
from reflex_motion import motion

def landing() -> rx.Component:
    return (
        rx.center(

            navbar("Home Page"),
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.heading("Your Heart Is Special", size="9", weight="bold", color_scheme="orange"),
                        rx.heading("Find ways to manage and live with your condition", size="7", weight="light"),
                        motion(
                            rx.link(
                                rx.flex(
                                    rx.icon("clipboard-plus", size=30),
                                    rx.text("Begin check up", ),
                                    width="30%", color="white", weight="bold", font_size="md", size="5",
                                    padding="0.5em",
                                    bg="red", border_radius="7px", gap='9px', align_items="center",justify="center"

                                ),
                                href="/questions",
                            ),
                            while_hover={"scale": 1.05},
                            while_tap={"scale": 0.9},
                            transition={"type": "spring", "stiffness": 400, "damping": 17},
                        ),
                        width="50%",
                        direction="column",
                        spacing="3",
                    ),
                    rx.image(src="/heart3.png", width="15%", height="80%"),
                    width="100%",
                    direction="row",
                    align="center",
                    justify="center",
                ),
                rx.heading("FEATURES WE PROVIDE", margin_y="20px", size="7", margin_left="4em"),
                rx.flex(
                    rx.flex(
                        rx.box(rx.heading("Calculating BMI is easier")),
                        rx.box(rx.blockquote("We calculate your BMI index from data like age, height, weight.")),
                        rx.image(src="/meter.png", width="50%", height="auto"),
                        direction="column", align="center"
                    ),
                    rx.flex(
                        rx.box(rx.heading("Food Recommendation")),
                        rx.box(rx.blockquote("We provide food recommendation according to your health problems.")),
                        rx.image(src="/beef.png", width="40%", height="auto"),
                        direction="column", align="center"
                    ),
                    rx.flex(
                        rx.box(rx.heading("Interactive Chatbot")),
                        rx.box(rx.blockquote("Solve your queries by interacting with our bot.")),
                        rx.image(src="/chatbot.png", width="50%", height="auto"),
                        direction="column", align="center"
                    ),
                    direction="row",
                    align="center",
                    justify="center",
                    spacing="0",  # Adjust the spacing between items
                    margin_left="100px",
                    margin_right="100px"
                ),
                width="100%",
                direction="column",
            ),
            padding_top="6em",
        ),
    )


"""The style classes and constants for the Dashboard App."""
from reflex.components.radix import themes as rx

THEME = rx.theme(
    appearance="light",
    has_background=True,
    radius="large",
    accent_color="iris",
    scaling="100%",
    panel_background="solid",
)

STYLESHEETS = ["https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"]

FONT_FAMILY = "Inter"
BACKGROUND_COLOR = "var(--accent-2)"


shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"

messageStyle = dict(
    padding="1em",
    border_radius="5px",
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="30em",
    display="inline-block",
)
# Set specific styles for questions and answers.
question_style = messageStyle | dict(
    bg="blue", color="white", font_weight="bold", margin_left="20%"
)
answer_style = messageStyle | dict(
    bg="red", color="white", margin_right="20%"
)


import reflex as rx
from reflexer.styles import BACKGROUND_COLOR, FONT_FAMILY, THEME, STYLESHEETS

from reflexer.pages.questions import questions
from reflexer.pages.dashboard import dashboard
from reflexer.pages.aichat import aichat
from reflexer.pages.weather import weather
from reflexer.pages.index import landing

# Create app instance and add index page.
app = rx.App(
    theme=THEME,
    stylesheets=STYLESHEETS,
)

app.add_page(landing, route="/")
app.add_page(questions, route="/questions")
app.add_page(dashboard, route="/dashboard")
app.add_page(aichat, route="/aichat")
app.add_page(weather, route='/weather')
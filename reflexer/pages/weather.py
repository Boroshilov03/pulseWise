
import reflex as rx
import requests

from reflexer.navigation import navbar
from reflex_motion import motion


def location_weather():
    response = requests.get('http://ipinfo.io/json')
    if response.status_code == 200:
        # Extract the city from the IP information
        ip_info = response.json()
        city = ip_info.get('city', '')

        # Make the API call to get weather information based on the city
        weather_loc = requests.get(f"http://api.weatherapi.com/v1/current.json?key=29ddca607cba4891bb4214737242004&q={city}")
        return weather_loc.json()
    else:
        return {"error": "Error retrieving location data"}

def weather() -> rx.Component:
    # Get weather information
    weather_info = location_weather()

    if 'error' in weather_info:
        return rx.html("<p>Error retrieving weather data</p>")

    # Extract weather attributes
    temperature_f = weather_info['current']['temp_f']
    pressure_in = weather_info['current']['pressure_in']
    humidity = weather_info['current']['humidity']


    # Generate message based on weather attributes
    message = f"Today's weather: Temperature: {temperature_f}째F, Pressure: {pressure_in} inHg, Humidity: {humidity}%"

    # Create the component structure
    return (
        rx.center(
            navbar(pageName="Home Page"),

            rx.flex(
                rx.heading(
                    "Weather",
                    font_weight="bold",
                    font_size="2em",
                    margin="1em"
                ),
                rx.hstack(
                    rx.box(
                        rx.flex(
                            rx.callout(
                                "Be aware of today's temperature, humidity, and atmospheric pressure",
                                icon="info",
                            ),
                            rx.flex(
                                motion(
                                    rx.box(
                                        rx.text("Temperature", weight="light", size="5", color="white"),
                                        rx.flex(rx.heading(f"{temperature_f}", weight="light", size="9", color="white"),
                                                rx.text("F", color="white", size="3"), direction="row"),
                                        # f"The temperature is currently {temperature_f}째F, which is higher than optimal for individuals with heart conditions.",
                                        width="250px",
                                        background="linear-gradient(45deg, dodgerblue, deepskyblue)",
                                        border_radius="10px",
                                        radius="10px",
                                        padding="2em",
                                        height="250px",
                                    ),
                                    while_hover={"scale": 1.05},
                                    while_tap={"scale": 0.9},
                                    transition={"type": "spring", "stiffness": 400, "damping": 17},
                                ),

                                motion(
                                    rx.box(
                                        rx.text("Pressure", weight="light", size="5", color="white"),
                                        rx.flex(rx.heading(f"{pressure_in}", weight="light", size="9", color="white"),
                                                rx.text("Hg", color="white", size="3"), direction="row"),
                                        # f"The atmospheric pressure is currently {pressure_in} inHg, which may impact individuals with heart conditions.",
                                        width="250px",
                                        background="linear-gradient(45deg, darkslateblue, cornflowerblue)",
                                        border_radius="10px",
                                        radius="10px",
                                        padding="2em",
                                        height="250px"
                                    ),
                                    while_hover={"scale": 1.05},
                                    while_tap={"scale": 0.9},
                                    transition={"type": "spring", "stiffness": 400, "damping": 17},
                                ),
                                motion(
                                    rx.box(
                                        rx.text("Humidity", weight="light", size="5", color="white"),
                                        rx.flex(rx.heading(f"{humidity}", weight="light", size="9", color="white"),
                                                rx.text("%", color="white", size="3"), direction="row"),
                                        # rx.image(src="/Sun.png", width="150px", height="auto"),
                                        # f"The humidity is currently {humidity}%, which can affect breathing and comfort for individuals with heart conditions.",
                                        width="250px",
                                        background="linear-gradient(45deg, lightcoral, lightsalmon)",
                                        border_radius="10px",
                                        radius="10px",
                                        padding="2em",
                                        height="250px"
                                    ),
                                    while_hover={"scale": 1.05},
                                    while_tap={"scale": 0.9},
                                    transition={"type": "spring", "stiffness": 400, "damping": 17},
                                ),
                                margin_y="2em",
                                spacing="8",
                                direction="row"
                            ),
                            rx.box(
                                rx.flex(
                                    rx.heading("Important Facts:"),
                                    rx.divider(),
                                    rx.text(
                                        "Individuals over age 50, overweight and those with preexisting heart, lung or kidney conditions are at higher risk for health complications due to humidity."
                                    ),
                                    rx.divider(),
                                    rx.text(
                                        "Sweating causes dehydration and reduces volume of blood for anyone: heart works harder to regulate body (greater risk for older, pre-existing conditions and outdoor activity)."
                                    ),
                                    rx.divider(),
                                    rx.text(
                                        "Temperatures higher than 70째F with a humidity above 70% have the highest risk for heart symptoms."
                                    ),
                                    rx.divider(),
                                    rx.text(
                                        "Signs of heat exhaustion include clammy skin, confusion, lightheadedness, rapid pulse, fatigue, muscle spasms/cramps, swollen arms/legs, and abnormal/no sweating."
                                    ),
                                    direction="column",
                                    spacing="2",
                                ),
                                border="1px lightgray"
                            ),
                            padding="1em",
                            direction="column",
                        ),
                        margin="5px",
                    ),
                    margin="2px",
                    spacing="5",
                    # justify_content="center",
                    # align_items="center"
                ),
            ),
            padding_top="6em",
        ),

    )
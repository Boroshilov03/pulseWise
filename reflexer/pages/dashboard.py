
import json
import reflex as rx

from reflexer.alert import alert
from reflexer.navigation import navbar
from reflexer.pages.aichat import ChatGemini
import requests
from reflex_motion import motion
import google.generativeai as genai



# Configure Google API
GOOGLE_API = "AIzaSyCQsYQDQbLZoMPhUnUdCgRM8wxv3iUM4Sg"
genai.configure(api_key=GOOGLE_API)

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "response_mime_type": "application/json",
}

# Safety settings
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]


class DashboardState(rx.State):

    localStorageData: str = rx.LocalStorage(name="questionInputs")
    userLocation = ""
    cholesterol: str = "200 mg/dl"
    bmi: str = "22.5"

    dashboard = {}

    finalResult = ""
    cholesterolData = {}
    bmiData = {}
    factsValue = []
    loading = True

    def loadingStart(self):
        self.loading = True

    def loadingEnd(self):
        self.loading = False

    async def analyzeUserData(self):

        if (self.localStorageData.strip() != ""):
            self.loadingStart()

            system_instruction = """
                    Based on the user hospital data which is given
                    {
                      "What is your full name?": "adrian adam",
                      "What is your email address?": "adrian@gmail.com",
                      "What is your age?": "20",
                      "What is your height in centimeters?": "180",
                      "What is your weight?": "180",
                      "What is your cholesterol level?": "200",
                      "Are you currently a smoker?": "no",
                      "Do you consume alcohol regularly?": "no",
                      "Have you ever experienced a stroke?": "no",
                      "What is your biological sex?": "male",
                      "Do you have a history of diabetes?": "no",
                      "Do you exercise regularly?": "no",
                      "How many hours do you sleep nightly?": "4",
                      "Do you have a history of asthma?": "no",
                      "Do you have any kidney conditions?": "no",
                      "Have you ever had skin cancer?": "no"
                    }

                    Important: Give me 5 or more of facts and make sure to include emojis

                    Cholesterol: Include the cholesterol value and a comment.
                    "value": Cholesterol level.
                    "comment": Brief comment on the cholesterol level.
                    BMI: Include the BMI value, a comment, height, and weight.
                    "value": BMI value.
                    "comment": Brief comment on the BMI.
                    "height": Height in centimeters.
                    "weight": Weight in kilograms.
                    Facts: Include 5 or more facts.
                    Each fact should be a string.

                    I want to get the output like this. where it includes Cholesterol with values and comment, BMI with value, comment, height, weight, and Facts which includes 5 items or above

                    Output: 
                    {
                        "Result": "Adrian is at high risk" // write 5 or less word result comment
                        "Cholesterol": {
                            "value": "34",
                            "comment": "Low cholesterol is generally good." // write 3 word or less comment
                        },
                        "BMI": {
                            "value": 24.0,
                            "comment": "Obese", // write 3 word or less comment
                            "height": 170,
                            "weight": 130
                        },
                        "Facts": [
                            "Hey, Adrian your cholesterol level is quite low, which is generally good for heart health. However, make sure to maintain a balanced diet to keep it in a healthy range. 📚",
                            "Your BMI is within the healthy range, which is great. Keep up the good work! Remember to maintain a balanced diet and continue exercising regularly. 🧠✅",
                            "Since you mentioned you're a smoker, it's important to note that smoking can negatively impact your cholesterol levels. Consider quitting or reducing smoking for better overall health. 🚭",
                            "Regular exercise, like the one you mentioned, helps in maintaining a healthy weight and reducing cholesterol levels. Keep it up! 🏋️‍♂️",
                            "Since you're young and your BMI is good, it's important to establish healthy habits now to prevent health issues later in life. Eating a balanced diet and staying physically active are key. 💪",
                            "Even though your cholesterol is low, it's still essential to maintain a healthy lifestyle, including a balanced diet and regular exercise, to prevent future health problems. 🥗🏃‍♂️"
                        ]
                    }

                    """

            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro-latest",
                generation_config=generation_config,
                system_instruction=system_instruction,
                safety_settings=safety_settings,
            )

            dashboardAI = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [
                        "{\n    \"What is your full name?\": \"Adrian Mendez\",\n    \"What is your email address?\": \"adrian@gmail.com\",\n    \"What is your age?\": \"20\",\n    \"What is your height in centimeters?\": \"180\",\n    \"What is your weight?\": \"200\",\n    \"What is your cholesterol level?\": \"130\",\n    \"Are you currently a smoker?\": \"no\",\n    \"Do you consume alcohol regularly?\": \"no\",\n    \"Have you ever experienced a stroke?\": \"no\",\n    \"What is your biological sex?\": \"male\",\n    \"Do you have a history of diabetes?\": \"no\",\n    \"Do you exercise regularly?\": \"no\",\n    \"How many hours do you sleep nightly?\": \"5\",\n    \"Do you have a history of asthma?\": \"no\",\n    \"Do you have any kidney conditions?\": \"no\",\n    \"Have you ever had skin cancer?\": \"no\"\n}"]
                },
                {
                    "role": "model",
                    "parts": [
                        "```json\n{\n    \"Result\": \"Adrian is at low risk\", \n    \"Cholesterol\": {\n        \"value\": \"130\",\n        \"comment\": \"Excellent cholesterol\" \n    },\n    \"BMI\": {\n        \"value\": 30.9,\n        \"comment\": \"Obese\", \n        \"height\": 180,\n        \"weight\": 200\n    },\n    \"Facts\": [\n        \"Adrian, your cholesterol level is excellent! This indicates a lower risk of heart disease. Keep up the healthy habits!  🙌\",\n        \"Your BMI suggests you might be in the obese range. Maintaining a healthy weight is important for overall well-being. Consider incorporating regular exercise and a balanced diet. 🍎🏃‍♂️\",\n        \"Since you mentioned not smoking, that's fantastic news! Not smoking significantly reduces your risk of heart disease and other health issues. 👍\", \n        \"Getting enough sleep is crucial for good health, so it's great that you're getting around 5 hours per night. Aim for 7-8 hours for optimal health benefits. 😴\",\n        \"Even with excellent cholesterol, regular exercise can further enhance your cardiovascular health and help manage weight.  💪\",\n        \"While you're young, it's the perfect time to develop healthy habits like regular exercise and a balanced diet to prevent future health concerns. 🌱🏋️‍♀️\"\n    ]\n}\n```"]
                },
            ])
            dashboardAI.send_message(self.localStorageData)

            self.dashboard = json.loads(dashboardAI.last.text)

            self.finalResult = self.dashboard.get("Result", "")
            self.cholesterolData = self.dashboard.get("Cholesterol", {})
            self.bmiData = self.dashboard.get("BMI", {})
            self.factsValue = self.dashboard.get("Facts", [])

            self.loadingEnd()


def location_weather():
    response = requests.get('http://ipinfo.io/json')

    if response.status_code == 200:
        # Extract the city from the IP information
        ip_info = response.json()

        DashboardState.userLocation = f"{ip_info['city']}, {ip_info['region']}"

        city = ip_info.get('city', '')

        # Make the API call to get weather information based on the city
        weather_loc = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=29ddca607cba4891bb4214737242004&q={city}")
        return weather_loc.json()
    else:
        return {"error": "Error retrieving location data"}


def humidity(weather_info) -> rx.Component:

    humidity = weather_info['current']['humidity']


    return motion(
        rx.link(
            rx.card(
                rx.vstack(
                    rx.icon("droplets", size=48, color="blue"),  # Updated icon
                    rx.text("Humidity", weight="medium", font_size="1.2em", margin="0 0 5px 0", color="gray"),
                    # Updated text
                    rx.text(f"{humidity}%", weight="bold", font_size="2.5em", color="blue"),  # Updated humidity value
                ),
                align_items="center",
                justify_content="center",
                bg="white",
                border_radius="lg",
                padding="20px",
                width="250px",  # Increased width
                shadow="2xl",  # Added shadow for depth
                border="1px solid lightgray",  # Added border for definition
            ),
            href="/weather"
        ),
        initial={"scale": 1},
        while_hover={"scale": 1.09, "shadow": "lg"},
        while_tap={"scale": 0.95},
        transition={"type": "spring", "stiffness": 200, "damping": 25},
    )


def cholesterol():

    return motion(
        rx.card(
            rx.vstack(
                rx.icon("heart-pulse", size=48, color="blue"),  # Updated icon
                rx.text("Cholesterol", weight="medium", font_size="1.2em", margin="0 0 5px 0", color="gray"),
                # Updated text
                rx.cond(
                    DashboardState.loading,
                    rx.text(f"Loading...", weight="bold", font_size="2em", color="red"),
                    rx.text(f"{DashboardState.cholesterolData['value']}", weight="bold", font_size="2em", color="blue"),
                ), # Updated humidity value
                rx.text(f"{DashboardState.cholesterolData['comment']}", weight="light", font_size="1em",
                        color="black"),
            ),
            align_items="center",
            justify_content="center",
            bg="blue.50",
            border_radius="lg",
            padding="20px",
            width="300px",  # Increased width
            shadow="2xl",  # Added shadow for depth
            border="1px solid lightgray",  # Added border for definition
        ),
        initial={"scale": 1},
        while_hover={"scale": 1.09, "shadow": "lg"},
        while_tap={"scale": 0.95},
        transition={"type": "spring", "stiffness": 200, "damping": 25},
    )

def bmi():

    return motion(
        rx.card(
            rx.vstack(
                rx.icon("dumbbell", size=48, color="blue"),  # Updated icon
                rx.text("BMI", weight="medium", font_size="1.2em", margin="0 0 5px 0", color="gray"),
                # Updated text
                rx.cond(
                    DashboardState.loading,
                    rx.text(f"Loading...", weight="bold", font_size="2em", color="red"),

                    rx.text(f"{DashboardState.bmiData['value']}", weight="bold", font_size="2em", color="blue"),
                    # Updated humidity value
                ),
            ),
            rx.text(f"{DashboardState.bmiData['comment']}", weight="light", font_size="1em", color="black"),
            align_items="center",
            justify_content="center",
            bg="blue.50",
            border_radius="lg",
            padding="20px",
            width="300px",  # Increased width
            shadow="2xl",  # Added shadow for depth
            border="1px solid lightgray",  # Added border for definition
        ),
        initial={"scale": 1},
        while_hover={"scale": 1.09, "shadow": "lg"},
        while_tap={"scale": 0.95},
        transition={"type": "spring", "stiffness": 200, "damping": 25},
    )


def factsLists() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(f"📋 Your tips and tricks", font_size="2em", align="center", margin_top="20px",
                       margin_bottom="20px", padding="10px"),
            rx.cond(
                DashboardState.loading,
                rx.text("Loading data...", font_size="1.7em", weight="bold",  justify="center", align="center", color="red", margin="5px"),
                rx.vstack(
                    rx.foreach(
                        DashboardState.factsValue,
                        lambda message: (
                            rx.text(message, font_size="1.2em", color="black", margin="5px")
                        ),
                    ),
                    gap="10px",
                    max_width="55rem"
                )
            ),
            gap="5px",
        )
    )


@rx.page(on_load=DashboardState.analyzeUserData)

def dashboard():

    weather_info = location_weather()

    return rx.center(

        navbar(pageName="Dashboard"),

        rx.cond(
            ChatGemini.localStorageData.strip() == "",
            alert(),
            rx.vstack(
                rx.vstack(

                    rx.cond(
                        DashboardState.loading,
                        rx.heading(f"___________ for heart disease", font_size="2em", align="center", margin_top="20px",
                                   margin_bottom="20px", padding="10px"),
                        rx.heading(f"❤️ {DashboardState.finalResult} for heart disease", font_size="2em", align="center", margin_top="20px",
                                   margin_bottom="20px", padding="10px", color="red"),
                    ),

                    rx.hstack(
                        rx.heading(f"👤 Your health profile", font_size="2em", align="center", margin_top="20px",
                                   margin_bottom="20px", padding="10px"),
                        rx.text(f"{DashboardState.userLocation}", weight="bold", font_size="1.5em", color="lightgray"),
                        border_bottom="1em",
                        justify="between",
                        align_items="center",

                    ),

                    rx.fragment(
                        rx.flex(
                            # Card for Humidity with a water droplet icon
                            humidity(weather_info),

                            # Card for Cholesterol with a heart health icon
                            cholesterol(),

                            # Card for BMI with a scale icon
                            bmi(),

                            justify_content="center",
                            align_items="center",
                            flex_wrap="wrap",
                            spacing="9"
                        ),

                        factsLists(),
                    ),
                    padding_top="6em",
                ),
            )
        )
    )
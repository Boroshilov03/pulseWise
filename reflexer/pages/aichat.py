import asyncio
import reflex as rx
from reflexer.navigation import navbar
from reflexer import styles
import google.generativeai as genai
from reflex_motion import motion
from reflexer.alert import alert
import os

# Configure Google API
GOOGLE_API = "AIzaSyCQsYQDQbLZoMPhUnUdCgRM8wxv3iUM4Sg"
genai.configure(api_key=GOOGLE_API)

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System instruction


# Initialize the generative model

# Start conversation with predefined initial message


class ChatGemini(rx.State):

    localStorageData: str = rx.LocalStorage(name="questionInputs")
    question: str = ""
    chat_history: list[tuple[str, str]] = []
    loading: bool = False
    language: str = "English"

    def loadingStart(self):
        self.loading = True

    def loadingEnd(self):
        self.loading = False

    def changeLanguagetoEN(self):
        self.language = "English"


    def changeLanguagetoKorean(self):
        self.language = 'Korean'

    def changeLanguagetoSP(self):
        self.language = "Spanish"

    def changeLanguagetoHD(self):
        self.language = "Hindi"
    async def answer(self):

        if not self.question.strip():
            default_message = "Please ask something related to health and medical, stuff."
            self.chat_history.append(("I didn't put anything :(", default_message))
            self.loadingEnd()
            yield
            return

        system_instruction = f"""
            
            Give me response in {self.language}
            You are a Heart Attack Doctor and your job is to give short tips and tricks, suggest foods that promote heart health, and recommend foods to avoid in order to prevent heart attacks based on user input. Important: Give short and helpful response. You shall not do anything but talk about health and medical, biology related stuff. if anyone asks you to do anything beside health and medical, biology related stuff related. Please reply by saying **I am a health doctor not your friendly chat bot who can do anything ( ͡° ͜ʖ ͡°).**
            When replying keep in mind of the user health profile, answer based on the user profile data: {self.localStorageData}
            
            Important: Give very short and concise advice.
            """

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=generation_config,
            system_instruction=system_instruction,
            safety_settings=safety_settings,
        )

        doctorChat = model.start_chat(history=[
            {
                "role": "model",
                "parts": [f"""
                Give very short and concise advice in {self.language}
                This is the user info that was given. look over this when replying to user question. Also always mention users name when answering.
                {self.localStorageData}
                """]
            }
        ])

        doctorChat.send_message(self.question)
        answer = doctorChat.last.text

        self.chat_history.append((self.question, answer))
        self.question = ""

        self.loadingEnd()
        yield
        # Stream response letter by letter
        for i in range(len(answer)):
            # Pause to show the streaming effect.
            await asyncio.sleep(0.01)
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer[: i + 1],
            )
            yield

    def reset_chat(self):
        # Reset chat history and question
        self.chat_history: list[tuple[str, str]] = []
        self.question = ""


def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=styles.question_style),
            text_align="right",
        ),
        rx.box(
            rx.markdown(answer, style=styles.answer_style),
            text_align="left",
        ),
        margin_y="1em",
    )


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            ChatGemini.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(

            value=ChatGemini.question,
            placeholder="Ask your doctor here",
            on_change=ChatGemini.set_question,
            style={
                "height": "50px",
                "padding": "5px",
                "font-size": "1em",
                "border-radius": "2em",
                "transition": "border-color 0.2s ease",
                "box-sizing": "border-box",
                "width": "50rem"
            },
        ),
        rx.cond(
            (ChatGemini.loading == True),
            rx.button(
                rx.icon("briefcase-medical", size=20, color="white"),
                "Loading...",
                style={
                    "font_weight": "bold",
                    "bg": "red",
                    "color": "white",
                    "height": "50px",
                },
            ),
            motion(
                rx.button(
                    rx.icon("briefcase-medical", size=20, color="white"),
                    "Ask your doctor",
                    on_click=lambda: [
                        ChatGemini.loadingStart,
                        ChatGemini.answer
                    ],
                    style={
                        "font_weight": "bold",
                        "bg": "red",
                        "color": "white",
                        "height": "50px",
                    },
                ),
                while_hover={"scale": 0.9},
                while_tap={"scale": 0.9},
                transition={"type": "spring", "stiffness": 400, "damping": 17},
            )
        )
    )



@rx.page(on_load=ChatGemini.reset_chat)
def aichat():

    return rx.center(
            navbar(pageName="Doctor Chat"),

            rx.cond(
                ChatGemini.localStorageData.strip() == "",
                alert(),
                rx.vstack(
                    rx.vstack(
                        rx.heading(f"Your health profile", font_size="2em", align="center", margin_bottom="20px"),

                        rx.hstack(
                            rx.text(f"Choose your language: ", font_size="1.4em", color="black"),
                            motion(
                                rx.cond(
                                    ChatGemini.language == "English",
                                    rx.box(
                                        rx.text("English"),
                                        padding="0.7em",
                                        on_click=ChatGemini.changeLanguagetoEN,
                                        border_width="1px",
                                        color="white", weight="bold", bg="red", border_radius="5px",
                                        style={"cursor": "pointer"}
                                    ),
                                    rx.box(
                                        rx.text("English"),
                                        padding="0.7em",
                                        on_click=ChatGemini.changeLanguagetoEN,
                                        border_width="1px",
                                        color="red", weight="bold", bg="white", border_radius="5px",
                                        style={"cursor": "pointer"}
                                    )
                                ),
                                while_hover={"scale": 1.1},
                                while_tap={"scale": 0.9},
                                transition={"type": "spring", "stiffness": 400, "damping": 17},
                            ),
                            motion(
                                rx.cond(
                                    ChatGemini.language == "Korean",
                                    rx.box(
                                        rx.text("Korean"),
                                        padding="0.7em",
                                        on_click=ChatGemini.changeLanguagetoEN,
                                        border_width="1px",
                                        color="white", weight="bold", bg="red", border_radius="5px",
                                        style={"cursor": "pointer"}
                                    ),
                                    rx.box(
                                        rx.text("Korean"),
                                        padding="0.7em",
                                        on_click=ChatGemini.changeLanguagetoKorean,
                                        border_width="1px",
                                        color="red", weight="bold", bg="white", border_radius="5px",
                                        style={"cursor": "pointer"}
                                    )
                                ),
                                while_hover={"scale": 1.1},
                                while_tap={"scale": 0.9},
                                transition={"type": "spring", "stiffness": 400, "damping": 17},
                            ),
                            motion(
                                rx.cond(
                                    ChatGemini.language == "Spanish",
                                    rx.box(
                                        rx.text("Spanish"),
                                        padding="0.7em",
                                        on_click=ChatGemini.changeLanguagetoEN,
                                        border_width="1px",
                                        color="white", weight="bold", bg="red", border_radius="5px",
                                        style={"cursor": "pointer"}
                                    ),
                                    rx.box(
                                        rx.text("Spanish"),
                                        padding="0.7em",
                                        on_click=ChatGemini.changeLanguagetoSP,
                                        border_width="1px",
                                        color="red", weight="bold", bg="white", border_radius="5px",
                                        style={"cursor": "pointer"}
                                    )
                                ),
                                while_hover={"scale": 1.1},
                                while_tap={"scale": 0.9},
                                transition={"type": "spring", "stiffness": 400, "damping": 17},
                            ),
                            motion(
                                rx.cond(
                                    ChatGemini.language == "Hindi",
                                    rx.box(
                                        rx.text("Hindi"),
                                        padding="0.7em",
                                        on_click=ChatGemini.changeLanguagetoEN,
                                        border_width="1px",
                                        color="white", weight="bold", bg="red", border_radius="5px",
                                        style={"cursor": "pointer"}
                                    ),
                                    rx.box(
                                        rx.text("Hindi"),
                                        padding="0.7em",
                                        on_click=ChatGemini.changeLanguagetoHD,
                                        border_width="1px",
                                        color="red", weight="bold", bg="white", border_radius="5px",
                                        style={"cursor": "pointer"}
                                    )
                                ),
                                while_hover={"scale": 1.1},
                                while_tap={"scale": 0.9},
                                transition={"type": "spring", "stiffness": 400, "damping": 17},
                            ),
                            gap="2em",
                        ),

                        rx.container(
                            chat(),
                            action_bar(),
                        ),
                        spacing="4",
                        width="100%",
                        padding_top="6em",
                    ),
                )
            )
        )




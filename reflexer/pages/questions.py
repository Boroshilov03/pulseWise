"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import asyncio
import json

from rxconfig import config
import reflex as rx
from reflexer.navigation import navbar
from reflexer.pages.dashboard import DashboardState
import pickle
class QuestionTrack(rx.State):

    current_question_index: int = 0
    question_inputs_local: str = rx.LocalStorage(name="questionInputs")

    question_inputs: list[tuple[str, str]] = [
            ("What is your full name?", ""),
            ("What is your email address?", ""),
            ("What is your age?", ""),
            ("What is your height in centimeters?", ""),
            ("What is your weight?", ""),
            ("What is your cholesterol level?", ""),
            ("Are you currently a smoker?", ""),
            ("Do you consume alcohol regularly?", ""),
            ("Have you ever experienced a stroke?", ""),
            ("What is your biological sex?", ""),
            ("Do you have a history of diabetes?", ""),
            ("Do you exercise regularly?", ""),
            ("How many hours do you sleep nightly?", ""),
            ("Do you have a history of asthma?", ""),
            ("Do you have any kidney conditions?", ""),
            ("Have you ever had skin cancer?", ""),
        ]

    questionCount: int = len(question_inputs) - 1

    loading = False

    def loadingStart(self):
        self.loading = True

    def loadingEnd(self):
        self.loading = False

    def next_question(self):
        current_input = self.question_inputs[self.current_question_index][1]

        if current_input.strip():
            if self.current_question_index < len(self.question_inputs) - 1:
                self.current_question_index += 1


    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1

    def add_input(self, input_text: str):
        self.question_inputs[self.current_question_index] = (
            self.question_inputs[self.current_question_index][0],
            input_text
        )

    def reset_data(self):
        self.current_question_index = 0
        self.question_inputs: list[tuple[str, str]] = [
            ("What is your full name?", ""),
            ("What is your email address?", ""),
            ("What is your age?", ""),
            ("What is your height in centimeters?", ""),
            ("What is your weight?", ""),
            ("What is your cholesterol level?", ""),
            ("Are you currently a smoker?", ""),
            ("Do you consume alcohol regularly?", ""),
            ("Have you ever experienced a stroke?", ""),
            ("What is your biological sex?", ""),
            ("Do you have a history of diabetes?", ""),
            ("Do you exercise regularly?", ""),
            ("How many hours do you sleep nightly?", ""),
            ("Do you have a history of asthma?", ""),
            ("Do you have any kidney conditions?", ""),
            ("Have you ever had skin cancer?", ""),
        ]

    def save_to_local_storage(self):

        localStore_data = {q: i for q, i in self.question_inputs}

        try:
            self.question_inputs_local = json.dumps(localStore_data)
        except TypeError as error:
            print(error)


    async def delayed_redirect(self):
        await asyncio.sleep(2)



def input_field() -> rx.Component:
    return rx.input(
        placeholder="Answer the question here..",
        on_change=QuestionTrack.add_input,
        value=QuestionTrack.question_inputs[QuestionTrack.current_question_index][1],
        radius="large",
        style={
            "width": "25rem",
            "height": "50px",
            "padding": "5px",
            "font-size": "1.5em",
            "border-radius": "2em",
            "transition": "border-color 0.2s ease",
            "box-sizing": "border-box",
        },
    )


def action_bar() -> rx.Component:
    return rx.flex(
        (
            rx.cond(
                QuestionTrack.current_question_index <= 0,
                rx.flex(
                    rx.button(
                        rx.icon("chevron-left", size=18, color="white"),
                        "Prev Question",
                        size="3",
                        background_color="gray",
                    )
                ),
                rx.flex(
                    rx.button(
                        rx.icon("chevron-left", size=18, color="white"),
                        "Prev Question",
                        on_click=QuestionTrack.prev_question,
                        size="3",
                    )
                )
            )
        ),

        rx.cond(
            (QuestionTrack.current_question_index == QuestionTrack.questionCount),
            (
                rx.cond(
                    QuestionTrack.loading,
                    rx.flex(
                        rx.button(
                            rx.icon("heart", size=18, color="white"),  # Adjusted size and color for better visibility
                            "Analyzing your data.....",
                            size="3",
                            background_color="red",
                            color="white",
                            style={"padding": "10px", "alignItems": "center"},
                            # Added padding and alignment for aesthetics
                        )
                    ),
                    rx.flex(
                        rx.button(
                            rx.icon("heart", size=18, color="white"),  # Adjusted size and color for better visibility
                            "Analyze your response",
                            size="3",
                            on_click=lambda: [
                                QuestionTrack.loadingStart,
                                QuestionTrack.save_to_local_storage,
                                QuestionTrack.delayed_redirect,
                                QuestionTrack.loadingEnd,
                                rx.redirect("/dashboard")
                            ],
                            background_color="red",
                            color="white",
                            style={"padding": "10px", "alignItems": "center"},
                            # Added padding and alignment for aesthetics
                        )
                    )
                )

            ),
            (
                rx.cond(
                    (QuestionTrack.question_inputs[QuestionTrack.current_question_index][1].strip() == ""),
                    rx.flex(
                        rx.button(
                            rx.icon("chevron-right", size=18, color="white"),
                            "Next Question",
                            size="3",
                            background_color="gray",
                        )
                    ),
                    rx.flex(
                        rx.button(
                            rx.icon("chevron-right", size=18, color="white"),
                            "Next Question",
                            on_click=QuestionTrack.next_question,
                            size="3"
                        )
                    )
                )
            ),
        ),
        justify="between", spacing="5"
    )


def info_hovercard() -> rx.Component:

    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Need help?", variant='outline')),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Welcome to Pulsewise!"),
                rx.dialog.close(
                    rx.button(
                        rx.icon("circle-x", size=15, color="red"),
                        "Close Dialog", size="2", variant="ghost", color="red"),
                ),

                justify="between", align="start",
            ),
            rx.dialog.description(
                "Please answer the questions as accurately as possible, so we can analyze your records and guide you to a healthy lifestyles.",
            ),
        ),
    )


@rx.page(on_load=QuestionTrack.reset_data)
def questions() -> rx.Component:
    return rx.center(
        navbar( pageName="Questions Page"),
        rx.vstack(
            rx.desktop_only(
                rx.center(
                    rx.text(
                        f"{QuestionTrack.current_question_index + 1}. {QuestionTrack.question_inputs[QuestionTrack.current_question_index][0]}",
                        font_weight="bold",
                        font_size="2.5em",
                    ),
                )
            ),

            rx.mobile_only(
                rx.center(
                    rx.text(
                        f"{QuestionTrack.current_question_index + 1}. {QuestionTrack.question_inputs[QuestionTrack.current_question_index][0]}",
                        font_weight="bold",
                        font_size="1.4em",
                    ),
                )
            ),

            input_field(),
            action_bar(),
            info_hovercard(),
            align="center", spacing="5"
        ),
        align="center", justify="center", height="100vh", width="100%", spacing="7",

    )

#panel serve main.py --show 
import os
import re
import random
from pathlib import Path
from threading import Thread # Asyncio
from functools import partial

import openai
import panel as pn
import speech_recognition as sr


pn.extension(nthreads=4)
pn.config.sizing_mode = "stretch_width"
os.path.join(os.path.dirname(__file__))

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        self.stop_listening = None

        # path to this directory
        this_directory = Path(__file__).parent.absolute()
        self.detect_prompt = (this_directory / "detect.txt").read_text()
        self.recommend_prompt = (this_directory / "recommend.txt").read_text()
        self.validate_prompt = (this_directory / "validate.txt").read_text()

    def prompt_gpt(
        self,
        system_input: str,
        user_input: str,
        model="gpt-4",
        openai_env_name: str = "OPENAI_API_KEY",
        stream: bool = False,
    ) -> dict:
        openai.api_key = os.environ[openai_env_name]

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_input},
                {"role": "user", "content": user_input},
            ],
            temperature=1,
            max_tokens=4096,
            stream=stream,
        )
        if not stream:
            response = response.choices[0]["message"]["content"]
        return response

    def blocking_task(self, recognizer: sr.Recognizer, audio: sr.AudioSource, doc=None):
        print("STARTING!!!")
        try:
            text = recognizer.recognize_google(audio)
            self.transcription.value = f"{self.transcription.value} {text}"
            try:
                likelihood_output = self.prompt_gpt(
                    self.detect_prompt, self.transcription.value
                )
                print(likelihood_output)
                self.likelihood.value = int(re.findall(r"\d+", likelihood_output)[0])
            except IndexError as e:
                print(e)
            if self.likelihood.value is not None:
                if self.likelihood.value == 100:
                    self.likelihood.value -= random.randint(0, 15)

                if self.likelihood.value > 40:
                    self.recommendations.loading = True
                    try:
                        self.recommendations.value = self.prompt_gpt(
                            self.recommend_prompt, self.transcription.value[-2098:]
                        )
                    finally:
                        self.recommendations.loading = False
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results from service; {0}".format(e))

    def transcribe_audio(
        self, recognizer: sr.Recognizer, audio: sr.AudioSource
    ) -> None:
        """
        Transcribes audio using Google Speech API.
        """
        thread = Thread(target=partial(self.blocking_task, recognizer=recognizer, audio=audio))
        thread.start()

    def start_listening(self, event) -> None:
        if event.new:
            self.stop_listening = self.recognizer.listen_in_background(
                self.microphone, self.transcribe_audio, phrase_time_limit=10
            )
        else:
            self.stop_listening()

    def reset_all(self, event):
        self.listen.value = False
        self.transcription.value = ""
        self.likelihood.value = None
        self.recommendations.value = ""

    def validate_phone(self, event):
        self.authenticated.color = "light"
        validate_output = self.prompt_gpt(
            self.validate_prompt, event.new
        )
        self.authenticated.value = True
        if "True" in validate_output:
            self.authenticated.color = "success"
            self.phone_details.value = validate_output.split("True")[1]
        else:
            self.authenticated.color = "danger"
            self.phone_details.value = validate_output

    def trigger_listen(self, event):
        self.listen.value = True

    def panel(self):
        self.listen = pn.widgets.Toggle(name="Begin listening", button_type="success")
        self.listen.param.watch(self.start_listening, "value")

        reset = pn.widgets.Button(name="Reset")
        reset.param.watch(self.reset_all, "clicks")

        self.phone_number = pn.widgets.TextInput(
            placeholder="Authenticate a phone number",
        )
        self.phone_number.param.watch(self.validate_phone, "value")
        self.authenticated = pn.indicators.BooleanStatus(
            value=False, color="secondary", align="center",
        )
        self.phone_number.param.watch(self.trigger_listen, "value")
        phone_row = pn.Row(self.phone_number, self.authenticated)
        self.phone_details = pn.widgets.StaticText(
            name="Caller", value="N/A",
        )

        self.transcription = pn.widgets.TextAreaInput(
            placeholder="Begin listening to see transcription...",
            sizing_mode="stretch_both",
        )
        self.likelihood = pn.indicators.Number(
            name="Scam Likelihood",
            value=None,
            format="{value}%",
            colors=[
                (0.2, "#006B3D"),
                (0.4, "#7BB662"),
                (0.6, "#FFD301"),
                (0.8, "#E03C32"),
                (1, "#D61F1F"),
            ],
            align=("center", "end"),
        )
        self.recommendations = pn.widgets.TextAreaInput(
            placeholder="Recommendations only appear if likely a scam...",
            sizing_mode="stretch_both",
            )

        sidebar_column = pn.Column(
            phone_row,
            self.phone_details,
            pn.layout.Divider(),
            self.likelihood,
            self.listen,
            reset,
            sizing_mode="stretch_both",
        )
        main_column = pn.Column(
            self.transcription,
            self.recommendations,
            sizing_mode="stretch_both",
        )
        template = pn.template.FastListTemplate(
            title="SCAMTECT",
            sidebar=[sidebar_column],
            main=[main_column],
            sidebar_width=300,
            accent="#A01346",
            font="Roboto",
        )
        template.servable()


speech_recognizer = SpeechRecognizer()
speech_recognizer.panel()

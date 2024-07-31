from openai import OpenAI
import os
from os import path
from dotenv import load_dotenv
import urllib.request as req

load_dotenv()

OPEN_AI_TOKEN = os.getenv('AI_TOKEN')
TEMP_FOLDER = './data'

class transcription():
    SYSTEM_PROMPT = ''

    # def __init__(self) -> None:
        # self.SYSTEM_PROMPT = "You are a helpful transcription assistant. "
        # self.SYSTEM_PROMPT += "Your task is analyze a timestamped transcription of a conference. "
        # self.SYSTEM_PROMPT += "The number of speakers can vary. "
        # self.SYSTEM_PROMPT += "Your job is to focuse on the individual that is providing an answer or response and use the individual questioning as guidance. "
        # self.SYSTEM_PROMPT += "You are to infer based on the dialogue, who is saying what, and inject the speaker into each line thus: "
        # self.SYSTEM_PROMPT += "For example, if the lines are:\n"
        # self.SYSTEM_PROMPT += "15.0-20.0: Did you have a good day today?\n"
        # self.SYSTEM_PROMPT += "20.0-26.0: Yeah, it was alright\n\n"
        # self.SYSTEM_PROMPT += "Then you should return:\n"
        # self.SYSTEM_PROMPT += "15.0-20.0: [Teacher] Did you have a good day today?\n"
        # self.SYSTEM_PROMPT += "20.0-26.0: [Participant] Yeah, it was alright\n\n"
        # self.SYSTEM_PROMPT += "You should do this for every single line in the transcript. "
        # self.SYSTEM_PROMPT += "Do not assume that each line is alternating between Particiant and Teacher. "
        # self.SYSTEM_PROMPT += "Read the dialog line by line, and change speaker based on sentence structure. "
        # self.SYSTEM_PROMPT += "Furthermore, you are to correct any spelling discrepancies in the transcribed text, "
        # self.SYSTEM_PROMPT += "adding necessary punctuation such as periods, commas, and capitalization, and use only the context provided. "
    #     self.SYSTEM_PROMPT += "Do not add any additional context or information that is not present in the dialogue. "
        
    # def correct_trascript(self, trascripted_text: str, temperature = 0)->str:        
    #     client = OpenAI(api_key = OPEN_AI_TOKEN)
    #     response = client.chat.completions.create(
    #         model="gpt-4-turbo-preview",
    #         temperature=temperature,
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": self.SYSTEM_PROMPT
    #             },
    #             {
    #                 "role": "user",
    #                 "content": trascripted_text
    #             }
    #         ]
    #     )
    #     return response.choices[0].message.content

    # def trascribe_audio(self, input_file: str, is_need_delete_source = True):
    #     from datetime import datetime
    #     client = OpenAI(api_key = OPEN_AI_TOKEN)
    #     print(f'[{datetime.now()}]: Transcribe "{input_file}" processing started...')
    #     with open(f"{input_file}", "rb") as audio_file:
    #         transcription = client.audio.transcriptions.create(
    #             model="whisper-1",
    #             file=audio_file,
    #             language="en",
    #             response_format="verbose_json",
    #             timestamp_granularities=["segment"]
    #         )

    #     transcript_text = ''
    #     for segment in transcription.segments:
    #         transcript_text+= f"{round(segment['start'], 2)}-{round(segment['end'], 2)}:{segment['text']}\n"

    #     if is_need_delete_source:
    #         os.remove(input_file)
    #     return transcript_text
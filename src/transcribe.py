from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class TranscriptionHandler:

    SYSTEM_PROMPT = ''

    def __init__(self) -> None:
        self.api_key = os.getenv('AI_TOKEN')
        self.client = self._init_client()

        self.SYSTEM_PROMPT = "You are a helpful transcription assistant."
        self.SYSTEM_PROMPT += "Your task is to analyze a timestamped transcription of a feedback dialogue between two individuals at a conference."
        self.SYSTEM_PROMPT += "One of the individuals is the Operator and the other is the Attendee."
        self.SYSTEM_PROMPT += "You are to infer based on the dialogue who is saying what, and inject the speaker into each line using the following format: "
        self.SYSTEM_PROMPT += "For example, if the lines are:\n"
        self.SYSTEM_PROMPT += "15.0-20.0: Did you have a good day today?\n"
        self.SYSTEM_PROMPT += "20.0-26.0: Yeah, it was alright.\n"
        self.SYSTEM_PROMPT += "26.0-29.0: I particularly enjoyed the latter workshops.\n"
        self.SYSTEM_PROMPT += "29.0-36.0: They were so educating and can't wait for what is to come next.\n\n"
        self.SYSTEM_PROMPT += "Then you should return:\n"
        self.SYSTEM_PROMPT += "15.0-20.0: [Operator] Did you have a good day today?\n"
        self.SYSTEM_PROMPT += "20.0-26.0: [Attendee] Yeah, it was alright. 26.0-29.0: [Attendee] I particularly enjoyed the latter workshops. 29.0-36.0: [Attendee] They were so educating and can't wait for what is to come next.\n\n"
        self.SYSTEM_PROMPT += "If a single sentence or dialogue is split across multiple timestamped segments, combine them into one line with the first timestamp, as demonstrated above."
        self.SYSTEM_PROMPT += "You should do this for every single line in the transcript."
        self.SYSTEM_PROMPT += "Do not assume that each line is alternating between Operator and Attendee."
        self.SYSTEM_PROMPT += "Read the dialogue line by line and change speakers based on the sentence structure."
        self.SYSTEM_PROMPT += "Additionally, you are to tokenize any sensitive information and correct any spelling discrepancies in the transcribed text."
        self.SYSTEM_PROMPT += "Add necessary punctuation such as periods, commas, and capitalization, and use only the context provided."
        self.SYSTEM_PROMPT += "Do not add any additional information or change the meaning of the text."

    def _init_client(self):
        try:
            client = OpenAI(api_key = self.api_key)
            print(f'[{datetime.now()}]: OpenAI client initialized successfully.')
            return client
        
        except Exception as e:
            print(f'[{datetime.now()}]: Failed to initialize OpenAI client: {e}')
    
    def correct_transcript(self, transcripted_text: str, temperature = 0)->str:        
        print(f'[{datetime.now()}]: Structuring transcript processing started...')
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": transcripted_text
                    }
                ]
            )
            print(f'[{datetime.now()}]: Structuring transcript processing completed.')
            return response.choices[0].message.content

        except Exception as e:
            print(f'[{datetime.now()}]: Error during transcript correction: {e}')
            return None
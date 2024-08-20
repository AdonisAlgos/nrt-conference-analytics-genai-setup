from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Whisper:

    def __init__(self) -> None:
        self.api_key = os.getenv('AI_TOKEN')
        self.client = self.init_client()

    def init_client(self):
        try:
            client = OpenAI(api_key = self.api_key)
            print(f'[{datetime.now()}]: OpenAI client initialized successfully.')
            return client
        except Exception as e:
            print(f'[{datetime.now()}]: Failed to initialize OpenAI client: {e}')
        
    def transcribe(self, audio_file_path: str):
        
        print(f'[{datetime.now()}]: Whisper transcribe "{audio_file_path}" processing started...')
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en",
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
                print(f'[{datetime.now()}]: Transcribe "{audio_file_path}" processing completed.')
                return transcription.text
            
        except Exception as e:
            print(f'[{datetime.now()}]: Error during transcription: {e}')
            return None




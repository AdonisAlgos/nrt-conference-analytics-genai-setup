from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Whisper:

    def __init__(self) -> None:
        self.api_key = os.getenv('AI_TOKEN')
        self.client = self._init_client()

    def _init_client(self):
        try:
            client = OpenAI(api_key = self.api_key)
            print(f'[{datetime.now()}]: OpenAI client initialized successfully.')
            return client
        except Exception as e:
            print(f'[{datetime.now()}]: Failed to initialize OpenAI client: {e}')
        
    def transcribe(self, audio_file_path: str, is_need_delete_source = True):
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

            transcript_text = ''
            for segment in transcription.segments:
                transcript_text += f"{round(segment['start'], 2)}-{round(segment['end'], 2)}:{segment['text']}\n"

            print(f'[{datetime.now()}]: Transcribe "{audio_file_path}" processing completed.')
            if is_need_delete_source:
                os.remove(audio_file_path)
            return transcript_text
            
        except Exception as e:
            print(f'[{datetime.now()}]: Error during transcription: {e}')
            return None




from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
OPEN_AI_TOKEN = os.getenv('AI_TOKEN')

class Transcriber:

    def transcribe(self, input_file: str):
        client = OpenAI(api_key = OPEN_AI_TOKEN)
        print(f'[{datetime.now()}]: Transcribe "{input_file}" processing started...')

        with open(f"{input_file}", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en",
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )
        return transcription
    
    def diarise(self,segments):
        diarised_segments = []
        speaker_id = 1
        prev_end_segment = 0
        
        for segment in segments:
            
            if segment["start"] - prev_end_segment > 1:
                speaker_id += 1

            print(f"Speaker {speaker_id}\n {round(segment['start'], 2)}-{round(segment['end'], 2)}: {segment['text']}\n\n")
            
            diarised_segments.append(
                {
                    "speaker": speaker_id,
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"]
                }
            )
            
            prev_end_segment = segment["end"]
        
        return diarised_segments
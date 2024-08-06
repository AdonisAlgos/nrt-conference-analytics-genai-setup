from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
OPEN_AI_TOKEN = os.getenv('AI_TOKEN')

class Transcriber:
    SYSTEM_PROMPT = ''

    def __init__(self) -> None:
        self.SYSTEM_PROMPT = (
            "You are a helpful transcription assistant. Your task is to analyze a transcription of a conference "
            "and identify when the speaker changes. Use the following guidelines to determine a change in speaker:\n\n"
        )
        self.SYSTEM_PROMPT += (
            "1. Abrupt Change in Talking Point: Look for shifts in the topic of conversation.\n"
            "2. Personal References: Notice changes in perspective indicated by personal pronouns (e.g., 'I' vs. 'we').\n"
            "3. Distinctive Style or Content: Pay attention to differences in speaking style or content.\n"
            "4. Explicit Mention of Different People: Look for mentions or references to different individuals.\n"
            "5. Logical Breaks or Pauses: Note any natural breaks or pauses that suggest a switch in speakers.\n"
            "6. Contextual Consistency: Ensure the context flows logically. If it feels disjointed, a speaker change "
            "may have occurred.\n\n"
        )
        self.SYSTEM_PROMPT += (
            "Examples:\n"
            "1. Abrupt Change in Topic:\n"
            "   - 'We had a great time at the conference.'\n"
            "   - 'I think the keynote speaker was very inspiring.'\n"
            "   Label:\n"
            "   - [Speaker 1] 'We had a great time at the conference.'\n"
            "   - [Speaker 2] 'I think the keynote speaker was very inspiring.'\n\n"
        )
        self.SYSTEM_PROMPT += (
            "2. Change in Pronouns or Perspective:\n"
            "   - 'I found the workshop very informative.'\n"
            "   - 'We also need to consider the budget for next year.'\n"
            "   Label:\n"
            "   - [Speaker 1] 'I found the workshop very informative.'\n"
            "   - [Speaker 2] 'We also need to consider the budget for next year.'\n\n"
        )
        self.SYSTEM_PROMPT += (
            "3. Distinctive Style or Content:\n"
            "   - 'The technical details were fascinating.'\n"
            "   - 'Yes, but we must focus on implementation.'\n"
            "   Label:\n"
            "   - [Speaker 1] 'The technical details were fascinating.'\n"
            "   - [Speaker 2] 'Yes, but we must focus on implementation.'\n\n"
        )
        self.SYSTEM_PROMPT += (
            "You should do this for every single line in the transcript. Do not assume that each line is alternating "
            "between speakers. Read the dialog line by line, and change the speaker based on sentence structure. "
            "Furthermore, you are to correct any spelling discrepancies in the transcribed text, adding necessary "
            "punctuation such as periods, commas, and capitalization, and use only the context provided. Do not add "
            "any additional context or information that is not present in the dialogue.\n\n"
        )


    def transcribe(self, input_file: str):
        client = OpenAI(api_key = OPEN_AI_TOKEN)
        print(f'[{datetime.now()}]: Transcribe "{input_file}" processing started...')
        try:
            with open(f"{input_file}", "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en",
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
        except Exception as e:
            print(f'[{datetime.now()}]: Error during transcription: {e}')
            return None

        print(f'[{datetime.now()}]: Transcribe "{input_file}" processing completed.')
        return transcription.text
    
    def correct_transcript(self, trascripted_text: str, temperature = 0)->str:        
        client = OpenAI(api_key = OPEN_AI_TOKEN)
        print(f'[{datetime.now()}]: Structuring transcript processing started...')
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": trascripted_text
                    }
                ]
            )
        except Exception as e:
            print(f'[{datetime.now()}]: Error during transcript correction: {e}')
            return None
        
        print(f'[{datetime.now()}]: Structuring transcript processing completed.')
        return response.choices[0].message.content
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class TranscriptionHandler:
    


    SYSTEM_PROMPT = ''

    def __init__(self) -> None:

        self.api_key = os.getenv('AI_TOKEN')
        self.client = self.init_client()

        self.SYSTEM_PROMPT = (
            "You are a helpful transcription assistant. Your task is to analyze a transcription of a conference, "
            "identify when the speaker changes, and appropriately tokenize sensitive information. You must strictly adhere "
            "to the instructions provided by the user, ensuring that you do not add any commentary or text before or after your response.\n\n"
        )
        self.SYSTEM_PROMPT += (
            "The following text is a transcript of a recorded reflection session about a conference. The purpose of this session "
            "is to capture feedback on the conference. Use the guidelines below to accurately identify speaker changes and tokenize sensitive information.\n\n"
        )
        self.SYSTEM_PROMPT += (
            "### Speaker Change Guidelines:\n\n"
            "- **Abrupt Change in Talking Point**: Identify shifts in the topic of conversation that may indicate a new speaker.\n"
            "- **Personal References**: Notice changes in perspective, especially shifts in personal pronouns (e.g., 'I' vs. 'we').\n"
            "- **Distinctive Style or Content**: Pay attention to differences in speaking style or content that suggest a different speaker.\n"
            "- **Explicit Mention of Different People**: Look for mentions or references to different individuals, which may signal a speaker change.\n"
            "- **Logical Breaks or Pauses**: Note any natural breaks or pauses that could indicate a transition to a new speaker.\n"
            "- **Contextual Consistency**: Ensure the context flows logically. If the flow seems disjointed, a speaker change may have occurred.\n\n"
        )
        self.SYSTEM_PROMPT += (
            "### Tokenization Guidelines:\n\n"
            "- **Sensitive Information**: Replace sensitive information such as names, company names, and specific locations with tokens. Use tokens like '[Name1]', '[Company1]', '[Location1]'.\n\n"
        )
        self.SYSTEM_PROMPT += (
            "### Examples:\n\n"
            "1. **Abrupt Change in Topic**:\n"
            "   - 'We had a great time at the conference.'\n"
            "   - 'I think the keynote speaker was very inspiring.'\n"
            "   - **Label**:\n"
            "     - [Speaker 1] 'We had a great time at the conference.'\n"
            "     - [Speaker 2] 'I think the keynote speaker was very inspiring.'\n\n"
        )
        self.SYSTEM_PROMPT += (
            "2. **Change in Pronouns or Perspective**:\n"
            "   - 'I found the workshop very informative.'\n"
            "   - 'We also need to consider the budget for next year.'\n"
            "   - **Label**:\n"
            "     - [Speaker 1] 'I found the workshop very informative.'\n"
            "     - [Speaker 2] 'We also need to consider the budget for next year.'\n\n"
        )
        self.SYSTEM_PROMPT += (
            "3. **Distinctive Style or Content**:\n"
            "   - 'The technical details were fascinating.'\n"
            "   - 'Yes, but we must focus on implementation.'\n"
            "   - **Label**:\n"
            "     - [Speaker 1] 'The technical details were fascinating.'\n"
            "     - [Speaker 2] 'Yes, but we must focus on implementation.'\n\n"
        )
        self.SYSTEM_PROMPT += (
            "### Final Instructions:\n\n"
            "Apply these principles to every line in the transcript. Do not assume that each line alternates between speakers. "
            "Carefully read the dialogue line by line, and determine speaker changes based on sentence structure and context. "
            "Additionally, correct any spelling errors in the transcribed text, add necessary punctuation (such as periods, commas, "
            "and capitalization), and rely solely on the provided context. Do not introduce any additional information or context "
            "that is not present in the transcript."
        )

    def init_client(self):
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
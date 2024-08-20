from datetime import datetime
from media import Media
from transcribe import TranscriptionHandler
from salesforce import SalesForce
from whisper import Whisper


def main():
    try:
        # Step 0: Initiate Salesforce connection and extract instance url
        print(f'[{datetime.now()}]: Initialising Salesforce connection...')
        salesforce_client = SalesForce()
        full_url = f"https://{salesforce_client.instance}{'version_data'}" # version_data - path to audio file in Salesforce - to be passed 

        # Step 1: Download the audio file from Salesforce
        print(f'[{datetime.now()}]: Initialising audio file download...')
        media = Media()
        audio_file_path = media.download_file(full_url, salesforce_client.headers)

        # Step 2: Transcribe the audio file using Whisper API
        print(f'[{datetime.now()}]: Establishing OpenAI Whisper API connection...')
        whisper = Whisper()
        transcription = whisper.transcribe(audio_file_path)

        # Step 3: Refine (correct grammar & tokenize) the transcription
        print(f'[{datetime.now()}]: Refining transcription using OpenAI GPT-4o...')
        transcription_service = TranscriptionHandler()
        refined_transcription = transcription_service.correct_transcript(transcription)

        # Step 4: Update Salesforce with the refined transcription
        print(f'[{datetime.now()}]: Initialising Conference object update with refined transcription...')
        salesforce_client.update_conference_record({'conference_id'}, refined_transcription) # conference_id - unique identifier for conference record in Salesforce - to be passed

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

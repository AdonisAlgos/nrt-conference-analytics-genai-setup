import argparse
from datetime import datetime
from media import Media
from transcribe import TranscriptionHandler
from salesforce import SalesForce
from whisper import Whisper

def main(media_type, conference_id, media_url):
    try:
        # Step 0: Initiate Salesforce connection and extract instance url
        print(f'[{datetime.now()}]: Initialising Salesforce connection...')
        salesforce_client = SalesForce()

        # Step 1: Download the audio file from Salesforce
        print(f'[{datetime.now()}]: Initialising audio file download...')
        media = Media(media_type, media_url)
        media_file_size = media.download_file_size(salesforce_client.instance, salesforce_client.headers)

        if media.check_media_size(media_file_size):
            media_file_path = media.download_file(salesforce_client.instance, salesforce_client.headers)
            audio_file_path = media.extract_audio(media_file_path)

        # Step 2: Transcribe the audio file using the Whisper API
        print(f'[{datetime.now()}]: Establishing OpenAI Whisper API connection...')
        whisper = Whisper()
        transcription = whisper.transcribe(audio_file_path)

        # Step 3: Refine (correct grammar & tokenize) the transcription
        print(f'[{datetime.now()}]: Refining transcription using OpenAI GPT-4...')
        transcription_service = TranscriptionHandler()
        refined_transcription = transcription_service.correct_transcript(transcription)

        # Step 4: Update Salesforce with the refined transcription
        print(f'[{datetime.now()}]: Initialising Conference object update with refined transcription...')
        salesforce_client.update_conference_record(conference_id, refined_transcription)

    except Exception as e:
        print(f'[{datetime.now()}]: Error during process: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process media files and update Salesforce with transcriptions.")
    parser.add_argument('--media_type', required=True, help='Type of media (e.g., audio, video)')
    parser.add_argument('--conference_id', required=True, help='Unique identifier for the conference record in Salesforce')
    parser.add_argument('--media_url', required=True, help='URL of the media file to download and transcribe')

    args = parser.parse_args()

    main(args.media_type, args.conference_id, args.media_url)

import os
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
from datetime import datetime

TEMP_FOLDER = './data'
load_dotenv()

class Media():

    def __init__(self, media_type, media_url) -> None:
        self.media_limits = {
            'video': self._load_media_limits('MAX_VIDEO', 500, float),
            'audio': self._load_media_limits('MAX_AUDIO', 24, float)
        }
        self.media_type = media_type.lower()
        self.media_url = media_url

    
    def _load_media_limits(self, limit_name, default, limit_type=float):
        try:
            limit = os.getenv(limit_name, default)
            return limit_type(limit)
        
        except Exception as e:
            print(f'[{datetime.now()}]: Error loading {limit_name} media limit: {e}')
            return default
            
    
    def check_media_size(self, file_size):
        limit = self.media_limits.get(self.media_type)

        if file_size <= limit:
            return True
        else:
            print(f'[{datetime.now()}]: File size exceeds limit of {limit}MB.')
            return False
        
        
    def extract_audio(self, file_path,  output_format:str = "mp3" , is_need_delete_source = True):
        if self.media_type != 'video':
            return file_path

        folder, file_name = os.path.split(file_path)
        output_file = file_name.replace(".mp4", ".mp3")
        result_file_path = f'{folder}/{output_file}'

        try:
            audio = AudioSegment.from_file(file_path, format="mp4")
            audio.export(f'{result_file_path}', format = output_format)

        except Exception as ex:
            print(f'[{datetime.now()}]: Error during audio extraction: {ex}')
            result_file_path = ''

        finally:
            if is_need_delete_source:
                os.remove(file_path)
                
        return result_file_path
       
       
    def download_file_size(self, salesforce_client_instance, session_headers):
        file_url = f"https://{salesforce_client_instance}{self.media_url}"

        try:
            response = requests.head(file_url, headers=session_headers)
            size_in_bytes = int(response.headers.get('Content-Length', 0))
            size_in_mb = round(size_in_bytes / (1024 * 1024), 2)
            return size_in_mb
        
        except requests.RequestException as e:
            print(f'[{datetime.now()}]: Error during file size retrieval: {e}')
            return 0.0


    def download_file(self, salesforce_client_instance, session_headers, file_name='temp.mp3'):
        file_url = f"https://{salesforce_client_instance}{self.media_url}"

        # Ensuring directory exists
        if not os.path.exists(TEMP_FOLDER):
            os.makedirs(TEMP_FOLDER)
        
        path = os.path.join(TEMP_FOLDER, file_name)
        print(f'[{datetime.now()}]: Downloading file from {file_url} ...')

        try:
            response = requests.get(file_url, headers=session_headers)
            if response.status_code == 200:
                with open(path, 'wb') as file:
                    file.write(response.content)

                print(f'[{datetime.now()}]: File downloaded successfully to path {path}')
                return path
            
        except Exception as e:
            print(f'[{datetime.now()}]: Error during file download: {e}')



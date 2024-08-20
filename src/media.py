import os
import requests
from datetime import datetime

TEMP_FOLDER = './data'

class Media():

    def download_file(self, file_url, session_headers, file_name='temp.m4a'):

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

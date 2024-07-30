import simple_salesforce
import os
from datetime import datetime
import requests
import json

class SalesForce():

    def __init__(self) -> None:
        self.consumer_key = os.getenv('CONSUMER_KEY')
        self.consumer_secret = os.getenv('CONSUMER_SECRET')
        self.domain = os.getenv('SALESFORCE_DOMAIN')

        # self.media_url = f"https://{domain}.salesforce.com/services/apexrest/mediaUrl"
        # self.setting_url = f"https://{domain}.salesforce.com/services/data/v58.0/query/?q=SELECT+Is_Active__c+from+Media_Processing_Config__mdt+WHERE+DeveloperName+=+'Media_Transcription'"

        if not all([self.consumer_key, self.consumer_secret, self.domain]):
                    raise ValueError("One or more Salesforce environment variables are missing.")

    # def check_enable_media_activity(self)-> bool:
    #     print(f'[{datetime.now()}]: Started check if Media transcribe enabled')
    #     sf = self.init_client()
    #     headers =  sf.headers
    #     result = {}
    #     result = False
    #     res = requests.get(self.setting_url, headers = headers)
    #     response_content = res.json()
    #     if type(response_content) == dict:
    #         for record in response_content['records']:
    #             result = record['Is_Active__c']
    #     return result

    # def init_medias(self, session_ids:list) -> bool:
    #     print(f'[{datetime.now()}]: Started Init media for getting links')
    #     sf = self.init_client()
    #     headers =  sf.headers
    #     res = requests.patch(self.media_url, json=session_ids, headers = headers)
    #     if res.status_code == 200 and res.text == 'true':
    #         return True
    #     return False

    # def get_media_url(self, session_ids:list):
    #     print(f'[{datetime.now()}]: Started getting media links')
    #     sf = self.init_client()
    #     headers =  sf.headers
    #     result = {}
    #     res = requests.post(self.media_url, json=session_ids, headers = headers)
    #     if res.status_code == 200:
    #         result = json.loads(res.json())
    #     return result

    # def init_client(self):
    #     return simple_salesforce.Salesforce(

    #          consumer_key = self.consumer_key,
    #                                         consumer_secret = self.consumer_secret,
    #                                         organizationId = self.org_id,
    #                                         #  instance_url = self.domain,

    #                                         # privatekey_file
    #                                         domain = self.domain
    #                                         )


    # def update_record_by_id(self, session_id: str, transcript ):
    #     try:
    #         sf = self.init_client()
    #         data = {
    #             'Processed__c' : True,
    #             'Transcript_corpus__c': transcript

    #         }
    #         resp = sf.Session__c.update(session_id, data)
    #         print(resp)
    #         return f'SAVED TRANSCRIPT FOR SESSION {session_id} IN SALESFORCE'

    #     except simple_salesforce.exceptions.SalesforceMalformedRequest as err:
    #         print(err)
    #         print('CANNOT SAVE THIS RECORD ' + session_id)
    #         return 'CANNOT SAVE THIS RECORD ' + session_id
    #     except Exception as e:
    #         print('ERRROR')
    #         print(e)


    # def upsert_record_by_external_id(self ,session_id, record, app):
    #     try:
    #         app.logger.info('TRY TO SEND TO SF')
    #         app.logger.info(record)

    #         sf = self.init_client()
    #         external_id = simple_salesforce.format_external_id('Session_External_Id__c', session_id)
    #         app.logger.info(external_id)
    #         resp = sf.Session__c.upsert(external_id, record)
    #         app.logger.info(resp)
    #         app.logger.info('SAVED RECORD IN SALESFORCE')
    #         return 'SAVED RECORD IN SALESFORCE'
    #     except simple_salesforce.exceptions.SalesforceMalformedRequest as err:
    #         app.logger.info(err)
    #         app.logger.info('CANNOT SAVE THIS RECORD ' + session_id)
    #         return 'CANNOT SAVE THIS RECORD ' + session_id
    #     except Exception as e:
    #         app.logger.info('ERRROR')
    #         app.logger.info(e)


    # def get_session_ids(self):
    #     sf = self.init_client()

    #     res = sf.query_all("SELECT Session_External_Id__c, Transcript_corpus__c FROM Session__c  WHERE Session_External_Id__c != NULL AND  Cannot_Be_Processed__c = false")
    #     session_ids = []

    #     for record in res['records']:
    #         if record['Session_External_Id__c'] is not None and record['Transcript_corpus__c'] is None:
    #             session_ids.append(record['Session_External_Id__c'])

    #     return session_ids


    # def get_session_ids_to_process(self, number_days  = 21, numbar_of_records = 100):
    #     sf = self.init_client()
    #     res = sf.query_all(''.join([f"SELECT ID, Transcript_corpus__c, Latest_Media_URL__c, Processed__c, CreatedDate   FROM Session__c",
    #                        f" WHERE  CreatedDate = LAST_N_DAYS:{number_days} ",
    #                                 f" AND Processed__c = false order by CreatedDate desc limit {numbar_of_records} "]))
    #     session = []
    #     for record in res['records']:
    #          session.append(record['Id'])
    #     return session


    # def get_urls_to_process(self, numbar_of_records = 100) -> dict:
    #     sf = self.init_client()

    #     res = sf.query_all(''.join([f"SELECT ID, Transcript_corpus__c, Latest_Media_URL__c, Processed__c, CreatedDate   FROM Session__c ",
    #                       f" WHERE Latest_Media_URL__c != NULL AND  Processed__c = false limit {numbar_of_records}"]))
    #     session_dict = {}
    #     for record in res['records']:
    #         data = {
    #             "Transcript_corpus__c" : record['Transcript_corpus__c'],
    #             "Latest_Media_URL__c" : record['Latest_Media_URL__c'],
    #             "Processed__c" : record['Processed__c'],
    #             "ID" : record['Id'],
    #         }

    #         session_dict[record['Id']] = data
    #     return session_dict


import simple_salesforce
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class SalesForce:

    def __init__(self) -> None:
        self.consumer_key = os.getenv('CONSUMER_KEY')
        self.consumer_secret = os.getenv('CONSUMER_SECRET')
        self.salesforce_username = os.getenv('SALESFORCE_USERNAME')
        self.salesforce_password = os.getenv('SALESFORCE_PASSWORD')
        self.security_token = os.getenv('SALESFORCE_SECURITY_TOKEN')
        self.org_id = os.getenv('ORG_ID')
        
        self.sf = self.init_client()
        self.headers = self.sf.headers
        self.instance = self.sf.sf_instance
        
    def init_client(self):
        try:
            sf = simple_salesforce.Salesforce(
                username = self.salesforce_username,
                password = self.salesforce_password,
                consumer_key = self.consumer_key,
                consumer_secret = self.consumer_secret,
                organizationId = self.org_id,
                security_token = self.security_token
                )
            print(f'[{datetime.now()}]: Salesforce client initialized successfully.')
            return sf
        
        except Exception as e:
            print(f'[{datetime.now()}]: Failed to initialize Salesforce client: {e}')
            return None
    
    def update_conference_record(self, conference_id, transcript):
        try:
            result = self.sf.Conference__c.update(conference_id, {'Transcript__c': transcript})
            print(f'[{datetime.now()}]: Conference record updated successfully: {result}')
            return result
        
        except Exception as e:
            print(f'[{datetime.now()}]: Failed to update Conference record: {e}')

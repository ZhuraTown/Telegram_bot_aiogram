from __future__ import print_function
import os
import json

import httplib2
from apiclient import discovery
from httplib2 import Http
from google.oauth2 import service_account
import time


class GoogleFormApi():

    def __init__(self):
        self.SCOPES = [
            "https://www.googleapis.com/auth/forms.body.readonly",
            "https://www.googleapis.com/auth/forms.responses.readonly",
            "https://www.googleapis.com/auth/drive",
            'https://www.googleapis.com/auth/drive.file',
        ]
        self.DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.SERVICE_ACCOUNT_FILE = os.path.join(self.BASE_DIR, 'creadentals.json')
        self.creeds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE,
                                                                            scopes=self.SCOPES)
        self.form_id = '1ywHgetyx4nz-AEJ-OltuoJBOav91j_WwLTwRwdRTw8A'

    def update_form_id(self, link_form):
        """
        Метод получает ссылку на форму, и достаёт из неё form_id. Затем сохраняет его в БД
        :param link_form:
        :return:
        """
        pass

    def service_form(self):
        return discovery.build('forms', 'v1', credentials=self.creeds)

    def get_responses_form_user(self):
        return self.service_form().forms().responses().list(formId=self.form_id).execute()

# ID SHEET 1kkqrJd_epesBO3rc0pViE3vwL8OwJhV7SI2McC0pyNY

google_form = GoogleFormApi()
for line in google_form.get_responses_form_user().get('responses'):
    print(line)

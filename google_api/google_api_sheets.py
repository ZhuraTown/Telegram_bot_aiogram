from __future__ import print_function

import datetime
import os
import json

import httplib2
from googleapiclient.discovery import build
from httplib2 import Http
from google.oauth2 import service_account
import time


class GoogleSheetsApi():

    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        # self.DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.SERVICE_ACCOUNT_FILE = os.path.join(self.BASE_DIR, 'creadentals.json')
        self.creeds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE,
                                                                            scopes=self.SCOPES)
        self.sheet_id = '1s8KI9UCWWMikIPI99icuKSh0HS7vCxo3OMuE06rbSo0'

    def service(self):
        return build('sheets', 'v4', credentials=self.creeds)

    def get_all_responses_sheet_user(self):
        return self.service().spreadsheets().values().get(spreadsheetId=self.sheet_id,
                                                          range='Табель времени').execute()

    def get_links_to_edit_form(self):
        for line in self.get_all_responses_sheet_user().get('values'):
            print(f"{line[3][0:12]:<2} {line[4]} {line[5]} "
                  f"{line[6]}"
                  f"{'Охрана'if line[7] else ''}"
                  f"{'Дежурный'if line[9] else ''}"
                  f"{'Рабочий'if line[11] else ''}"
                  f"{'ИТР'if line[13] else ''}"
                  )

google_form = GoogleSheetsApi()
for line in google_form.get_all_responses_sheet_user().get('values'):
    print(line[0], ' ', line)
    # if len(line[0].split('.')) == 3:
    #     a = datetime.datetime.strptime(line[0], "%d.%m.%Y %H:%M:%S")
    #     print(a.day, a.month)

google_form.get_links_to_edit_form()

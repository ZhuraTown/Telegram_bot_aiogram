from __future__ import print_function
import os
import json

import httplib2
from apiclient import discovery
from httplib2 import Http
from google.oauth2 import service_account



SCOPES = ["https://www.googleapis.com/auth/forms.body.readonly",
          "https://www.googleapis.com/auth/forms.responses.readonly",
          ]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'creadentals.json')

credentails = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = discovery.build('forms', 'v1', credentials=credentails)

# Prints the title of the sample form:
form_id = '1ywHgetyx4nz-AEJ-OltuoJBOav91j_WwLTwRwdRTw8A'
result = service.forms().responses().list(formId=form_id).execute()
# 1FAIpQLSfj3nGZjk6T5sFKn7Cc1lMCLy7dlPOs4kEOe5EVVSaLClL08g
# 2_ABaOnudJxdTv8ADFk-a7CQETUw1E7vDMqvdCvl33W_bJ9Mls6pnoOszRL7B-gru0ce5i33E
print(result)
print(len(result.get('responses')))
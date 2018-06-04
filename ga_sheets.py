# [START sheets_quickstart]
"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import gspread

import json
from oauth2client.service_account import ServiceAccountCredentials

from RealTimeHelloAnalytics import *



# use creds to create a client to interact with the Google Drive API
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('YOUR_GOOGLE_SHEETS_CREDENTIALS.json', scope) #the file you downloaded after enabling a service account from the google api console
client = gspread.authorize(creds)
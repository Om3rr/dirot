from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import List


class SheetsAPI():
    # If modifying these scopes, delete the file gmail.token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1YEPJCM-u2dab5ewhTCMgR31oivsDa8lY4Oaajzilpwk'

    SENT_RANGE="Sheet1!J{row}:J{row}"
    ROW_RANGE="Sheet1!A{row}:I{row}"

    @staticmethod
    def get_service():
        creds = None
        # The file gmail.token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('sheets.token.pickle'):
            with open('sheets.token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SheetsAPI.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('sheets.token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        return service.spreadsheets()

    def __init__(self):
        self.__service = SheetsAPI.get_service()

    def append(self, body: List):
        value_range_body = {
            "values": [body]
        }
        valueInputOption = "RAW"
        return self.__service.values().append(spreadsheetId=SheetsAPI.SPREADSHEET_ID, valueInputOption=valueInputOption,
                                range=SheetsAPI.ROW_RANGE.format(row=1), body=value_range_body).execute()

    def get(self, row):
        return self.__service.values().get(spreadsheetId=SheetsAPI.SPREADSHEET_ID, range=SheetsAPI.ROW_RANGE.format(row=row)).execute().get("values")

    def get_all_ids(self):
        return self.__service.values().get(spreadsheetId=SheetsAPI.SPREADSHEET_ID,
                                           range="Sheet1!A2:A100000").execute().get("values")[0]

    def is_sent(self, row):
        resp = self.__service.values().get(spreadsheetId=SheetsAPI.SPREADSHEET_ID, range=SheetsAPI.SENT_RANGE.format(row=row)).execute()
        values = resp.get("values") or [[0]]
        return str(values[0][0]) == '1'

    def set_sent(self, row):
        value_range_body = {
            "values": [[1]]
        }
        valueInputOption = "RAW"
        return self.__service.values().update(spreadsheetId=SheetsAPI.SPREADSHEET_ID, valueInputOption=valueInputOption,
                                              range=SheetsAPI.SENT_RANGE.format(row=row), body=value_range_body).execute()




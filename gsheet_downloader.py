import os
import sys
import string

import numpy as np
import pandas as pd

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def find_date_file(last_date_ws: str, file_list: list):
    date_file_list = list(map(lambda x: x.split('_')[0].replace('-', ''), file_list))
    date_index = date_file_list.index(last_date_ws)
    need_2b_open = file_list[date_index + 1:]
    return need_2b_open


class SpreadSheetsDownloader:
    def __init__(self, spreadsheet_id, key_path=None):
        if not key_path:
            key_path = os.getcwd()

        self.doc = None
        self.worksheet = None
        self.sheet_name = None
        self.worksheet_df = None
        self.spreadsheet_id = spreadsheet_id
        self.google_key = os.path.join(key_path, "caramel-biplane-329615-39421c5e66b4.json")
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.google_key, self.scope)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def _open_sheet(self):
        sheet_response = self.sheet.values()
        self.sheet_values = sheet_response.batchGet(
            spreadsheetId=self.spreadsheet_id,
            ranges=f'{self.sheet_name}!A1:X'
        ).execute().get('valueRanges')[0]
        self.last_values = np.array(self.sheet_values.get('values')) if self.sheet_values.get('values') else None

    def get_sheet_values(self, sheet_name):
        sheet_response = self.sheet.values()
        result_values = sheet_response.batchGet(
            spreadsheetId=self.spreadsheet_id,
            ranges=f'{sheet_name}!A1:X'
        ).execute().get('valueRanges')[0]
        return result_values

    def set_cell_index(self, sheet_name: str, metric_length: int, dimension_length: int):
        self.sheet_name = sheet_name
        self._open_sheet()
        column_length = metric_length + dimension_length

        value_idx = self.last_values.shape[0] if self.last_values is not None else 0
        new_values_idx_first = value_idx + 1

        self.new_data_range = f"{self.sheet_name}!A{new_values_idx_first}:{string.ascii_uppercase[column_length]}"
        return new_values_idx_first

    def update_sheet(self, new_data: list):
        response = \
            self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=self.new_data_range,
                valueInputOption="USER_ENTERED",
                body={'values': new_data}
            ).execute()

        print(response)

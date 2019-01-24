#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import time

import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials

GDOCS_OAUTH_JSON = 'TIEA345-Demo3-jumapolv-b27927e3d929.json'
GDOCS_SPREADSHEET_NAME = 'TIEA345 Demo3'

DHT_TYPE = Adafruit_DHT.DHT11
DHT_PIN = 26

FREQUENCY_SECONDS = 30

humidity, temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)


def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)


print('Logging sensor measurements to {0} every {1} seconds.'.format(
    GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')

worksheet = None
while True:
    # Login if necessary.
    if worksheet is None:
        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

    if humidity is None or temp is None:
        time.sleep(2)
        continue

    print('Temperature: {0:0.1f} C'.format(temp))
    print('Humidity:    {0:0.1f} %'.format(humidity))

    # Append the data in the spreadsheet, including a timestamp
    timeStamp = unicode(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(timeStamp)
    worksheet.append_row((timeStamp, temp, humidity))

    # Wait 30 seconds before continuing
    print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
    time.sleep(FREQUENCY_SECONDS)

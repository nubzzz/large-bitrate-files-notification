#!/usr/bin/env python3

import pandas as pd
import http.client, urllib
from os import environ

api_key = environ['PUSHOVER_API_KEY']
user_key = environ['PUSHOVER_USER_KEY']
if environ.get('UPPER_BOUND_BITRATE') is not None:
    high_bitrate = int(environ['UPPER_BOUND_BITRATE'])
else:
    high_bitrate = 8388608

def main():
    large_files = pd.read_csv('/tmp/episodes-raw.csv', names=['file_path','bitrate']).sort_values(by=['bitrate'],ascending = False)
    large_files = large_files.loc[large_files['bitrate'] > high_bitrate]

    if large_files['file_path'].count() > 0:
        print("Large files detected")
        print("Alerting")
        title = "ALERT: Large Bitrate Files Detected"
        message = "The following files have a high bitrate.\nPlease investigate\n" 
        message += '\n'.join(large_files['file_path'].to_list())
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
              "token": api_key,
              "user": user_key,
              "message": message,
              "title": title
              }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    else:
        print("No large files detected")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import os
import pandas as pd
import http.client, urllib

api_key = os.environ['PUSHOVER_API_KEY']
user_key = os.environ['PUSHOVER_USER_KEY']

large_files = pd.read_csv('/tmp/episodes-raw.csv', names=['file_path','bitrate']).sort_values(by=['bitrate'],ascending = False)
large_files = large_files.loc[large_files['bitrate'] > 8388608]

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

#!/usr/bin/env python3
"""Takes a csv input at /tmp/episodes-raw.csv, sorts by bitrate, compares against a
high bitrate env variable or defaults to 8Mb/s and sends a pushover notification
via the api"""

import http.client
import urllib
from os import environ
import pandas as pd

API_KEY = environ['PUSHOVER_API_KEY']
USER_KEY = environ['PUSHOVER_USER_KEY']
if environ.get('UPPER_BOUND_BITRATE') is not None:
    HIGH_BITRATE = int(environ['UPPER_BOUND_BITRATE'])
else:
    HIGH_BITRATE = 8388608

def main():
    """Main function"""
    raw_files = pd.read_csv('/tmp/episodes-raw.csv', names=['file_path','bitrate'])
    large_files = raw_files.sort_values(by=['bitrate'],ascending = False)
    large_files = large_files.loc[large_files['bitrate'] > HIGH_BITRATE]

    if large_files['file_path'].count() > 0:
        print("Large files detected")
        print("Alerting")
        title = "ALERT: Large Bitrate Files Detected"
        message = "The following files have a high bitrate.\nPlease investigate\n"
        message += '\n'.join(large_files['file_path'].to_list())
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
              "token": API_KEY,
              "user": USER_KEY,
              "message": message,
              "title": title
              }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    else:
        print("No large files detected")

if __name__ == '__main__':
    main()

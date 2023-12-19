# Large Bitrate Files Notification
Uses minio to get the file list
Runs that file list through mediainfo and builds a csv
Then uses pandas within python to process the data and send a notification via Pushover

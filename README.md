# Large Bitrate Files Notification
Uses minio to get the file list

Runs that file list through mediainfo and builds a csv

Then uses pandas within python to process the data and send a notification via Pushover

## Needed environment variables

`PUSHOVER_API_KEY` Pushover application key

`PUSHOVER_USER_KEY` Pushover user key

`S3_HOST` S3/Minio full url (e.g. http://s3.nubzzz.com:9000)

`S3_BUCKET` S3/Minio bucket that holds the media files

`AWS_KEY` S3/Minio access key

`AWS_SECRET_KEY` S3/Minio secret key

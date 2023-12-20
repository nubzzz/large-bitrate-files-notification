# Large Bitrate Files Notification

A simple docker container to alert the user of large bitrate files in object storage

## Basic logic flow

Uses minio to get the file list

Runs that file list through mediainfo and builds a csv

Then uses pandas within python to process that data and send a notification via Pushover

## Needed environment variables

`PUSHOVER_API_KEY`: Pushover application key

`PUSHOVER_USER_KEY`: Pushover user key

`S3_HOST`: S3/Minio full url (e.g. http://s3.nubzzz.com:9000)

`S3_BUCKET`: S3/Minio bucket that holds the media files

`AWS_KEY`: S3/Minio access key

`AWS_SECRET_KEY`: S3/Minio secret key

`EMAIL`: Alert by email [true|false]

## Optional environment variables

`UPPER_BOUND_BITRATE`: The upper bound for acceptable bitrate in bytes/s (e.g 8388608 for 8Mb/s)

`VERBOSE`: Enable verbose logging [true|false]

`GMAIL`: If you choose to turn on EMAIL above use gmail to send the message (currently the only thing that works) [true|false]

`GMAIL_APP_PASSWORD`: App Password for access to gmail (https://myaccount.google.com/apppasswords)

`EMAIL_RECIPIENT`: Where you want your email to go

`EMAIL_SENDER`: The From address for the email

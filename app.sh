#!/bin/bash
set -e

/usr/local/bin/mc alias set s3 "$S3_HOST" "$AWS_KEY" "$AWS_SECRET_KEY"

echo "Getting media file list from minio"
media_files=$(/usr/local/bin/mc ls s3/${S3_BUCKET} | awk '{print $6}')
echo "Finished getting media file list"

echo "Generating csv"
for file in $media_files;do
    if $VERBOSE;then
        echo "Getting bitrate from ${file}"
    fi
    bitrate="$(mediainfo --Output='Video;%BitRate%' ${S3_HOST}/${S3_BUCKET}/${file})"
    echo "${file},${bitrate}" >> /tmp/episodes-raw.csv
done
echo "CSV created"
echo "Running python code"
/usr/bin/python3 app.py

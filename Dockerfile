FROM alpine:3.19

RUN apk --update --no-cache add python3 py3-pip py3-pandas py3-pymediainfo mediainfo libmediainfo bash curl perl

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/
COPY app.sh /app/

RUN pip3 install -r requirements.txt --break-system-packages

RUN curl https://dl.min.io/client/mc/release/linux-amd64/mc \
    --create-dirs \
    -o /usr/local/bin/mc; \
    chmod +x /usr/local/bin/mc

ENTRYPOINT ["/bin/bash","/app/app.sh"]

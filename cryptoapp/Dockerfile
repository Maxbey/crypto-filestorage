FROM alpine:latest
RUN apk add --update python py-pip bash
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/main py-psycopg2


RUN apk update && apk add --update libffi-dev freetype-dev libxslt-dev libxml2-dev \
    pcre-dev zlib-dev gcc python-dev \
    g++ build-base linux-headers

COPY ./requirements /usr/requirements/
COPY . /usr/src/app

WORKDIR /usr/requirements/

RUN pip install -r base.txt

RUN adduser -D myuser
WORKDIR /usr/src/app

RUN chown -R myuser.myuser .

USER myuser

CMD bash bin/run.sh

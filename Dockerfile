#FROM python:3.11-alpine
FROM nginx:alpine

WORKDIR /APP

RUN apk update
RUN apk add python3
RUN apk add py3-pip
RUN apk add py3-virtualenv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin/:$PATH"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
COPY ./.config/nginx/recipe_viewer.conf /etc/nginx/conf.d/default.conf

CMD ["/bin/sh", "/APP/entrypoint.sh"]
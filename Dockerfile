# pull official base image
FROM python:3.8.10-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev 
    # && apk add postgresql-dev 
    # && pip install psycopg2

# install dependencies
COPY ./requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput


# add and run as non-root user
USER root



# run gunicorn
CMD gunicorn proj.wsgi:application --bind 0.0.0.0:8080 

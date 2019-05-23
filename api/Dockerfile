FROM python:3.6-alpine
RUN apk update && apk add build-base unixodbc-dev freetds-dev
ADD odbcinst.ini /etc/odbcinst.ini
WORKDIR /app
COPY app .
RUN pip install -U pip && pip install -r requirements.txt
ENTRYPOINT [ "python", "app.py" ]
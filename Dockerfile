FROM python:3.10.5

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

ENV FLASK_APP=main.py

EXPOSE 5000

CMD [ "flask","run","--host=0.0.0.0"]
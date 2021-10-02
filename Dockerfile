FROM python:3.9.5-slim-buster

RUN apt-get update && apt-get install -y libpq-dev

RUN adduser --disabled-password --gecos "" alertbot

USER alertbot
COPY --chown=alertbot Pipfile Pipfile.lock /home/alertbot/app/
WORKDIR /home/alertbot/app

RUN python3 -m pip install --upgrade pip pipenv 
RUN python3 -m pipenv install --deploy --system --ignore-pipfile

COPY --chown=alertbot . /home/alertbot/app/

ENTRYPOINT ["python3","alert_bot.py"]

FROM python:3.9.5-slim-buster

COPY . /app/

WORKDIR app
RUN python -m pip install pipenv
RUN python -m pipenv install

ENTRYPOINT ["pipenv","run","python","alert_bot.py"]

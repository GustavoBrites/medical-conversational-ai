FROM python:3.12-slim

WORKDIR /app

RUN pip install pipenv

COPY data/qa_data.csv data/qa_data.csv
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --ignore-pipfile --system

COPY med-conv-ai .

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 app:app
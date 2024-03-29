FROM python:slim-bullseye

WORKDIR /app

COPY ./app /app

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py"]

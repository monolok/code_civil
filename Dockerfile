FROM python:slim-bullseye

WORKDIR /app

COPY ./app /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD streamlit run --server.port $PORT app.py

#CMD ["streamlit", "run", "app.py"]
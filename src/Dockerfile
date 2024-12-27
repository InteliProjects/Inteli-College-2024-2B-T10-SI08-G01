FROM python:3.12-slim

WORKDIR /src/s3_to_clickhouse_etl

RUN pip install poetry
COPY . .
RUN pip install --upgrade poetry
RUN poetry add flask

EXPOSE 5000
ENV FLASK_APP=src/s3_to_clickhouse_etl/app.py
CMD ["poetry", "run", "python"]


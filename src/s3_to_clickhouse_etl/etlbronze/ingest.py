import json
import datetime
import pyarrow.parquet as pq
import io
import os
from datetime import datetime, timezone
from prefect import task, flow
from config.connections import Connections
from config.settings import DataFalhas, DataOcorrencias
from config.observability import ObservabilityLogger
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class DataIngestionService:
    """
    Serviço para ingerir dados de arquivos Parquet do S3 para o ClickHouse.
    """

    def get_s3_client(self):
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
        aws_session_token = os.getenv('AWS_SESSION_TOKEN') 

        if not aws_access_key_id or not aws_secret_access_key:
            raise NoCredentialsError()

        return boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )

    @task
    def get_parquet_files(self, bucket_name, prefix="ocorrencias-e-falhas/"):
        """
        Lista os arquivos Parquet no bucket S3 dentro do prefixo especificado.
        """
        s3 = self.get_s3_client()
        try:
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            return [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.parquet')]
        except ClientError as e:
            if e.response['Error']['Code'] == 'ExpiredToken':
                print("Token expired. Refreshing credentials...")
                s3 = self.get_s3_client() 
                response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
                return [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.parquet')]
            else:
                raise e

    @task
    def read_parquet_and_insert_to_clickhouse(self, bucket_name, file_key):
        """
        Lê um arquivo Parquet do S3, valida os dados com Pydantic e insere no ClickHouse.
        """
        start_time = datetime.now(timezone.utc)
        s3 = Connections.get_s3_client()
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        parquet_data = pq.read_table(io.BytesIO(obj['Body'].read()))

        client = Connections.get_clickhouse_client()

        file_name = os.path.basename(file_key)
        schema = None
        if file_name == "tabela_big_data_ft_ocorrencias.parquet":
            schema = DataOcorrencias
        elif file_name == "tabela_big_data_ft_falhas.parquet":
            schema = DataFalhas
        else:
            print(f"File name {file_name} não reconhecido para processamento.")
            return

        client.execute('''
            CREATE TABLE IF NOT EXISTS grupo1.data_ingestion (
                data_ingestao DateTime,
                data_linha String,
                data_tag String
            ) ENGINE = MergeTree()
            ORDER BY data_ingestao
        ''')

        rows = []
        for batch in parquet_data.to_batches():
            for row in batch.to_pylist():
                try:
                    row_with_spaces = {key.replace(" ", "_"): value for key, value in row.items()}
                    validated_row = schema(**row_with_spaces)

                    data_linha = json.dumps(validated_row.dict())
                    data_ingestao = datetime.now(timezone.utc)
                    data_tag = file_key
                    rows.append((data_ingestao, data_linha, data_tag))
                except Exception as e:
                    print(f"Erro de validação na linha {row}: {e}")

        if rows:
            client.execute(
                "INSERT INTO grupo1.data_ingestion (data_ingestao, data_linha, data_tag) VALUES",
                rows
            )

        end_time = datetime.now(timezone.utc)
        details = f"Processed {len(rows)} valid records from {file_key} in bucket {bucket_name} and inserted into ClickHouse"
        ObservabilityLogger.log_observability("read_parquet_and_insert_to_clickhouse", start_time, end_time, details)

    @flow(log_prints=True)
    def run_ingest_data(self):
        """
        Método público para ingerir dados de arquivos Parquet do S3 para o ClickHouse.
        """
        start_time = datetime.now(timezone.utc)
        bucket_name = 'cptm-xpress'

        parquet_files = self.get_parquet_files(bucket_name)

        for file_key in parquet_files:
            self.read_parquet_and_insert_to_clickhouse(bucket_name, file_key)

        end_time = datetime.now(timezone.utc)
        details = f"Ingested data from all Parquet files in bucket {bucket_name}"
        ObservabilityLogger.log_observability("ingest_data", start_time, end_time, details)


if __name__ == "__main__":
    service = DataIngestionService()
    service.run_ingest_data()

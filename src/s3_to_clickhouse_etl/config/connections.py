import boto3
from clickhouse_driver import Client
import psycopg2
from config.settings import settings


class Connections:
    """
    Classe para gerenciar conexões com S3, ClickHouse e PostgreSQL.
    """

    @staticmethod
    def get_s3_client():
        """
        Retorna um cliente S3 configurado com as credenciais do AWS.
        """
        return boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_REGION
        )

    @staticmethod
    def get_clickhouse_client():
        """
        Retorna um cliente ClickHouse configurado com as credenciais.
        """
        return Client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            user=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD
        )

    @staticmethod
    def get_postgres_connection():
        """
        Retorna uma conexão com o PostgreSQL configurada com as credenciais.
        """
        return psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD
        )

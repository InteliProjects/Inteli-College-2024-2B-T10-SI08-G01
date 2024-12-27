import os
from clickhouse_driver import Client
from dotenv import load_dotenv

load_dotenv()


class ClickHouseClient:
    """
    Representa um cliente para conexão e execução de consultas no banco ClickHouse.

    Métodos:
        execute_query: Executa uma consulta SQL no ClickHouse.
    """

    def __init__(self):
        self.client = Client(
            host=os.getenv("CLICKHOUSE_HOST"),
            port=int(os.getenv("CLICKHOUSE_PORT")),
            user=os.getenv("CLICKHOUSE_USER"),
            password=os.getenv("CLICKHOUSE_PASSWORD")
        )

    def execute_query(self, sql: str):
        """
        Executa uma consulta SQL no ClickHouse.

        Args:
            sql (str): Comando SQL a ser executado.
        """
        self.client.execute(sql)
        print(f"Executado com sucesso: {sql}")


load_dotenv()


class ClickHouseClient:
    """
    Representa um cliente para conexão e execução de consultas no banco ClickHouse.

    Métodos:
        execute_query: Executa uma consulta SQL no ClickHouse.
    """

    def __init__(self):
        self.client = Client(
            host=os.getenv("CLICKHOUSE_HOST"),
            port=int(os.getenv("CLICKHOUSE_PORT")),
            user=os.getenv("CLICKHOUSE_USER"),
            password=os.getenv("CLICKHOUSE_PASSWORD")
        )

    def execute_query(self, sql: str):
        """
        Executa uma consulta SQL no ClickHouse.

        Args:
            sql (str): Comando SQL a ser executado.
        """
        self.client.execute(sql)
        print(f"Executado com sucesso: {sql}")


load_dotenv()


class ClickHouseClient:
    """
    Representa um cliente para conexão e execução de consultas no banco ClickHouse.

    Métodos:
        execute_query: Executa uma consulta SQL no ClickHouse.
    """

    def __init__(self):
        self.client = Client(
            host=os.getenv("CLICKHOUSE_HOST"),
            port=int(os.getenv("CLICKHOUSE_PORT")),
            user=os.getenv("CLICKHOUSE_USER"),
            password=os.getenv("CLICKHOUSE_PASSWORD")
        )

    def execute_query(self, sql: str):
        """
        Executa uma consulta SQL no ClickHouse.

        Args:
            sql (str): Comando SQL a ser executado.
        """
        self.client.execute(sql)
        print(f"Executado com sucesso: {sql}")

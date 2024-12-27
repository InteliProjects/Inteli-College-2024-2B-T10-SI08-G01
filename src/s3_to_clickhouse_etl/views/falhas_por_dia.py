from prefect import task, flow
from config.clickhouse_client import ClickHouseClient

class FalhasPorDia:
    """
    Serviço para realizar operações no ClickHouse relacionadas a falhas por dia.
    """

    def __init__(self):
        """
        Inicializa o serviço com um cliente ClickHouse.
        """
        self.client = ClickHouseClient()

    def execute_query(self, query: str) -> None:
        """
        Executa uma query no ClickHouse.

        :param query: A string da query a ser executada.
        """
        self.client.execute_query(query)

    @task
    def _create_intermediate_table(self) -> str:
        """
        (Privado) Cria uma tabela intermediária para armazenar falhas por dia no ClickHouse.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS grupo1.intermediate_falhas_dia (
            data_falha Date,
            total_falhas Int32
        )
        ENGINE = MergeTree()
        ORDER BY data_falha;
        """
        self.execute_query(create_table_sql)
        return "Tabela intermediária criada com sucesso!"

    @task
    def _insert_intermediate_data(self) -> str:
        """
        (Privado) Insere dados na tabela intermediária falhas por dia.
        """
        insert_sql = """
        INSERT INTO grupo1.intermediate_falhas_dia (data_falha, total_falhas)
        SELECT
            toDateOrNull(JSONExtractString(data_linha, 'ID_DT_FALHA')) AS data_falha,
            COUNT(*) AS total_falhas
        FROM
            grupo1.data_ingestion
        WHERE
            JSONExtractString(data_linha, 'ID_DT_FALHA') IS NOT NULL
            AND toDateOrNull(JSONExtractString(data_linha, 'ID_DT_FALHA')) IS NOT NULL
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_falhas.parquet'
        GROUP BY
            data_falha
        ORDER BY
            data_falha;
        """
        self.execute_query(insert_sql)
        return "Dados inseridos na tabela intermediária com sucesso!"

    @task
    def _create_view(self) -> str:
        """
        (Privado) Cria a view falhas_por_dia consolidada no ClickHouse.
        """
        create_view_sql = """
        CREATE OR REPLACE VIEW grupo1.falhas_por_dia AS
        SELECT
            data_falha,
            total_falhas
        FROM
            grupo1.intermediate_falhas_dia
        ORDER BY
            data_falha;
        """
        self.execute_query(create_view_sql)
        return "View falhas_por_dia criada com sucesso!"

    @flow(log_prints=True)
    def run_falhas_por_dia(self):
        """
        Método público para executar o ETL completo no ClickHouse.
        """
        table_status = self._create_intermediate_table()
        print(table_status)
        insert_status = self._insert_intermediate_data()
        print(insert_status)

        view_status = self._create_view()
        print(view_status)

if __name__ == "__main__":
    service = FalhasPorDia()
    service.run_falhas_por_dia()

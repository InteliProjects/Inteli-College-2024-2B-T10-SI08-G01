from prefect import task, flow
from config.clickhouse_client import ClickHouseClient

class OcorrenciasPorDia:
    """
    Serviço para realizar operações no ClickHouse relacionadas a ocorrências por dia.
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
        (Privado) Cria uma tabela intermediária para armazenar ocorrências por dia no ClickHouse.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS grupo1.intermediate_ocorrencias_dia (
            data_ocorrencia Date,
            total_ocorrencias Int32
        )
        ENGINE = MergeTree()
        ORDER BY data_ocorrencia;
        """
        self.execute_query(create_table_sql)
        return "Tabela intermediária criada com sucesso!"

    @task
    def _insert_intermediate_data(self) -> str:
        """
        (Privado) Insere dados na tabela intermediária ocorrências por dia.
        """
        insert_sql = """
        INSERT INTO grupo1.intermediate_ocorrencias_dia (data_ocorrencia, total_ocorrencias)
        SELECT
            toDate(toString(Id_Dataocorrencia)) AS data_ocorrencia,
            COUNT(*) AS total_ocorrencias
        FROM
            grupo1.data_ingestion
        WHERE
            data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_ocorrencias.parquet'
        GROUP BY
            data_ocorrencia
        ORDER BY
            data_ocorrencia;
        """
        self.execute_query(insert_sql)
        return "Dados inseridos na tabela intermediária com sucesso!"


    @task
    def _create_view(self) -> str:
        """
        (Privado) Cria a view ocorrências_por_dia consolidada no ClickHouse.
        """
        create_view_sql = """
        CREATE OR REPLACE VIEW grupo1.ocorrencias_por_dia AS
        SELECT
            data_ocorrencia,
            total_ocorrencias
        FROM
            grupo1.intermediate_ocorrencias_dia
        ORDER BY
            data_ocorrencia;
        """
        self.execute_query(create_view_sql)
        return "View ocorrências_por_dia criada com sucesso!"

    @flow(log_prints=True)
    def run_ocorrencias_por_dia(self):
        """
        Método público para executar o ETL completo no ClickHouse.
        """
        table_status = self._create_intermediate_table()
        print(table_status)
        insert_status = self._insert_intermediate_data()
        print(insert_status)

        view_status = self._create_view()
        print(view_status)

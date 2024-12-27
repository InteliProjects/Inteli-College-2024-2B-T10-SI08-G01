from prefect import task, flow
from config.clickhouse_client import ClickHouseClient


class FalhasPorSituacao:
    """
    Serviço para realizar operações no ClickHouse relacionadas a falhas por situação.
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
    def _create_table(self) -> str:
        """
        (Privado) Cria a tabela intermediate_falhas_por_situacao no ClickHouse, se não existir.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS grupo1.intermediate_falhas_por_situacao (
            Situacao String,
            DataFalha Date,
            total_falhas UInt64
        )
        ENGINE = MergeTree()
        ORDER BY (Situacao, DataFalha);
        """
        self.execute_query(create_table_sql)
        return "Tabela intermediate_falhas_por_situacao criada ou já existente."

    @task
    def _insert_data(self) -> str:
        """
        (Privado) Insere dados na tabela intermediate_falhas_por_situacao.
        """
        insert_data_sql = """
        INSERT INTO grupo1.intermediate_falhas_por_situacao (Situacao, DataFalha, total_falhas)
        SELECT 
            JSONExtractString(data_linha, 'SITUACAO_FALHA') AS Situacao,
            toDateOrNull(JSONExtractString(data_linha, 'ID_DT_FALHA')) AS DataFalha,
            COUNT(*) AS total_falhas
        FROM grupo1.data_ingestion
        WHERE 
            JSONExtractString(data_linha, 'SITUACAO_FALHA') IS NOT NULL
            AND JSONExtractString(data_linha, 'ID_DT_FALHA') IS NOT NULL
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_falhas.parquet'
        GROUP BY 
            Situacao,
            DataFalha
        ORDER BY 
            total_falhas DESC;
        """
        self.execute_query(insert_data_sql)
        return "Dados inseridos na tabela intermediate_falhas_por_situacao com sucesso."

    @task
    def _create_view(self) -> str:
        """
        (Privado) Cria a view falhas_por_situacao consolidada no ClickHouse.
        """
        create_view_sql = """
        CREATE OR REPLACE VIEW grupo1.falhas_por_situacao AS
        SELECT 
            Situacao,
            DataFalha,
            total_falhas
        FROM grupo1.intermediate_falhas_por_situacao
        ORDER BY total_falhas DESC;
        """
        self.execute_query(create_view_sql)
        return "View falhas_por_situacao criada ou atualizada com sucesso."

    @flow(log_prints=True)
    def run_falhas_por_situacao(self):
        """
        Método público para executar o ETL completo no ClickHouse.
        """
        table_status = self._create_table()
        print(table_status)

        insert_status = self._insert_data()
        print(insert_status)

        view_status = self._create_view()
        print(view_status)


if __name__ == "__main__":
    service = FalhasPorSituacao()
    service.run_falhas_por_situacao()

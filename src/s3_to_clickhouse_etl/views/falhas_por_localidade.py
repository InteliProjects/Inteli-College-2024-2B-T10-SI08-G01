from prefect import task, flow
from config.clickhouse_client import ClickHouseClient


class FalhasPorLocalidade:
    """
    Serviço para realizar operações no ClickHouse relacionadas a falhas por localidade.
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
        (Privado) Cria a tabela intermediate_falhas_por_localidade no ClickHouse, se não existir.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS grupo1.intermediate_falhas_por_localidade (
            Localidade String,
            DataFalha Date,
            total_falhas Int32
        )
        ENGINE = MergeTree()
        ORDER BY (Localidade, DataFalha);
        """
        self.execute_query(create_table_query)
        return "Tabela intermediate_falhas_por_localidade criada (ou já existente)."

    @task
    def _insert_data(self) -> str:
        """
        (Privado) Insere dados na tabela intermediate_falhas_por_localidade, agrupando por localidade e data.
        """
        insert_data_query = """
        INSERT INTO grupo1.intermediate_falhas_por_localidade (Localidade, DataFalha, total_falhas)
        SELECT 
            JSONExtractString(data_linha, 'LOCALIDADE') AS Localidade,
            toDateOrNull(JSONExtractString(data_linha, 'ID_DT_FALHA')) AS DataFalha,
            COUNT(JSONExtractString(data_linha, 'ID_FT_FALHA')) AS total_falhas
        FROM grupo1.data_ingestion
        WHERE 
            JSONExtractString(data_linha, 'LOCALIDADE') IS NOT NULL
            AND JSONExtractString(data_linha, 'ID_DT_FALHA') IS NOT NULL
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_falhas.parquet'
        GROUP BY 
            Localidade,
            DataFalha
        ORDER BY 
            total_falhas DESC;
        """
        self.execute_query(insert_data_query)
        return "Dados de falhas por localidade inseridos na tabela intermediate_falhas_por_localidade."

    @task
    def _create_view(self) -> str:
        """
        (Privado) Cria a view view_falhas_por_localidade no ClickHouse, se não existir.
        """
        create_view_query = """
        CREATE OR REPLACE VIEW grupo1.view_falhas_por_localidade AS
        SELECT 
            Localidade,
            DataFalha,
            total_falhas
        FROM grupo1.intermediate_falhas_por_localidade
        ORDER BY total_falhas DESC;
        """
        self.execute_query(create_view_query)
        return "View view_falhas_por_localidade criada (ou já existente)."

    @flow(log_prints=True)
    def run_falhas_por_localidade(self):
        """
        Método público para executar o ETL completo no ClickHouse.
        """
        tables_status = self._create_table()
        print(tables_status)

        falhas_localidade_status = self._insert_data()
        print(falhas_localidade_status)

        view_status = self._create_view()
        print(view_status)


if __name__ == "__main__":
    service = FalhasPorLocalidade()
    service.run_falhas_por_localidade()
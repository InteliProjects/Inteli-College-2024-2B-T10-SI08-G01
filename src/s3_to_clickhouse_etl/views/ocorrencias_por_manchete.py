from prefect import task, flow
from config.clickhouse_client import ClickHouseClient


class OcorrenciasPorManchete:
    """
    Serviço para realizar operações no ClickHouse relacionadas a ocorrências por manchete.
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
        (Privado) Cria a tabela intermediate_ocorrencias_por_manchete no ClickHouse, se necessário.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS grupo1.intermediate_ocorrencias_por_manchete (
            Manchete String,
            DataOcorrencia Date,
            Quantidade_Ocorrencias UInt64
        )
        ENGINE = MergeTree()
        ORDER BY (Manchete, DataOcorrencia);
        """
        self.execute_query(create_table_sql)
        return "Tabela intermediate_ocorrencias_por_manchete criada ou já existente."

    @task
    def _insert_data(self) -> str:
        """
        (Privado) Insere dados na tabela intermediate_ocorrencias_por_manchete.
        """
        insert_data_sql = """
        INSERT INTO grupo1.intermediate_ocorrencias_por_manchete (Manchete, DataOcorrencia, Quantidade_Ocorrencias)
        SELECT 
            JSONExtractString(data_linha, 'Classificacao_Manchete') AS Manchete,
            toDateOrNull(JSONExtractString(data_linha, 'Id_Dataocorrencia')) AS DataOcorrencia,
            COUNT(*) AS Quantidade_Ocorrencias
        FROM grupo1.data_ingestion
        WHERE 
            JSONExtractString(data_linha, 'Classificacao_Manchete') IS NOT NULL
            AND JSONExtractString(data_linha, 'Id_Dataocorrencia') IS NOT NULL
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_ocorrencias.parquet'
        GROUP BY 
            Manchete,
            DataOcorrencia
        ORDER BY 
            Quantidade_Ocorrencias DESC;
        """
        self.execute_query(insert_data_sql)
        return "Dados inseridos na tabela intermediate_ocorrencias_por_manchete com sucesso."

    @task
    def _create_view(self) -> str:
        """
        (Privado) Cria a view ocorrencias_por_manchete consolidada no ClickHouse.
        """
        create_view_sql = """
        CREATE OR REPLACE VIEW grupo1.view_ocorrencias_por_manchete AS
        SELECT 
            Manchete,
            DataOcorrencia,
            Quantidade_Ocorrencias
        FROM grupo1.intermediate_ocorrencias_por_manchete
        ORDER BY Quantidade_Ocorrencias DESC;
        """
        self.execute_query(create_view_sql)
        return "View view_ocorrencias_por_manchete criada ou atualizada com sucesso."

    @flow(log_prints=True)
    def run_ocorrencias_por_manchete(self):
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
    service = OcorrenciasPorManchete()
    service.run_ocorrencias_por_manchete()

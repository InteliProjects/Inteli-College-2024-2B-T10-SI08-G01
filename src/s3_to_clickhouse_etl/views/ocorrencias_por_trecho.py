from prefect import task, flow
from config.clickhouse_client import ClickHouseClient


class OcorrenciasPorTrecho:
    """
    Serviço para realizar operações no ClickHouse relacionadas a ocorrências por trecho.
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
    def _create_tables(self) -> str:
        """
        (Privado) Cria as tabelas necessárias no ClickHouse, se não existirem.
        """
        create_table_unicos = """
        CREATE TABLE IF NOT EXISTS grupo1.valores_unicos (
            Trecho String,
            DataOcorrencia Date,
            total_ocorrencias Int32
        )
        ENGINE = MergeTree()
        ORDER BY (Trecho, DataOcorrencia);
        """
        create_table_correlacionais = """
        CREATE TABLE IF NOT EXISTS grupo1.valores_correlacionais (
            Trecho String,
            DataOcorrencia Date,
            total_ocorrencias Int32
        )
        ENGINE = MergeTree()
        ORDER BY (Trecho, DataOcorrencia);
        """
        self.execute_query(create_table_unicos)
        self.execute_query(create_table_correlacionais)
        return "Tabelas criadas (ou já existentes)."

    @task
    def _insert_valores_unicos(self) -> str:
        """
        (Privado) Insere os valores únicos na tabela valores_unicos no ClickHouse.
        """
        insert_unicos_sql = """
        INSERT INTO grupo1.valores_unicos (Trecho, DataOcorrencia, total_ocorrencias)
        SELECT 
            JSONExtractString(data_linha, 'Trecho') AS Trecho,
            toDateOrNull(JSONExtractString(data_linha, 'Id_Dataocorrencia')) AS DataOcorrencia,
            COUNT(JSONExtractInt(data_linha, 'Sic_Id_Ocorrencia')) AS total_ocorrencias
        FROM grupo1.data_ingestion
        WHERE 
            JSONExtractString(data_linha, 'Trecho') NOT LIKE '%/%'
            AND JSONExtractString(data_linha, 'Id_Dataocorrencia') IS NOT NULL
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_ocorrencias.parquet'
        GROUP BY Trecho, DataOcorrencia
        ORDER BY total_ocorrencias DESC;
        """
        self.execute_query(insert_unicos_sql)
        return "Dados únicos inseridos na tabela valores_unicos."

    @task
    def _insert_valores_correlacionais(self) -> str:
        """
        (Privado) Insere os valores correlacionais na tabela valores_correlacionais no ClickHouse.
        """
        insert_correlacionais_sql = """
        INSERT INTO grupo1.valores_correlacionais (Trecho, DataOcorrencia, total_ocorrencias)
        SELECT 
            CASE
                WHEN JSONExtractString(data_linha, 'Trecho') LIKE '%/%' THEN
                    arrayJoin([JSONExtractString(data_linha, 'Trecho'), reverseUTF8(JSONExtractString(data_linha, 'Trecho'))])
                ELSE JSONExtractString(data_linha, 'Trecho')
            END AS Trecho,
            toDateOrNull(JSONExtractString(data_linha, 'Id_Dataocorrencia')) AS DataOcorrencia,
            COUNT(JSONExtractInt(data_linha, 'Sic_Id_Ocorrencia')) AS total_ocorrencias
        FROM grupo1.data_ingestion
            WHERE 
            JSONExtractString(data_linha, 'Trecho') LIKE '%/%'
            AND JSONExtractString(data_linha, 'Id_Dataocorrencia') IS NOT NULL
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_ocorrencias.parquet'
        GROUP BY Trecho, DataOcorrencia
        ORDER BY total_ocorrencias DESC;
        """
        self.execute_query(insert_correlacionais_sql)
        return "Dados correlacionais inseridos na tabela valores_correlacionais."

    @task
    def _create_view(self) -> str:
        """
        (Privado) Cria uma view consolidando os dados no ClickHouse, se ainda não existir.
        """
        create_view_sql = """
        CREATE OR REPLACE VIEW grupo1.view_ocorrencias_com_tipo AS
        SELECT 
            Trecho,
            DataOcorrencia,
            total_ocorrencias,
            'Unitario' AS tipo_trecho
        FROM grupo1.valores_unicos
        UNION ALL
        SELECT 
            Trecho,
            DataOcorrencia,
            total_ocorrencias,
            'Correlacionado' AS tipo_trecho
        FROM grupo1.valores_correlacionais
        ORDER BY total_ocorrencias DESC;
        """
        self.execute_query(create_view_sql)
        return "View criada (ou já existente)."

    @flow(log_prints=True)
    def run_ocorrencias_por_trecho(self):
        """
        Método público para executar o ETL completo no ClickHouse.
        """
        tables_status = self._create_tables()
        print(tables_status)

        unicos_status = self._insert_valores_unicos()
        print(unicos_status)

        correlacionais_status = self._insert_valores_correlacionais()
        print(correlacionais_status)

        view_status = self._create_view()
        print(view_status)


if __name__ == "__main__":
    service = OcorrenciasPorTrecho()
    service.run_etl()

from prefect import task, flow
from config.clickhouse_client import ClickHouseClient


class FalhasPorIdEquipamento:
    """
    Serviço para realizar operações no ClickHouse relacionadas a falhas por ID_EQUIPAMENTO.
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
        (Privado) Cria a tabela intermediate_falhas_por_id_equipamento no ClickHouse, se não existir.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS grupo1.intermediate_falhas_por_id_equipamento (
            ID_EQUIPAMENTO Int32,
            total_falhas Int32
        )
        ENGINE = MergeTree()
        ORDER BY ID_EQUIPAMENTO;
        """
        self.execute_query(create_table_query)
        return "Tabela intermediate_falhas_por_id_equipamento criada (ou já existente)."

    @task
    def _insert_data(self) -> str:
        """
        (Privado) Insere dados na tabela intermediate_falhas_por_id_equipamento, agrupando por ID_EQUIPAMENTO.
        """
        insert_data_query = """
        INSERT INTO grupo1.intermediate_falhas_por_id_equipamento (ID_EQUIPAMENTO, total_falhas)
        SELECT 
            JSONExtractInt(data_linha, 'ID_EQUIPAMENTO') AS ID_EQUIPAMENTO,
            COUNT(JSONExtractString(data_linha, 'ID_FT_FALHA')) AS total_falhas
        FROM grupo1.data_ingestion
        WHERE JSONExtractInt(data_linha, 'ID_EQUIPAMENTO') IS NOT NULL
        GROUP BY ID_EQUIPAMENTO
        ORDER BY total_falhas DESC;
        """
        self.execute_query(insert_data_query)
        return "Dados de falhas por ID_EQUIPAMENTO inseridos na tabela intermediate_falhas_por_id_equipamento."

    @task
    def _create_view(self) -> str:
        """
        (Privado) Cria a view view_falhas_por_id_equipamento no ClickHouse, se não existir.
        """
        create_view_query = """
        CREATE OR REPLACE VIEW grupo1.view_falhas_por_id_equipamento AS
        SELECT 
            JSONExtractInt(data_linha, 'ID_EQUIPAMENTO') AS ID_EQUIPAMENTO,
            toDateOrNull(JSONExtractString(data_linha, 'ID_DT_FALHA')) AS DataFalha,
            COUNT(*) AS total_falhas
        FROM grupo1.data_ingestion
        WHERE 
            JSONExtractInt(data_linha, 'ID_EQUIPAMENTO') > 0
            AND JSONExtractString(data_linha, 'ID_DT_FALHA') IS NOT NULL
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_falhas.parquet'
        GROUP BY 
            ID_EQUIPAMENTO,
            DataFalha
        ORDER BY 
            total_falhas DESC;
        """
        self.execute_query(create_view_query)
        return "View view_falhas_por_id_equipamento criada (ou já existente)."

    @flow(log_prints=True)
    def run_falhas_por_id_equipamento(self):
        """
        Método público para executar o ETL completo no ClickHouse.
        """
        tables_status = self._create_table()
        print(tables_status) 

        falhas_equipamento_status = self._insert_data()
        print(falhas_equipamento_status)

        view_status = self._create_view()
        print(view_status)


if __name__ == "__main__":
    service = FalhasPorIdEquipamento()
    service.run_falhas_por_id_equipamento()

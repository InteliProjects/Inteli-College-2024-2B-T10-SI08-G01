from prefect import task, flow
from config.clickhouse_client import ClickHouseClient


class FalhasPorHorario:
    """
    Serviço para realizar operações no ClickHouse relacionadas a falhas por horário.
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
    def _create_view(self) -> str:
        """
        (Privado) Cria a view falhas_por_horario consolidada no ClickHouse.
        """
        create_view_sql = """
        CREATE OR REPLACE VIEW grupo1.falhas_por_horario AS
        SELECT
            CAST(
                floor(toFloat32OrNull(replaceAll(JSONExtractString(data_linha, 'HORA_FALHA'), ',', '.')) * 24) AS Int32
            ) AS Horario,
            toDateOrNull(JSONExtractString(data_linha, 'ID_DT_FALHA')) AS DataFalha,
            COUNT(*) AS total_falhas
        FROM grupo1.data_ingestion
        WHERE 
            JSONExtractString(data_linha, 'HORA_FALHA') IS NOT NULL
            AND JSONExtractString(data_linha, 'ID_DT_FALHA') IS NOT NULL
            AND replaceAll(JSONExtractString(data_linha, 'HORA_FALHA'), ',', '.') != ''
            AND toFloat32OrNull(replaceAll(JSONExtractString(data_linha, 'HORA_FALHA'), ',', '.')) IS NOT NULL
            AND floor(toFloat32OrNull(replaceAll(JSONExtractString(data_linha, 'HORA_FALHA'), ',', '.')) * 24) BETWEEN 0 AND 23
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_falhas.parquet'
        GROUP BY 
            Horario,
            DataFalha
        ORDER BY 
            total_falhas DESC;
        """
        self.execute_query(create_view_sql)
        return "View falhas_por_horario criada com sucesso!"

    @flow(log_prints=True)
    def run_falhas_por_horario(self):
        """
        Método público para executar o ETL completo no ClickHouse.
        """
        view_status = self._create_view()
        print(view_status)


if __name__ == "__main__":
    service = FalhasPorHorario()
    service.run_falhas_por_horario()

from prefect import task, flow
from config.clickhouse_client import ClickHouseClient


class OcorrenciasPorHorario:
    """
    Serviço para realizar operações no ClickHouse relacionadas a ocorrências por horário.
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
        (Privado) Cria a view ocorrências_por_horário consolidada no ClickHouse.
        """
        create_view_sql = """
        CREATE OR REPLACE VIEW grupo1.ocorrencias_por_horario AS
        SELECT
            CAST(
                floor(toFloat32(replaceAll(JSONExtractString(data_linha, 'Hora_Ocorrencia'), ',', '.')) * 24) AS Int32
            ) AS Horario,
            toDateOrNull(JSONExtractString(data_linha, 'Id_Dataocorrencia')) AS DataOcorrencia,
            COUNT(*) AS total_ocorrencias
        FROM grupo1.data_ingestion
        WHERE 
            JSONExtractString(data_linha, 'Hora_Ocorrencia') IS NOT NULL
            AND JSONExtractString(data_linha, 'Id_Dataocorrencia') IS NOT NULL
            AND replaceAll(JSONExtractString(data_linha, 'Hora_Ocorrencia'), ',', '.') != ''
            AND data_tag = 'ocorrencias-e-falhas/tabela_big_data_ft_ocorrencias.parquet'
        GROUP BY 
            Horario,
            DataOcorrencia
        ORDER BY 
            total_ocorrencias DESC;
        """
        self.execute_query(create_view_sql)
        return "View ocorrências_por_horario criada com sucesso!"

    @flow(log_prints=True)
    def run_ocorrencias_por_horario(self):
        """
        Método público para executar o ETL completo no ClickHouse.
        """
        view_status = self._create_view()
        print(view_status)


if __name__ == "__main__":
    service = OcorrenciasPorHorario()
    service.run_etl()

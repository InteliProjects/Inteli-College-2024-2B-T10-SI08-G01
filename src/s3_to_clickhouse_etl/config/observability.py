from config.connections import Connections


class ObservabilityLogger:
    """
    Classe para realizar o log de métricas de observabilidade no banco de dados PostgreSQL.
    """

    @staticmethod
    def log_observability(metric_name, start_time, end_time, details):
        """
        Registra métricas de observabilidade no banco de dados.

        :param metric_name: Nome da métrica.
        :param start_time: Timestamp de início.
        :param end_time: Timestamp de término.
        :param details: Detalhes adicionais da métrica.
        """
        conn = Connections.get_postgres_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS observability (
                id SERIAL PRIMARY KEY,
                metric_name VARCHAR(255),
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration INTERVAL,
                details TEXT
            )
        ''')

        duration = end_time - start_time
        cursor.execute('''
            INSERT INTO observability (metric_name, start_time, end_time, duration, details)
            VALUES (%s, %s, %s, %s, %s)
        ''', (metric_name, start_time, end_time, duration, details))

        conn.commit()
        cursor.close()
        conn.close()

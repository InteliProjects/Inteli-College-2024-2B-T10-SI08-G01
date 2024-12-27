# src/tests/test_falhas_por_causa.py

import sys
import os

# Configuração do caminho para suportar imports absolutos
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../s3_to_clickhouse_etl"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from unittest.mock import patch, MagicMock
from views.falhas_por_causa import (
    execute_sql_clickhouse,
    create_tables,
    insert_falhas_por_causa,
    create_view,
    falhas_por_causa_etl
)


def test_execute_sql_clickhouse():
    """
    Este teste verifica se a função execute_sql_clickhouse executa a consulta SQL utilizando o cliente do ClickHouse.
    """
    # Arrange: Configura o mock do Client do clickhouse_driver
    with patch('views.falhas_por_causa.Client') as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        sql_query = "SELECT 1"

        # Act: Chama a função com a consulta SQL de teste
        execute_sql_clickhouse(sql_query)

        # Assert: Verifica se o método execute foi chamado com a consulta correta
        mock_client.execute.assert_called_with(sql_query)


def test_create_tables():
    """
    Este teste verifica se a tarefa create_tables chama a função execute_sql_clickhouse corretamente e retorna a mensagem esperada.
    """
    # Arrange: Mock da função execute_sql_clickhouse
    with patch('views.falhas_por_causa.execute_sql_clickhouse') as mock_execute_sql:
        # Act: Chama a tarefa
        result = create_tables()

        # Assert: Verifica se a função execute_sql_clickhouse foi chamada
        assert mock_execute_sql.called
        # Verifica se o retorno é o esperado
        assert result == "Tabela intermediate_falhas_por_causa criada (ou já existente)."


def test_insert_falhas_por_causa():
    """
    Este teste verifica se a tarefa insert_falhas_por_causa chama a função execute_sql_clickhouse e retorna a mensagem correta.
    """
    # Arrange: Mock da função execute_sql_clickhouse
    with patch('views.falhas_por_causa.execute_sql_clickhouse') as mock_execute_sql:
        # Act: Chama a tarefa
        result = insert_falhas_por_causa()

        # Assert: Verifica se a função execute_sql_clickhouse foi chamada
        assert mock_execute_sql.called
        # Verifica se o retorno é o esperado
        assert result == "Dados de falhas por causa inseridos na tabela intermediate_falhas_por_causa."


def test_create_view():
    """
    Este teste verifica se a tarefa create_view chama a função execute_sql_clickhouse e retorna a mensagem esperada.
    """
    # Arrange: Mock da função execute_sql_clickhouse
    with patch('views.falhas_por_causa.execute_sql_clickhouse') as mock_execute_sql:
        # Act: Chama a tarefa
        result = create_view()

        # Assert: Verifica se a função execute_sql_clickhouse foi chamada
        assert mock_execute_sql.called
        # Verifica se o retorno é o esperado
        assert result == "View view_falhas_por_causa criada (ou já existente)."


def test_falhas_por_causa_etl():
    """
    Este teste verifica se o flow falhas_por_causa_etl chama as tarefas na ordem correta.
    """
    # Arrange: Mock das tarefas
    with patch('views.falhas_por_causa.create_tables') as mock_create_tables, \
         patch('views.falhas_por_causa.insert_falhas_por_causa') as mock_insert_falhas, \
         patch('views.falhas_por_causa.create_view') as mock_create_view:
        # Configura os retornos das tarefas
        mock_create_tables.return_value = "Tabela criada"
        mock_insert_falhas.return_value = "Dados inseridos"
        mock_create_view.return_value = "View criada"

        # Act: Chama o flow
        falhas_por_causa_etl()

        # Assert: Verifica se as tarefas foram chamadas na ordem correta
        mock_create_tables.assert_called_once()
        mock_insert_falhas.assert_called_once()
        mock_create_view.assert_called_once()

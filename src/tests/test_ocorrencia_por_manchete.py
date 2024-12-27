import pytest
from unittest.mock import patch, MagicMock
from s3_to_clickhouse_etl.views.ocorrencias_por_manchete import OcorrenciasPorManchete

# Testa a execução de query no ClickHouse (caminho feliz)
@patch('s3_to_clickhouse_etl.views.ocorrencias_por_manchete.ClickHouseClient')
def test_execute_query(mock_client):
    """
    Testa a execução de query no ClickHouse (caminho feliz).
    - Arrange: Mock do cliente ClickHouse para simular execução sem erro.
    - Act: Criação do serviço e chamada do método execute_query.
    - Assert: Verifica se a query foi executada corretamente.
    """
    service = OcorrenciasPorManchete()
    query = "SELECT * FROM test"
    
    service.execute_query(query)
    
    mock_client.return_value.execute_query.assert_called_once_with(query)

# Testa a execução de query no ClickHouse (caminho triste)
@patch('s3_to_clickhouse_etl.views.ocorrencias_por_manchete.ClickHouseClient')
def test_execute_query_failure(mock_client):
    """
    Testa a execução de query no ClickHouse (caminho triste).
    - Arrange: Mock do cliente ClickHouse para simular erro.
    - Act: Criação do serviço e tentativa de executar query.
    - Assert: Verifica se a exceção é levantada corretamente.
    """
    mock_client.return_value.execute_query.side_effect = Exception("Erro na execução da query")
    service = OcorrenciasPorManchete()
    
    with pytest.raises(Exception) as excinfo:
        service.execute_query("SELECT * FROM test")
    assert str(excinfo.value) == "Erro na execução da query"

# Testa a criação da view de ocorrências por manchete (caminho feliz)
@patch('s3_to_clickhouse_etl.views.ocorrencias_por_manchete.OcorrenciasPorManchete.execute_query')
def test_create_view_ocorrencias_por_manchete(mock_execute_query):
    """
    Testa a criação da view de ocorrências por manchete (caminho feliz).
    - Arrange: Mock da função execute_query para retornar None (sucesso).
    - Act: Criação do serviço e chamada do método _create_view_ocorrencias_por_manchete.
    - Assert: Verifica se a mensagem correta foi retornada.
    """
    mock_execute_query.return_value = None
    service = OcorrenciasPorManchete()
    
    result = service._create_view_ocorrencias_por_manchete()
    
    assert "View view_ocorrencias_por_manchete criada" in result
    mock_execute_query.assert_called_once()

# Testa a criação da view de ocorrências por manchete (caminho triste)
@patch('s3_to_clickhouse_etl.views.ocorrencias_por_manchete.OcorrenciasPorManchete.execute_query')
def test_create_view_ocorrencias_por_manchete_failure(mock_execute_query):
    """
    Testa a criação da view de ocorrências por manchete (caminho triste).
    - Arrange: Mock da função execute_query para lançar uma exceção.
    - Act: Criação do serviço e tentativa de criar view.
    - Assert: Verifica se a exceção é levantada corretamente.
    """
    mock_execute_query.side_effect = Exception("Erro ao criar view")
    service = OcorrenciasPorManchete()
    
    with pytest.raises(Exception) as excinfo:
        service._create_view_ocorrencias_por_manchete()
    assert str(excinfo.value) == "Erro ao criar view"

# Testa o fluxo completo de criação da view (caminho feliz)
@patch('s3_to_clickhouse_etl.views.ocorrencias_por_manchete.OcorrenciasPorManchete._create_view_ocorrencias_por_manchete')
def test_run_ocorrencias_por_manchete(mock_create_view):
    """
    Testa o fluxo completo de criação da view (caminho feliz).
    - Arrange: Mock do método _create_view_ocorrencias_por_manchete para simular sucesso.
    - Act: Criação do serviço e execução do fluxo completo.
    - Assert: Verifica se o método foi chamado corretamente.
    """
    service = OcorrenciasPorManchete()
    
    service.run_ocorrencias_por_manchete()
    
    mock_create_view.assert_called_once()

# Testa o fluxo completo de criação da view (caminho triste)
@patch('s3_to_clickhouse_etl.views.ocorrencias_por_manchete.OcorrenciasPorManchete._create_view_ocorrencias_por_manchete')
def test_run_ocorrencias_por_manchete_failure(mock_create_view):
    """
    Testa o fluxo completo de criação da view (caminho triste).
    - Arrange: Mock do método _create_view_ocorrencias_por_manchete para simular erro.
    - Act: Criação do serviço e tentativa de executar o fluxo completo.
    - Assert: Verifica se a exceção é levantada corretamente.
    """
    mock_create_view.side_effect = Exception("Erro no fluxo de criação da view")
    service = OcorrenciasPorManchete()
    
    with pytest.raises(Exception) as excinfo:
        service.run_ocorrencias_por_manchete()
    assert str(excinfo.value) == "Erro no fluxo de criação da view"
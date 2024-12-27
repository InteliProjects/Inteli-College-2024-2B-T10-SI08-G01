import pytest
from unittest.mock import patch
from s3_to_clickhouse_etl.views.falhas_por_trecho_etl import FalhasPorTrecho

# Teste positivo para criação de tabelas relacionadas a falha_por_trecho
@patch('s3_to_clickhouse_etl.views.falhas_por_trecho_etl.FalhasPorTrecho.execute_query')
def test_successful_table_creation(mock_execute_query):
    """
    Contexto: Garantir que o sistema consegue criar as tabelas necessárias sem interrupções.
    Objetivo: Verificar que o método retorna a mensagem esperada e executa o número correto de queries.
    
    - Configuração: Mock do método `execute_query` para emular funcionamento normal.
    - Execução: Chamada ao método `_create_tables` da classe FalhaPorTrecho.
    - Verificação: Asserção da resposta e validação da quantidade de chamadas realizadas.
    """
    mock_execute_query.return_value = None  # Simula execução bem-sucedida

    falha_service = FalhaPorTrecho()
    response = falha_service._create_tables()

    assert response == "As tabelas foram criadas ou já existem."
    assert mock_execute_query.call_count == 2  # Devem ser realizadas duas chamadas


# Teste negativo para falha na criação de tabelas em falha_por_trecho
@patch('s3_to_clickhouse_etl.views.falhas_por_trecho_etl.FalhasPorTrecho.execute_query')
def test_table_creation_error(mock_execute_query):
    """
    Contexto: Simular falha na criação de tabelas.
    Objetivo: Confirmar que o método levanta a exceção correta ao encontrar erros durante a execução.
    
    - Configuração: Mock do método `execute_query` para gerar uma exceção.
    - Execução: Tentativa de criar tabelas através do método `_create_tables`.
    - Verificação: Checar a mensagem da exceção levantada.
    """
    mock_execute_query.side_effect = Exception("Erro durante a criação das tabelas")

    falha_service = FalhaPorTrecho()

    with pytest.raises(Exception) as exception_info:
        falha_service._create_tables()

    assert "Erro durante a criação das tabelas" in str(exception_info.value)


# Teste positivo para inserção de dados na tabela falha_por_trecho
@patch('s3_to_clickhouse_etl.views.falhas_por_trecho_etl.FalhasPorTrecho.execute_query')
def test_successful_data_insertion(mock_execute_query):
    """
    Contexto: Inserir registros na tabela falha_por_trecho sem problemas.
    Objetivo: Garantir que a execução ocorre sem erros e que a mensagem esperada é retornada.
    
    - Configuração: Mock do método `execute_query` para simular uma inserção bem-sucedida.
    - Execução: Chamada do método `_insert_dados`.
    - Verificação: Validação da mensagem de sucesso e contagem de chamadas ao banco.
    """
    mock_execute_query.return_value = None  # Simula sucesso na execução da query

    falha_service = FalhaPorTrecho()
    response = falha_service._insert_dados()

    assert response == "Os dados foram adicionados à tabela falha_por_trecho."
    assert mock_execute_query.call_count == 1  # Apenas uma query é esperada


# Teste negativo para falha na inserção de dados na tabela falha_por_trecho
@patch('s3_to_clickhouse_etl.views.falhas_por_trecho_etl.FalhasPorTrecho.execute_query')
def test_data_insertion_error(mock_execute_query):
    """
    Contexto: Simular falha durante a tentativa de inserir registros.
    Objetivo: Garantir que o erro é detectado e tratado corretamente.
    
    - Configuração: Mock do método `execute_query` para gerar uma exceção.
    - Execução: Tentativa de inserir dados usando o método `_insert_dados`.
    - Verificação: Validação da mensagem de erro na exceção capturada.
    """
    mock_execute_query.side_effect = Exception("Erro ao tentar inserir os dados")

    falha_service = FalhaPorTrecho()

    with pytest.raises(Exception) as exception_info:
        falha_service._insert_dados()

    assert "Erro ao tentar inserir os dados" in str(exception_info.value)

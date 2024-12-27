
# ETL para ClickHouse

Este projeto implementa fluxos de ETL (Extract, Transform, Load) utilizando **Prefect** para ingerir dados de falhas e armazená-los no banco de dados **ClickHouse**. Inclui testes automatizados com **pytest** para garantir a qualidade e funcionalidade do código.

## Pré-requisitos

- **Python 3.10** ou superior
- **Git**

## Instalação

1. **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv env
    source env/bin/activate  # No Windows: env\Scripts\activate
    ```

2. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ``` 
    Obs.: a lib `pytest` deve ser instalada para que os testes possam ser executados.
   

## Executando os Testes

Com o ambiente virtual ativado, execute os testes usando:
```bash
pytest
```
Os testes estão localizados na pasta `src/tests/` e verificarão a funcionalidade das funções e fluxos de ETL implementados.

## Descrição dos Testes

### `test_falhas_por_causa.py`

#### `test_execute_sql_clickhouse`
- Verifica se a função `execute_sql_clickhouse` executa corretamente uma consulta SQL usando o cliente ClickHouse.

#### `test_create_tables`
- Verifica se a tarefa `create_tables` chama `execute_sql_clickhouse` e retorna a mensagem esperada.

#### `test_insert_falhas_por_causa`
- Verifica se a tarefa `insert_falhas_por_causa` chama `execute_sql_clickhouse` e retorna a mensagem correta.

#### `test_create_view`
- Verifica se a tarefa `create_view` chama `execute_sql_clickhouse` e retorna a mensagem esperada.

#### `test_falhas_por_causa_etl`
- Verifica se o fluxo `falhas_por_causa_etl` executa as tarefas na ordem correta.

### `test_falhas_por_id_equipamento.py`

#### `test_execute_sql_clickhouse`
- Verifica se a função `execute_sql_clickhouse` executa corretamente uma consulta SQL usando o cliente ClickHouse.

#### `test_create_tables`
- Verifica se a tarefa `create_tables` chama `execute_sql_clickhouse` e retorna a mensagem esperada.

#### `test_insert_falhas_por_id_equipamento`
- Verifica se a tarefa `insert_falhas_por_id_equipamento` chama `execute_sql_clickhouse` e retorna a mensagem correta.

#### `test_create_view`
- Verifica se a tarefa `create_view` chama `execute_sql_clickhouse` e retorna a mensagem esperada.

#### `test_falhas_por_id_equipamento_etl`
- Verifica se o fluxo `falhas_por_id_equipamento_etl` executa as tarefas na ordem correta.

## Estrutura do Projeto

```
2024-2B-T10-SI08-G01/
│
├── src/
│   ├── s3_to_clickhouse_etl/
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── falhas_por_causa.py
│   │   │   └── falhas_por_id_equipamento.py
│   │   └── __init__.py
│   └── tests/
│       ├── __init__.py
│       ├── test_falhas_por_causa.py
│       └── test_falhas_por_id_equipamento.py
├── .env
├── requirements.txt
└── pytest.ini
```
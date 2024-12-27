# Estrutura de Ingestão de Dados

## Introdução 
<p align="justify">&emsp;&emsp; O processo de ETL (Extract, Transform, Load) é fundamental para a integração e gestão de dados em ambientes corporativos modernos. A sigla refere-se às três etapas principais desse processo: Extração, Transformação e Carga. Durante a extração, os dados são coletados de diferentes fontes, sejam sistemas legados, bancos de dados ou outras plataformas. Em seguida, na transformação, esses dados são ajustados, limpos e combinados de acordo com as necessidades da empresa, garantindo que atendam a padrões de qualidade e sejam consistentes. Por fim, os dados são carregados no destino final, como um Data Warehouse ou Data Mart, onde ficam disponíveis para análises e decisões estratégicas. O ETL é essencial para consolidar informações de várias fontes e fornecer uma base sólida para a tomada de decisões mais informadas e eficientes.</p>

## Relatório de Processamento de Dados - Processo ETL

### Ferramentas Utilizadas

- **Amazon S3**: Usado para armazenar e fornecer acesso aos arquivos Parquet que contêm os dados brutos.
- **ClickHouse**: Utilizado como o banco de dados de destino para armazenar e consultar os dados transformados.
- **PyArrow**: Utilizado para ler arquivos Parquet e converter para um formato manipulável em Python.
- **JSON**: Utilizado para estruturar e validar os dados antes de inseri-los no banco de dados.
- **Python**: A linguagem de programação principal usada para o processo ETL.
- **Datetime e Timezone**: Módulos para gerenciar a data e hora no processo de ingestão.


### Fluxo do Processo ETL

#### 1. Extração (Extract)

<p align="justify">&emsp;&emsp;Na etapa de extração, o processo começa com a coleta de arquivos Parquet armazenados no Amazon S3. A função `get_parquet_files` é responsável por listar os arquivos dentro do bucket especificado, usando o prefixo "ocorrencias-e-falhas/". O código obtém todos os arquivos `.parquet` presentes no bucket, o que permite a extração dos dados necessários para o processamento</p>

```python
def get_parquet_files(bucket_name, prefix="ocorrencias-e-falhas/"):
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.parquet')]
```

#### 2. Transformação (Transform)
<p align="justify">&emsp;&emsp;Na etapa de transformação, os dados são processados e preparados para garantir que atendam aos requisitos de qualidade antes de serem carregados no banco de dados ClickHouse. A função read_parquet_and_insert_to_clickhouse realiza a leitura dos arquivos Parquet diretamente do Amazon S3, transforma cada linha para o formato desejado e executa validações de acordo com o esquema DataOcorrencias. Para cada linha validada, um registro é criado com três colunas principais: data_ingestao (data de ingestão), data_linha (dados formatados da linha) e data_tag (identificação do arquivo).

```python
def read_parquet_and_insert_to_clickhouse(bucket_name, file_key):
    start_time = datetime.now(timezone.utc)
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    
    parquet_data = pq.read_table(io.BytesIO(obj['Body'].read()))

    client = get_clickhouse_client()

    client.execute(f'''
    CREATE TABLE IF NOT EXISTS grupo1.data_ingestion (
        data_ingestao DateTime,
        data_linha String,
        data_tag String
    ) ENGINE = MergeTree()
    ORDER BY data_ingestao
    ''')

    schema = DataOcorrencias

    rows = []
    for batch in parquet_data.to_batches():
        for row in batch.to_pylist():
            try:
                row_with_spaces = {key.replace(" ", "_"): value for key, value in row.items()}
                validated_row = schema(**row_with_spaces)
                
                data_linha = json.dumps(validated_row.dict())
                data_ingestao = datetime.now(timezone.utc)
                data_tag = file_key
                rows.append((data_ingestao, data_linha, data_tag))
            
            except Exception as e:
                print(f"Erro de validação na linha {row}: {e}")

    if rows:
        client.execute(
            "INSERT INTO grupo1.data_ingestion (data_ingestao, data_linha, data_tag) VALUES",
            rows
        )

    end_time = datetime.now(timezone.utc)
    details = f"Processed {len(rows)} valid records from {file_key} in bucket {bucket_name} and inserted into ClickHouse"
    log_observability("read_parquet_and_insert_to_clickhouse", start_time, end_time, details)
```

#### Decisões

&emsp;&emsp;Durante o processo de implementação, algumas decisões foram tomadas para otimizar a eficiência e garantir a integridade dos dados. Primeiramente, foi estabelecido um esquema de validação chamado `DataOcorrencias`, cujo propósito é assegurar que os dados atendam aos requisitos de integridade. Além disso, esse esquema realiza a renomeação automática de chaves que contêm espaços, facilitando a consistência dos dados durante a ingestão.

&emsp;&emsp;O ClickHouse foi escolhido como banco de dados devido ao seu alto desempenho em análise de grandes volumes de dados. Esse banco é especialmente adequado para cenários em que há necessidade de consultas analíticas rápidas, tornando-o uma opção eficiente para a carga de dados transformados. Outra decisão importante foi a criação dinâmica da tabela de destino no ClickHouse. Isso permite que a tabela seja gerada automaticamente caso não exista, simplificando o fluxo de ingestão e tornando o processo menos suscetível a erros de configuração.

#### Desafios

&emsp;&emsp;Durante a implementação do processo, surgiram desafios relacionados à validação dos dados. Em linhas específicas, foram encontrados erros que poderiam interromper a ingestão. Para lidar com esses problemas, foi implementado um bloco `try-except` no código, que permite registrar e tratar falhas em linhas individuais sem interromper o processo como um todo. Esse tratamento garante que erros pontuais não comprometam a integridade do fluxo de ingestão e mantém a continuidade do processo de forma robusta e confiável.

#### 3. Carregar (Load)
<p align="justify">&emsp;&emsp;A etapa de carregar consiste em inserir os dados transformados e validados no banco de dados ClickHouse. Após a validação de cada linha do arquivo Parquet, os dados são formatados e carregados na tabela de destino `data_ingestion` no ClickHouse. Se a tabela não existir, ela é criada dinamicamente, garantindo que o processo possa ser executado sem pré-configuração manual. A função `read_parquet_and_insert_to_clickhouse` é responsável por essa etapa de carga, onde cada linha validada é inserida com três colunas principais: `data_ingestao` (timestamp de quando a linha foi inserida), `data_linha` (conteúdo formatado da linha) e `data_tag` (identificação do arquivo para rastreamento).</p>

## Observabilidade e Métricas de Performance

<p align="justify">&emsp;&emsp;A implementação do processo de ETL inclui mecanismos de observabilidade e coleta de métricas para monitorar e avaliar o desempenho das operações. Cada etapa do processo gera logs detalhados que incluem timestamps, identificadores de arquivos processados e informações de sucesso ou falha. Em casos de erro durante a validação ou inserção de dados, o código registra a linha problemática e o motivo da falha, garantindo que o problema possa ser identificado e corrigido rapidamente. Para rastreamento, a coluna data_tag no banco de dados armazena o identificador do arquivo processado, permitindo localizar a origem dos dados.</p>

<p align="justify">&emsp;&emsp;Além disso, métricas importantes como o número de registros válidos processados, a duração de cada operação (extração, transformação e carga) e a taxa de sucesso são calculadas e registradas para análise posterior. O tempo de processamento de cada execução é medido utilizando o intervalo entre o início e o término do processo, essencial para identificar gargalos de desempenho. O número de registros processados, tanto válidos quanto inválidos, é contabilizado em cada execução, oferecendo insights sobre a qualidade dos dados e o desempenho do sistema. Erros por linha são registrados, destacando a proporção de linhas rejeitadas em relação ao total processado, o que permite uma visão clara de problemas recorrentes nos dados de origem.</p>


<p align="justify">&emsp;&emsp;A função log_observability, por exemplo, é usada para registrar informações essenciais de cada etapa do processo, como o nome da etapa, o horário de início, o horário de término, a duração e detalhes do processamento. Isso possibilita o monitoramento contínuo e uma análise mais aprofundada de desempenho.</p>


## Conclusão
<p align="justify">&emsp;&emsp;O ETL é uma ferramenta indispensável para empresas que precisam consolidar dados de origens diversas e torná-los acessíveis de forma centralizada e organizada. Sua importância está no fato de que ele não apenas integra dados, mas também os transforma em um formato adequado para análise e geração de relatórios, suportando processos de Business Intelligence (BI) e planejamento estratégico. A implementação de um processo ETL eficiente permite que as organizações mantenham a qualidade e a consistência dos dados, contribuindo para decisões mais assertivas e baseadas em informações precisas e atualizadas. Dessa forma, o ETL se apresenta como uma peça chave na transformação digital das empresas, permitindo o aproveitamento máximo do potencial dos seus dados.</p>






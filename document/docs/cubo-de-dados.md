# Cubo de Dados

<p align="justify">&emsp;&emsp; Um cubo de dados é uma estrutura multidimensional que permite a organização e análise de dados a partir de diferentes perspectivas, permitindo consultas rápidas e eficientes. Essa estrutura é utilizada com frequência em sistemas de Business Intelligence (BI) para sumarizar e organizar grandes volumes de dados de forma que se tornem facilmente acessíveis para análises. </p>

### Aplicação

<p align="justify">&emsp;&emsp; No projeto, o cubo de dados será utilizado para armazenar e analisar informações sobre Ocorrências e Falhas. Visamos facilitar o acompanhamento dos eventos operacionais que impactam a rede ferroviária, como falhas de equipamentos e ocorrências de vandalismo ou acidentes. Permitirá também que a CPTM visualize padrões, analise o desempenho e performance de algumas KPI’s e tome ações proativas para melhorar a eficiência operacional e reduzir custos, ou entender melhor a causa e foco dos gastos, por exemplo. </p>

---

## Dimensões

<p align="justify">&emsp;&emsp; O cubo de dados permite que as informações sejam agregadas em dimensões, como tempo, localidade, tipo de evento, entre outras. Com ele, é possível responder a perguntas complexas, como quais tipos de eventos ocorrem com maior frequência em determinadas localizações ou qual é o tempo médio de resolução para uma falha específica. Isso torna o cubo de dados uma ferramenta essencial para monitoramento e tomada de decisões baseadas em dados, que é o principal foco da CPTM. </p>
  
### Tabela das Dimensões

<p align="justify">&emsp;&emsp; Tabela das dimensões do cubo de dados, organizando suas hierarquias, descrições e aplicações. Cada dimensão reflete um aspecto essencial para a análise e monitoramento das ocorrências e falhas, permitindo identificar padrões, priorizar ações corretivas e otimizar recursos. As hierarquias facilitam a segmentação dos dados, enquanto as aplicações destacam o impacto operacional e estratégico de cada dimensão. </p>

| **Dimensão**           | **Hierarquia**                             | **Descrição**                                                                                      | **Aplicação**                                                                                                                  |
|-------------------------|--------------------------------------------|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| **Tempo**              | Ano → Mês → Dia → Hora            | Representa o momento em que uma ocorrência ou falha foi registrada.                              | Analisar frequência, identificar sazonalidades, picos de falhas, e avaliar a eficácia de ações em períodos específicos.      |
| **Causa/Razão**        | Categoria de Falha → Subcategoria → Causa  | Refere-se à natureza/motivo específico do evento (usando palavras-chave ou códigos).             | Identificar causas mais frequentes e priorizar ações corretivas/preventivas em problemas recorrentes ou críticos.           |
| **Classificação do Evento** | Ocorrências - Falhas (sem hierarquia)                    | Distingue os eventos por natureza (ex.: "Ocorrência" ou "Falha").                                | Separar eventos operacionais de eventos externos (ex.: vandalismo). Facilita análises independentes e relatórios específicos. |
| **Tipo do Evento**     | Categoria Geral → Subcategoria Específica  | Classifica o evento em tipos de falhas (preventiva, corretiva) ou ocorrências (vandalismo, acidente). | Entender frequência de eventos específicos, otimizar alocação de recursos e priorizar ações preventivas.                     |
| **Trecho**             | Linha → Estação → Ponto Específico         | Refere-se à localização específica onde ocorreu o evento.                                         | Identificar pontos críticos de falhas/ocorrências em regiões específicas (ex.: estação ou trecho de linha).                  |
| **Equipamento**        | Grupo de Equipamentos → Tipo → ID Específico | Identificação dos equipamentos associados ao evento.                                              | Monitorar equipamentos com maior frequência de falhas, otimizando manutenção e planejamento de substituições.                |


---

## Planilhas

<p align="justify">&emsp;&emsp; Uma planilha (ou view) é uma consulta armazenada que permite visualizar dados de forma estruturada, geralmente filtrando, agrupando ou agregando informações de várias tabelas de origem. As views criadas para projeto, como ocorrencias_por_horario, falhas_por_causa, falhas_por_id_equipamento, facilitam a consulta e a análise de dados já processados. </p>

<p align="justify">&emsp;&emsp; As views foram projetadas para fornecer insights críticos, facilitando a tomada de decisões estratégicas para manutenção e otimização operacional. Todas as views utilizam dados da coluna `data_linha`, que está no formato JSON e contém as colunas correspondentes às tabelas de ocorrências e de linha. As queries empregam a função `JSONExtract` para processar e transformar os dados. </p>

<p align="justify">&emsp;&emsp; Além disso, cada view foi automatizada com o Prefect, utilizando um pipeline que engloba os fluxos (flows) para a criação das tasks de todas as views e do ETL. Esse pipeline está implementado no arquivo principal `app.py`. </p>

---

### 1. View `falhas_por_trecho`

<p align="center">Imagem XX - Tabela de falhas por trecho</p>

<div align="center">
    
![Tabela de falhas por trecho](https://res.cloudinary.com/ds6aq9roo/image/upload/v1732475989/falhas_por_trecho_bukj9x.png)

</div>

<p align="center">Fonte: Autoria própria.</p>

#### Explicação 
Agrupa as falhas com base no trecho de incidência:
- **Contabiliza Falhas**: Soma o total de falhas por trecho utilizando a função de agregação `COUNT(*)`.
- **Agrupa e Ordena**: Organiza os resultados por trecho e classifica em ordem decrescente com base no número total de falhas.

#### Importância
- **Identifica Regiões Críticas**: Prioriza trechos com maior número de falhas para manutenção.
- **Melhora a Alocação de Recursos**: Facilita decisões estratégicas para distribuição de equipes.

---

### 2. View `ocorrencias_por_horario`

<p align="center">Imagem XX - Tabela de ocorrências por horário</p>

<div align="center">
    
![Tabela de ocorrências por horário](https://res.cloudinary.com/ds6aq9roo/image/upload/v1732475989/ocorrencias_por_horario_gp7tsc.png)

</div>

<p align="center">Fonte: Autoria própria.</p>

#### Explicação 
Analisa ocorrências ao longo das 24 horas do dia:
- **Agrupa e Conta**: Soma o total de ocorrências para cada hora do dia.
- **Organiza**: Classifica os dados por horário para facilitar a visualização.

#### Importância
- **Identifica Picos de Ocorrência**: Auxilia na alocação de equipes em horários críticos.
- **Planejamento Operacional**: Reduz impacto em horários de maior fluxo.

---

### 3. View `ocorrencias_por_manchete`

<p align="center">Imagem XX - Tabela de ocorrências por manchete</p>

<div align="center">
    
![Tabela de ocorrências por manchete](https://res.cloudinary.com/ds6aq9roo/image/upload/v1732475989/ocorrencia_por_manchete_fcwrfm.png)

</div>

<p align="center">Fonte: Autoria própria.</p>

#### Explicação 
Agrupa ocorrências conforme a manchete categorizada (e.g., Segurança Pública, Operação):
- **Agrupamento por Categoria**: Baseia-se no campo `manchete` para contabilizar as ocorrências por cada categoria.
- **Cálculo de Ocorrências**: Utiliza `SUM` ou `COUNT` para totalizar eventos por categoria.

#### Importância
- **Prioriza Intervenções**: Ajuda a decidir áreas de ação, como reforço na segurança pública.
- **Análise Estratégica**: Apoia decisões para reduzir causas de ocorrência.

---

### 4. View `falhas_por_id_equipamento`

<p align="center">Imagem XX - Tabela de falhas por id de equipamento</p>

<div align="center">
    
![Tabela de falhas por id de equipamento](https://res.cloudinary.com/ds6aq9roo/image/upload/v1732475989/falha_por_id_equipamento_yd5nzr.png)

</div>

<p align="center">Fonte: Autoria própria.</p>

#### Explicação 
Identifica falhas associadas a equipamentos específicos:
- **Relaciona ID de Equipamento e Falhas**: Mapeia as ocorrências por equipamento para acessar os IDs.
- **Agrupamento e Ordenação**: Ordena os IDs de equipamento com base no total de falhas.

#### Importância
- **Troca de Fornecedor**: Identifica equipamentos problemáticos, sugerindo ajustes de fornecedor ou recorrencia de manutenção.
- **Redução de Custos**: Melhora a durabilidade e eficiência dos equipamentos.

---

### 5. View `ocorrencias_com_tipo`

<p align="center">Imagem XX - Tabela de ocorrências com tipo</p>

<div align="center">
    
![Tabela de ocorrências com tipo](https://res.cloudinary.com/ds6aq9roo/image/upload/v1732476001/ocorrencias_com_tipo_sbfosa.png)

</div>

<p align="center">Fonte: Autoria própria.</p>

#### Explicação 
Filtra ocorrências por tipo de trecho:
- **Classificação Unitária/Correlacionada**: Cria uma nova coluna em uma tabela temporária para identificar o tipo de trecho (unitário ou correlacionado).
- **Análise por Tipo**: Agrupa os dados e apresenta a quantidade de ocorrências por tipo de trecho.

#### Importância
- **Otimização de Linhas**: Identifica trajetos e estações problemáticas.
- **Planejamento Estrutural**: Base para reforço de segurança e melhorias na linha.

---

### 6. View `falhas_por_causa`

<p align="center">Imagem XX - Tabela de falhas por causa</p>

<div align="center">
    
![Tabela de falhas por causa](https://res.cloudinary.com/ds6aq9roo/image/upload/v1732475989/falhas_por_causa_fbwvlx.png)

</div>
    
<p align="center">Fonte: Autoria própria.</p>

#### Explicação
Identifica as principais causas das falhas: 
- **Contagem de Falhas**: Agrupa os dados por causa e soma o número de ocorrências.
- **Relação de Causa**: Agrupa as causas por palavras chave e retorna o númeo correpondentes àquela causa.

#### Importância
- **Ações Preventivas**: Reduz falhas causadas por fatores recorrentes, como vandalismo ou problemas técnicos.
- **Mitigação de Riscos**: Melhora a segurança e eficiência geral.

*Essa view ainda será ajustada para agrupar as causas por palavras chave e filtráveis por busca*

---

## Automatização

<p align="justify">&emsp;&emsp; Com o Prefect, é possível automatizar a criação e atualização das views. Isso é útil em fluxos de ETL, onde novas entradas de dados são processadas regularmente. Para automatizar a view, cria-se um fluxo que inclui a lógica necessária para atualizar ou criar a view no banco de dados. As views e o processo ETL foram automatizados utilizando o Prefect Cloud, com implementação centralizada no arquivo `app.py`. </p>

#### Detalhes do Pipeline
- **Pipeline Unificado**: O pipeline engloba todos os fluxos necessários para a criação e manutenção das views e do ETL, utilizando o Prefect para combinar as tarefas e fluxos. A definição de tarefas é feita com o decorador `@task` no arquivo da view, enquanto o fluxo que gerencia a sequência das operações é definido com o decorador `@flow`.
- **Monitoramento e Agendamento**: O Prefect permite monitorar o status de cada task em tempo real e também possibilita o agendamento de atualizações regulares das views, através de fluxos definidos com o decorador @flow. Além disso, o Prefect Cloud oferece uma interface para acompanhar a execução e o progresso das tarefas, garantindo que o sistema esteja sempre atualizado.
- **Reexecução Automatizada**: Em caso de falhas, os fluxos podem ser configurados para reexecução automática, garantindo a continuidade do processo sem intervenção manual. A integração com o Flask, utilizando o decorador @app.route, também permite que os fluxos sejam executados quando necessário, ao acessar os endpoints específicos via HTTP.
- **Tempo de Execução**: Até o momento, cada view possui uma média de 5 segundos de execução, enquanto o ETL toma cerca de 17 minutos para realizar a extração, transformação e carga dos dados.

#### Benefícios
- **Dados Atualizados**: Assim como as views, o ETL principal que alimenta o `data-ingestion` foi automatizado, o que os deixa sempre sincronizados com os dados mais recentes.
- **Confiabilidade**: A arquitetura baseada em Prefect garante escalabilidade.
- **Simplicidade**: A integração centralizada no `app.py` facilita manutenção e ajustes futuros.

---

## Conclusão

<p align="justify">&emsp;&emsp; As dimensões selecionadas para o cubo de dados fornecem uma estrutura abrangente para o monitoramento e análise de ocorrências e falhas no sistema de trens da CPTM. Com o uso das visualizações geradas no data app, gestores e operadores poderão acessar informações de forma rápida e segmentada, facilitando a tomada de decisões baseada em dados. Esse sistema auxiliará na identificação de padrões, otimização de recursos e na implementação de ações corretivas e preventivas, contribuindo para a melhoria da eficiência operacional e redução de custos. </p>

 <p align="justify">&emsp;&emsp; A integração com o Prefect agrega um nível adicional de automação e confiabilidade ao processo, garantindo que todas as views sejam atualizadas de maneira contínua e eficiente por meio de um pipeline centralizado no arquivo `app.py`. Essa solução unificada permite monitorar, agendar e gerenciar os fluxos de trabalho, oferecendo maior visibilidade de possiveis falhas. Além disso, o sistema proporciona visualizações importantes e detalhadas do processo, como a identificação de trechos críticos, horários de maior incidência de ocorrências e equipamentos com maior índice de falhas, tornando possível a priorização de ações em áreas estratégicas e de alto impacto. Dessa forma, o projeto não apenas potencializa o desempenho operacional da CPTM, mas também promove a inovação na gestão de dados e no planejamento de ações para mitigar falhas e ocorrências.</p>

## Referências:

**AERO Engenharia.** O que é: Cubo de dados. Disponível em: <https://aeroengenharia.com/glossario/o-que-e-cubo-de-dados/>. Acesso em: 13 nov. 2024.

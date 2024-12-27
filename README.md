# Inteli - Instituto de Tecnologia e Liderança 

<p align="center">
  <a href="https://www.inteli.edu.br/">
    <img src="https://res.cloudinary.com/dp4liildh/image/upload/v1727900405/inteli_fooxgo.png" 
         alt="Inteli - Instituto de Tecnologia e Liderança" 
         style="border:0; max-width:100%; height:auto;">
  </a>
</p>

# Integração, Gerenciamento e Análise de Big Data

## Xpress

### Integrantes: 
- <a href="https://www.linkedin.com/in/daniel-a-mendez-571217251/">Daniel Augusto Rivas Mendez</a>
- <a href="https://www.linkedin.com/in/danielzular/">Daniel Zular</a>
- <a href="https://www.linkedin.com/in/enzoboccia/">Enzo Boccia Pagliara</a>
- <a href="https://www.linkedin.com/in/luizarsantana/">Luiza Rodrigues Santana</a>
- <a href="https://www.linkedin.com/in/marcelo-saadi-pessini/">Marcelo Saadi Pessini</a>
- <a href="https://www.linkedin.com/in/samuel-martins-lopes-nascimento-7a805526a/">Samuel Martins Lopes Nascimento</a>
- <a href="https://www.linkedin.com/in/thiago-goulart-de-oliveira?trk=blended-typeahead">Thiago Goulart de Oliveira</a>

## 📝 Descrição

O projeto desenvolvido pelo grupo Xpress tem como objetivo criar um pipeline de Big Data para a CPTM (Companhia Paulista de Trens Metropolitanos), permitindo a análise eficiente de grandes volumes de dados a partir de diferentes fontes, como logs operacionais e dados administrativos. A solução incluirá a coleta de dados em tempo real e em lotes, armazenamento em um Data Lake na nuvem, processamento e análise utilizando ferramentas como AWS Glue e AWS EMR, e a geração de infográficos informativos com AWS QuickSight. 

## Conteúdo do Módulo

### Sprint 1: Fundamentação e Descoberta
- **Entregáveis de Negócios**:  
  - Criação do **Canvas Proposta de Valor**.  
  - Definição de **TAM, SAM e SOM**.  
  - Construção da **Matriz de Risco**.  

- **UX**:  
  - Criação de **Persona**.  
  - Desenvolvimento do **Mapa de Jornada do Usuário**.  
  - Elaboração das **User Stories**.  

- **Descoberta de Dados**:  
  - Construção do **Data Model Canvas**.  
  - Realização de **análises exploratórias** nas tabelas.  


### Sprint 2: Design e Ingestão de Dados
- **Wireframes**:  
  - Criação e documentação dos **Wireframes**.  

- **Estruturação de Ingestão de Dados**:  
  - Desenvolvimento do **ETL** com documentação.  
  - Criação da **Arquitetura UML**.  


### Sprint 3: Automatização e Ética
- **Cubo de Dados Automatizado**:  
  - Implementação de **Views/Planilhas**.  
  - Automatização com **Prefect**.  
  - Documentação do **Cubo de Dados** (dimensões, views, automatização).  

- **Análise Ética**:  
  - Documentação da análise das **5 dimensões éticas**:  
    - Privacidade, Equidade, Transparência, Responsabilidade Social e Viés.  


### Sprint 4: Resultados e Aplicação
- **Análise Financeira**:  
  - Elaboração e documentação da **Análise Financeira**.  

- **Plano de Comunicação**:  
  - Documentação do **Plano de Comunicação**.  

- **DataApp**:  
  - Implementação dos arquivos **api.py** e **streamlit.py**.  
  - Documentação do **DataApp**.  

- **Infográfico**:  
  - Criação e documentação do **Infográfico**.
 
### Sprint 5: Conclusão fnal
- **Avaliação Final e Encerramento do Módulo.**

## 📁 Estrutura de pastas
- <b>assets</b>: aqui estão arquivos relacionados à parte gráfica do projeto, sendo eles todas as imagens utilizadas na documentação.

- <b>docs</b>: aqui está a documentação do projeto, sendo ela um arquivo tanto em markdown (`.md`), quanto em `.docx` e em `.pdf`.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto, incluindo a base de dados enviada pela empresa e um NoteBook em Jupyter.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## **Como Rodar o Projeto**

### **Pré-requisitos**  
Certifique-se de ter as seguintes dependências instaladas:  
- `Python (>= 3.8)`  
- `Poetry (gerenciador de dependências)`  
- `Streamlit`  
- `Prefect`

---

### **1º Passo: Configurar o ambiente virtual e rodar a API**  

**No Primeiro Terminal**  
1. Navegue até a pasta do projeto: 
   ```bash
   cd ./src/
2. Ative o ambiente virtual:
   ```bash
   poetry shell   
3. Execute a API:
   ```bash
   python ./dataApp/api.py

### **2º Passo: Rodar a interface no Streamlit**  

**No Segundo Terminal**  
1. Navegue novamente até a pasta do projeto:
   ```bash
   cd ./src/
2. Ative o ambiente virtual:
   ```bash
   poetry shell
3. Inicie o Streamlit:
   ```bash
   poetry run streamlit run dataApp/streamlit.py

### **3º Passo: Acessar a aplicação no navegador**  
Após iniciar os serviços, acesse a interface da aplicação pelo navegador utilizando o endereço padrão do Streamlit 
- `"http://<endereço_gerado>"`


### **Observações**  
- Certifique-se de que a API esteja rodando **antes** de iniciar o Streamlit.  
- Caso algum erro de dependência ocorra, instale novamente as dependências do projeto.  

## 📦 Histórico de Lançamentos

- **0.5.0** - 17/12/2023  
    - **Quinta entrega:** Avaliação Final e Encerramento do Módulo.

- **0.4.0** - 08/12/2023  
    - **Quarta entrega:**  
      - Análise Financeira (Documentação e PDF).  
      - Plano de Comunicação (Documentação e PDF).  
      - DataApp (api.py e streamlit.py).  
      - Documentação do DataApp.  
      - Criação de Infográfico.  

- **0.3.0** - 24/11/2023  
    - **Terceira entrega:**  
      - Cubo de Dados Automatizado.  
      - Análise de Impacto Ético.  

- **0.2.0** - 10/11/2023  
    - **Segunda entrega:**  
      - Criação de Wireframes e Documentação.  
      - Estruturação de Ingestão de Dados (ETL e Arquitetura UML).  

- **0.1.0** - 27/10/2023  
    - **Primeira entrega:**  
      - Entregável de Negócios:  
        - Canvas Proposta de Valor.  
        - TAM, SAM, SOM.  
        - Matriz de Risco.  
      - Criação de Persona, User Stories e Mapa de Jornada do Usuário.  
      - Descoberta de Dados com Data Model Canvas.  
      - Análises Exploratórias.

## 🎬 Video de Demonstração

[Aqui](https://github.com/Inteli-College/2024-2B-T10-SI08-G01/blob/main/document/docs/imgs/demonstracao.mp4)
	
## 📋 Licença/License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Inteli-College/2024-2B-T10-SI08-G01">Integração, Gerenciamento e Análise de Big Data</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/InteliProjects">Inteli</a>, <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/Inteli-College/2024-2B-T10-SI08-G01">Xpress</a>: <a href="https://www.linkedin.com/in/daniel-a-mendez-571217251/">Daniel Augusto Rivas Mendez</a>, <a href="https://www.linkedin.com/in/danielzular/">Daniel Zular</a>, <a href="https://www.linkedin.com/in/enzoboccia/">Enzo Boccia Pagliara</a>, <a href="https://www.linkedin.com/in/luizarsantana/">Luiza Rodrigues Santana/a>, <a href="https://www.linkedin.com/in/marcelo-saadi-pessini/">Marcelo Saadi Pessini</a>, <a href="https://www.linkedin.com/in/samuel-martins-lopes-nascimento-7a805526a/">Samuel Martins Lopes Nascimento</a>, <a href="https://www.linkedin.com/in/thiago-goulart-de-oliveira?trk=blended-typeahead">Thiago Goulart</a>, is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></a></p>

## 🎓 Referências

### Referências

1. **How to Learn Big Data Step by Step from Scratch in 2023?**  
   Disponível em: [https://www.projectpro.io/article/learn-big-data/695](https://www.projectpro.io/article/learn-big-data/695)  
   Acesso em: 28 out. 2023  

2. **AWS - Práticas recomendadas de arquitetura para análise e Big Data**  
   Disponível em: [https://aws.amazon.com/pt/architecture/analytics-big-data/?cards-all.sort-by=item.additionalFields.sortDate&cards-all.sort-order=desc&awsf.content-type=*all&awsf.methodology=*all](https://aws.amazon.com/pt/architecture/analytics-big-data/?cards-all.sort-by=item.additionalFields.sortDate&cards-all.sort-order=desc&awsf.content-type=*all&awsf.methodology=*all)  
   Acesso em: 5 nov. 2023  

3. **MICROSOFT - Big Data Architectures**  
   Disponível em: [https://learn.microsoft.com/en-us/azure/architecture/databases/guide/big-data-architectures](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/big-data-architectures)  
   Acesso em: 9 nov. 2023  

4. **Componentes Principais Para a Infraestrutura de Big Data**  
   Disponível em: [https://blog.dsacademy.com.br/4-componentes-principais-para-a-infraestrutura-de-big-data/](https://blog.dsacademy.com.br/4-componentes-principais-para-a-infraestrutura-de-big-data/)  
   Acesso em: 11 nov. 2023  

5. **Guia Completo do Diagrama de Arquitetura AWS**  
   Disponível em: [https://www.edrawsoft.com/pt/article/aws-architecture-diagram.html](https://www.edrawsoft.com/pt/article/aws-architecture-diagram.html)  
   Acesso em: 13 nov. 2023  


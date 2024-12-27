## Documentação do Teste da View `ocorrencias_por_manchete`

### Como Executar

1. **Navegue até `/scr`**: Navegue até onde está o código fonte do projeto utilizando o comando:

```
cd .\src\
```


2. **Instale as dependências**  
   Certifique-se de que o ambiente está configurado e as dependências necessárias estão instaladas. Use o **Poetry** para gerenciar pacotes e instale as dependências necessárias, incluindo **pytest** e **pytest-cov**, com os comandos:

   ```
   poetry install

   poetry add --dev pytest

   poetry add pytest-cov
   ```


3. **Rode os testes**  
   Para executar todos os testes unitários e verificar a funcionalidade das funções implementadas, utilize:  
   ```
   poetry run pytest
   ```  
   Esses testes verificam aspectos como execução de queries, criação de views e fluxos completos usando mocks para simular o comportamento das dependências.

4. **Verificar a cobertura de testes no terminal**  
   Para avaliar a cobertura de testes diretamente no terminal, utilize:  

     ```
     poetry run pytest --cov=tests
     ```  
    
    ou também (para verificar a cobertura de somente um arquivo)

    ```bash
     poetry run pytest --cov=test_ocorrencia_por_manchete
     ```

5. **Gere visualização de cobertura em HTML**  
   Para criar um relatório detalhado de cobertura em formato HTML:  
   - **Para o pacote completo**:  
     ```bash
     poetry run pytest --cov=tests --cov-report=html
     ```  
   Após executar os comandos acima, acesse a pasta `htmlcov` gerada e abra o arquivo `index.html` em um navegador para explorar a cobertura de testes detalhada.

6. **Gere visualização de cobertura em XML**  
    Para gerar um relatório em XML, execute:
    
    ```bash
    pytest --cov=tests --cov-report=xml
    ```
    
    Isso criará um arquivo `coverage.xml` com o relatório.


### Funções Testadas

Cada função foi validada com cenários de **caminho feliz** (sem erros) e **caminho triste** (tratamento de erros).  

- **`execute_query`**  
   - **Caminho Feliz**: Testa a execução bem-sucedida de uma query no ClickHouse.  
   - **Caminho Triste**: Valida o comportamento quando ocorre um erro na execução da query.  

- **`_create_view_ocorrencias_por_manchete`**  
   - **Caminho Feliz**: Testa a criação bem-sucedida de uma view no ClickHouse.  
   - **Caminho Triste**: Verifica o tratamento de falhas durante a criação da view.  

- **`run_ocorrencias_por_manchete`**  
   - **Caminho Feliz**: Valida o fluxo completo de criação da view sem erros.  
   - **Caminho Triste**: Testa o comportamento do fluxo completo quando ocorre uma falha.  
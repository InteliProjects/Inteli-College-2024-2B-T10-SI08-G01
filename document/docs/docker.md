# Docker

## Introdução

<p align="justify">&emsp;&emsp;Docker é uma plataforma de código aberto projetada para criar, distribuir e executar aplicações em containers. Um container é uma unidade de software leve e autossuficiente que inclui tudo o que é necessário para executar uma aplicação: código, bibliotecas, dependências e configurações. Isso garante que as aplicações funcionem de maneira consistente, independentemente do ambiente onde são implantadas. </p>

<p align="justify">&emsp;&emsp;Docker funciona criando imagens de containers, que são templates imutáveis que especificam como o container deve ser configurado. Essas imagens são baseadas em camadas, permitindo que as dependências sejam reutilizadas e compartilhadas entre diferentes containers, economizando espaço e aumentando a eficiência. </p>

<p align="justify">&emsp;&emsp;Ao usar Docker, você pode garantir que sua aplicação seja facilmente portátil entre diferentes ambientes, como máquinas locais, servidores de desenvolvimento ou ambientes de produção na nuvem. </p>

## Dockerfile

<p align="justify">&emsp;&emsp;O Dockerfile do projeto que está localizado na pasta "scr", define o ambiente necessário para executar a aplicação Python. Ele utiliza a imagem base `python:3.12-slim`, uma versão otimizada do Python 3.12, e configura o diretório de trabalho como `/src/s3_to_clickhouse_etl`. Em seguida, instala o Poetry para gerenciamento de dependências, copia os arquivos do projeto para o container, e atualiza o Poetry para sua versão mais recente. Adiciona o Flask como dependência e expõe a porta 5000 para acesso externo. Uma variável de ambiente `FLASK_APP` é configurada para apontar ao arquivo principal da aplicação, e o comando padrão `poetry run python run` é definido para iniciar a aplicação com as dependências gerenciadas pelo Poetry. </p>

## Docker-compose

<p align="justify">&emsp;&emsp;
O arquivo docker-compose.yml define e orquestra a execução de containers Docker para a aplicação s3_to_clickhouse_etl. Ele especifica que a imagem será construída a partir do Dockerfile no diretório atual, configura o nome do container, mapeia a porta 5000 do container para a porta 5000 do host, e define variáveis de ambiente, como FLASK_APP, para apontar para o arquivo principal da aplicação Flask. Além disso, o volumes permite que mudanças feitas no código local sejam refletidas no container, e o command define o comando a ser executado para iniciar a aplicação. A principal diferença entre o docker-compose.yml e o Dockerfile é que o primeiro gerencia a execução dos containers, configurando serviços, portas e volumes, enquanto o segundo define como a imagem será construída, incluindo a instalação de dependências e a configuração do ambiente da aplicação. </p>

## Diferenças entre o Dockerfile e o Docker-compose

<p align="justify">&emsp;&emsp;A principal diferença entre o `docker-compose.yml` e o `Dockerfile` é o propósito de cada um. O `Dockerfile` define como a imagem Docker será construída, incluindo a instalação de dependências, configuração do ambiente e execução de comandos dentro do container. Já o `docker-compose.yml` orquestra e gerencia a execução do container (ou containers) construídos a partir do `Dockerfile`. Enquanto o `Dockerfile` é responsável pela configuração e construção do ambiente da aplicação, o `docker-compose.yml` é usado para definir como a aplicação será executada, incluindo serviços, volumes, portas e variáveis de ambiente.
 </p>

## Conclusão

<p align="justify">&emsp;&emsp;O uso do Docker na sua solução simplifica o processo de desenvolvimento, implantação e manutenção, encapsulando a aplicação e suas dependências em um ambiente isolado e portátil, garantindo consistência em diferentes ambientes. O Dockerfile demonstra boas práticas quando utiliza uma imagem base leve (slim), gerencia as dependências com o Poetry e expõe a aplicação na porta correta, tornando sua aplicação pronta para ser executada em qualquer ambiente compatível com Docker, promovendo eficiência e confiabilidade na entrega do software. </p>
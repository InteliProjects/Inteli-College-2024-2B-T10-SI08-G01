# Relatório do Data App - Sprint Final

## Sumário
1. [Introdução](#introdução)
2. [A Importância do Streamlit](#a-importância-do-streamlit)
3. [Mudanças na Sprint 4](#mudanças-na-sprint-4)
4. [Mudanças na Sprint 5](#mudanças-na-sprint-5)
5. [Imagens do Sistema](#imagens-do-sistema)
6. [Melhorias Planejadas para o Futuro](#melhorias-planejadas-para-o-futuro)

---

## Introdução
O **Data App** é uma aplicação interativa projetada para facilitar a análise de dados de ocorrências e falhas. A aplicação utiliza o **Flask** como backend, que conecta-se ao banco de dados **ClickHouse**, enquanto o frontend é desenvolvido no **Streamlit**. O objetivo principal é fornecer insights precisos e visuais para apoiar a tomada de decisões.

---

## A Importância do Streamlit
O **Streamlit** foi escolhido como a principal tecnologia de frontend devido a:

- **Desenvolvimento rápido**: Criação intuitiva de dashboards interativos.
- **Suporte a bibliotecas populares**: Como Pandas, Plotly e Matplotlib.
- **Acessibilidade**: Oferece uma interface fácil para o acesso aos dados em tempo real.

---

## Mudanças na Sprint 4
As seguintes mudanças foram realizadas na **Sprint 4**:

### Backend:
- Criação de rotas na API para integração com o **ClickHouse**:
  - `/api/ocorrencias_por_manchete/<limit>`
  - `/api/falhas_por_causa/<limit>`
  - `/api/ocorrencias_por_horario/<hora_inicio>/<hora_fim>`

### Frontend no Streamlit:
- Implementação das seções principais:
  - **Início**: Exibição de métricas do dia, como total de falhas e ocorrências.
  - **Ocorrências**: Gráficos interativos mostrando dados por horário, manchete e trecho.
  - **Falhas**: Visualização de falhas por causa e equipamento.

### Configuração do Ambiente:
- Criação do arquivo **.env** para proteger credenciais do **ClickHouse** e **AWS**.
- Scripts **ETL** atualizados para integração com serviços **AWS**.

---

## Mudanças na Sprint 5
Nesta última sprint, as seguintes melhorias e adições foram implementadas:

### Novas views no backend:
- Implementação das rotas:
  - `/api/ocorrencias_por_dia/<data>`
  - `/api/falhas_por_dia/<data>`

### Tela de Login:
- Adição de uma interface simples para autenticação básica de usuários.
- Controle de acesso às seções do dashboard.

### Atualizações no frontend:
- **Dashboard principal** agora inclui gráficos interativos agregados por dia para ocorrências e falhas.
- Integração das novas views com o frontend.

### Refinamento de ambiente:
- Scripts **ETL** ajustados para processar dados diários de ocorrências e falhas.

---

## Imagens do Sistema
### Tela de Login
<p align="center">
    <img src="https://res.cloudinary.com/dp4liildh/image/upload/v1734449525/WhatsApp_Image_2024-12-17_at_12.30.50_xz8egd.jpg" 
         alt="Inteli - Instituto de Tecnologia e Liderança" 
         style="border:0; max-width:100%; height:auto;">
  </a>
</p>
*Nova tela de login com autenticação de usuário.*

### Tela Inicial
![Tela Inicial](caminho-para-imagem-inicial)
*A tela inicial exibe as métricas do dia, permitindo um overview rápido das falhas e ocorrências.*

### Tela de Ocorrências
![Tela de Ocorrências](caminho-para-imagem-ocorrencias)
*Gráfico interativo mostrando ocorrências por horário e manchete.*

### Tela de Falhas
![Tela de Falhas](caminho-para-imagem-falhas)
*Visualização detalhada das falhas por causa e equipamento.*

---

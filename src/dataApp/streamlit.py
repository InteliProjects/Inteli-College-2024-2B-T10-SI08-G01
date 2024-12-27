import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_credentials_auth():
    credentials_auth = os.getenv("CREDENTIALS")
    try:
        return json.loads(credentials_auth) if credentials_auth else {}
    except json.JSONDecodeError as e:
        st.error(f"Não pode realizar autenticação: {e}")
        return {}

def login_user(username, password, credentials):
    user_data = credentials.get(username)
    return user_data and user_data.get("password") == password

class DataApp:
    def __init__(self):
        self.api_url = "http://localhost:5000/api"
        self.authenticated = False
        self.credentials = get_credentials_auth().get("credentials", {}).get("users", {})

    def pagina_login(self):
        st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("Usuário")
                password = st.text_input("Senha", type="password")
                login_button = st.form_submit_button("Entrar")
                if login_button:
                    if login_user(username, password, self.credentials):
                        st.session_state['username'] = username
                        st.session_state['login_successful'] = True
                        self.authenticated = True
                        st.success("Login reaizado com sucesso!")
                    else:
                        st.error("Usuário ou senha incorretos.")

    def main(self):
        st.set_page_config(page_title="Xpress")
        if 'username' not in st.session_state or not st.session_state.get("login_successful", False):
            self.pagina_login()
        else:
            self.show_main_content()

    def show_main_content(self):
        tab1, tab2, tab3, tab4 = st.tabs(["Início", "Ocorrências", "Falhas", "Infográfico"])
        with tab1:
            self.pagina_inicial()
        with tab2:
            self.pagina_ocorrencias()
        with tab3:
            self.pagina_falhas()
        with tab4:
            self.pagina_infografico()

    def pagina_infografico(self):
        st.title("Infográfico")
        st.image("https://res.cloudinary.com/ddhxypadw/image/upload/v1733491550/Por_dentro_dos_trilhos_q6ddbq.png", caption="Infográfico de Ocorrências e Falhas", use_container_width=True)

    def pagina_inicial(self):
        st.title("Ocorrências e Falhas")
        
        col1, col2 = st.columns(2)

        with col1:
            try:
                response = requests.get(f"{self.api_url}/falhas_por_dia")
                if response.status_code == 200:
                    dados = response.json()["data"]
                    if dados:
                        st.metric("Total de Falhas", dados[0]["Quantidade_Falhas"])
                        st.caption(f"Data: {dados[0]['Data']}")
            except Exception as e:
                st.error(f"Erro ao buscar falhas: {str(e)}")

        with col2:
            try:
                response = requests.get(f"{self.api_url}/ocorrencias_por_dia")
                if response.status_code == 200:
                    dados = response.json()["data"]
                    if dados:
                        st.metric("Total de Ocorrências", dados[0]["Quantidade_Ocorrencias"])
                        st.caption(f"Data: {dados[0]['Data']}")
            except Exception as e:
                st.error(f"Erro ao buscar ocorrências: {str(e)}")

        st.write("""
        ### Sobre o Projeto Xpress

        O projeto Xpress oferece uma solução avançada de análise de Big Data para a Companhia Paulista de Trens Metropolitanos (CPTM). 
        Nosso objetivo é transformar a maneira como os dados operacionais e administrativos são processados, armazenados e visualizados, 
        utilizando tecnologias de ponta. Nesse sentido, este projeto melhora tanto as operações diárias como também fortalece a capacidade estratégica da CPTM 
        através do uso inteligente dos dados.

        #### Conteúdo das Páginas:
        - **Início**: Visão geral do projeto e métricas principais de falhas e ocorrências.
        - **Ocorrências**: Análises detalhadas de ocorrências por hora, manchete e trecho, incluindo uma nuvem de palavras.
        - **Falhas**: Informações sobre falhas por causa e equipamento, com gráficos interativos.
        - **Infográfico**: Visualização completa das informações em um infográfico de modo mais lúdico.
        """)


    def pagina_ocorrencias(self):
        st.title("Análise de Ocorrências")
        
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("Data Início", value=pd.to_datetime('2019-01-01'))
        with col2:
            data_fim = st.date_input("Data Fim", value=pd.to_datetime('today'))

        st.subheader("Ocorrências por Manchete")
        
        try:
            response = requests.get(f"{self.api_url}/todas_manchetes")
            if response.status_code == 200:
                todas_manchetes = [m["Manchete"] for m in response.json()["data"]]
                manchetes_selecionadas = st.multiselect(
                    "Selecione as manchetes",
                    options=todas_manchetes,
                    default=todas_manchetes[:5] if len(todas_manchetes) > 5 else todas_manchetes
                )
                
                params = {
                    'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                    'data_fim': data_fim.strftime('%Y-%m-%d'),
                    'manchetes': manchetes_selecionadas
                }
                
                response = requests.get(f"{self.api_url}/ocorrencias_por_manchete", params=params)
                if response.status_code == 200:
                    dados = response.json()["data"]
                    if dados:
                        fig = px.bar(
                            dados,
                            x='Manchete',
                            y='Quantidade_Ocorrencias',
                            title='Ocorrências por Manchete'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Nenhum dado encontrado para os filtros selecionados")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")



        st.subheader("Ocorrências por Trecho")
        qtd_trechos = st.slider(
            "Quantidade de trechos",
            min_value=5,
            max_value=20,
            value=10,
            key="trechos_slider"
        )
        try:
            response = requests.get(f"{self.api_url}/ocorrencias_por_trecho/{qtd_trechos}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='Trecho', y='Quantidade_Ocorrencias', color='Tipo_Trecho')
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar dados por trecho: {str(e)}")

        st.subheader("Ocorrências por Dia")
        qtd_dias = st.slider(
            "Quantidade de dias",
            min_value=5,
            max_value=20,
            value=10,
            key="ocorrencias_dias_slider"
        )

        try:
            response = requests.get(f"{self.api_url}/ocorrencias_por_dia/{qtd_dias}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='Data', y='Quantidade_Ocorrencias')
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar ocorrências por dia: {str(e)}")

        st.subheader("Ocorrências por Descrição")
        qtd_descricao = st.slider(
            "Quantidade de descrições",
            min_value=5,
            max_value=20,
            value=10,
            key="ocorrencias_descricao_slider"
        )

        try:
            response = requests.get(f"{self.api_url}/ocorrencias_por_descricao/{qtd_descricao}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='Descricao', y='Quantidade_Ocorrencias')
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar ocorrências por descrição: {str(e)}")

    def pagina_falhas(self):
        st.title("Falhas")
        st.subheader("Falhas por Causa")
        qtd_causas = st.slider(
            "Quantidade de causas",
            min_value=5,
            max_value=20,
            value=10
        )
        try:
            response = requests.get(f"{self.api_url}/falhas_por_causa/{qtd_causas}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='Causa', y='Quantidade_Falhas')
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar falhas por causa: {str(e)}")

        st.subheader("Falhas por Equipamento")
        qtd_equipamentos = st.slider(
            "Quantidade de equipamentos",
            min_value=5,
            max_value=20,
            value=10,
            key="equipamentos_slider"
        )
        try:
            response = requests.get(f"{self.api_url}/falhas_por_equipamento/{qtd_equipamentos}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='ID_Equipamento', y='Quantidade_Falhas')
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar falhas por equipamento: {str(e)}")

        st.subheader("Falhas por Dia")
        qtd_dias = st.slider(
            "Quantidade de dias",
            min_value=5,
            max_value=20,
            value=10,
            key="falhas_dias_slider"
        )

        try:
            response = requests.get(f"{self.api_url}/falhas_por_dia/{qtd_dias}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='Data', y='Quantidade_Falhas')
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar falhas por dia: {str(e)}")

        st.subheader("Falhas por Descrição")
        qtd_descricao = st.slider(
            "Quantidade de descrições",
            min_value=5,
            max_value=20,
            value=10,
            key="falhas_descricao_slider"
        )

        try:
            response = requests.get(f"{self.api_url}/falhas_por_descricao/{qtd_descricao}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='Descricao', y='Quantidade_Falhas')
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar falhas por descrição: {str(e)}")

        st.subheader("Falhas por Localidade")
        qtd_localidade = st.slider(
            "Quantidade de localidades",
            min_value=5,
            max_value=20,
            value=10,
            key="falhas_localidade_slider"
        )

        try:
            response = requests.get(f"{self.api_url}/falhas_por_localidade/{qtd_localidade}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='Localidade', y='Quantidade_Falhas')
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar falhas por localidade: {str(e)}")

        st.subheader("Falhas por Horário")
        col1, col2 = st.columns(2)
        with col1:
            hora_inicio = st.number_input("Hora Início", 0, 23, 0, key="falhas_hora_inicio")
        with col2:
            hora_fim = st.number_input("Hora Fim", 0, 23, 23, key="falhas_hora_fim")
            
        try:
            response = requests.get(f"{self.api_url}/falhas_por_horario/{hora_inicio}/{hora_fim}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.line(df, x='Horario', y='Quantidade_Falhas')
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar falhas por horário: {str(e)}")

        st.subheader("Falhas por Situação")
        qtd_situacao = st.slider(
            "Quantidade de situações",
            min_value=5,
            max_value=20,
            value=10,
            key="falhas_situacao_slider"
        )

        try:
            response = requests.get(f"{self.api_url}/falhas_por_situacao/{qtd_situacao}")
            if response.status_code == 200:
                dados = response.json()["data"]
                if dados:
                    df = pd.DataFrame(dados)
                    fig = px.bar(df, x='Situacao', y='Quantidade_Falhas')
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao buscar falhas por situação: {str(e)}")

if __name__ == "__main__":
    app = DataApp()
    app.main()
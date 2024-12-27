from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    AWS_SESSION_TOKEN: str
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

settings = Settings()

class DataOcorrencias(BaseModel):
    Class_Manchete: str
    Classificacao_Manchete: str
    Data_Atualizacao: float
    Data_Normalizacao: str
    Desc_Ocorrencia: str
    Eventos_Relacionados: float
    Fl_Estimados: int
    Flag_Controle: str
    Hora_Ocorrencia: str
    Id_Datanormalizacao: float
    Id_Dataocorrencia: int
    Id_Localidade: int
    Id_Sic_Classificacao: int
    Id_Tipo_Relevancia: float
    Manchete: str
    Nr_Acoes: float
    Pass_Estimados: int
    Sic_Id_Ocorrencia: int
    Sic_Id_Ocorrencia_3: int
    Total_Ajustes: int
    Trecho: str
    Tx_Tipo_Relevancia: str
    Tx_Trem: float

class DataFalhas(BaseModel):
    NR_SAF: str
    NR_ANO: str
    ID_CCO_SAF: str
    ID_FT_FALHA: str
    ID_DT_FALHA: str
    ID_DT_FALHA_LIBERADO: str
    TEMPO_LIBERACAO: float
    HORA_FALHA: float
    LOCALIDADE: str
    TRECHO: str
    AVARIA: str
    SISTEMA: str
    ATUACAO: str
    CAUSA: str
    DESC_AVARIA: str
    DESC_CAUSA: str
    DESC_ATUACAO: str
    SITUACAO_FALHA: str
    ID_HORA: str
    FL_EQUIPAMENTO_DISP: str
    TEMPO_REPARO_LIB: float
    TEMPO_REPARO_TOTAL: float
    TX_POSICAO_FALHA: str
    TX_POSICAO_OSM: str
    TX_CARRO_AVAR_FALHA: str
    TX_CARRO_AVAR_OSM: str
    TX_CARRO_COMANDO_FALHA: str
    TX_CARRO_COMANDO_OSM: str
    TX_COMPOSICAO_FALHA: str
    TX_COMPOSICAO_OSM: str
    TEMPO_ATENDIMENTO: float
    AGENTE_CAUSADOR: str
    ID_NIVEL: str
    DT_TERMINO_INTERVENCAO: str
    DT_MODIFICACAO: str
    TX_LOCAL_FIM: str
    TX_LOCAL_INI: str
    TEMPO_INDISPONIVEL: float
    HORA_LIBERADO_FALHA: float
    DIM_EQUIP_TAG_SK: str
    ID_EQUIPAMENTO: str
    ID_GARANTIA: str
    TX_GARANTIA: str
    TEMPO_ATENDIMENTO_2: float
    TEMPO_INDISPONIVEL_2: float
    TEMPO_LIBERACAO_2: float
    TEMPO_REPARO_LIB_2: str
    TEMPO_REPARO_TOTAL_2: float
    NR_TEMPO_ACESSO: float
    DIM_ATUACAO_SK: float
    FALHA_S_EM_DATA: int
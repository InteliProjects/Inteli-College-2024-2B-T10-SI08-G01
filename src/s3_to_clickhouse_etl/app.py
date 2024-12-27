from flask import Flask, send_file
from flasgger import Swagger
from etlbronze.ingest import DataIngestionService
from views.ocorrencias_por_horario import OcorrenciasPorHorario
from views.ocorrencias_por_manchete import OcorrenciasPorManchete
from views.falhas_por_causa import FalhasPorCausa
from views.falhas_por_id_equipamento import FalhasPorIdEquipamento
from views.falhas_por_trecho_etl import FalhasPorTrecho
from views.ocorrencias_por_trecho import OcorrenciasPorTrecho
from views.ocorrencias_por_dia import OcorrenciasPorDia
from views.falhas_por_dia import FalhasPorDia
from views.ocorrencias_por_descricao import OcorrenciasPorDescricao
from views.falhas_por_descricao import FalhasPorDescricao
from views.falhas_por_localidade import FalhasPorLocalidade
from views.falhas_por_horario import FalhasPorHorario
from views.falhas_por_situacao import FalhasPorSituacao


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/ingest_data', methods=['GET'])
def start_ingestion():
  """
  Iniciar o processo para ingestão de dados
  ---
  tags:
    - Processo de ETL Bronze
  responses:
    200:
    description: Dados inseridos com sucesso no ClickHouse e métricas registradas no PostgreSQL!
    500:
    description: Erro ao executar o processo de ingestão de dados.
  """
  try:
    ingest_data = DataIngestionService()
    ingest_data.run_ingest_data()
    return "Dados inseridos com sucesso no ClickHouse e métricas registradas no PostgreSQL!", 200
  except Exception as e:
    return f"Erro ao executar o processo de ingestão de dados: {e}", 500

@app.route('/view_ocorrencias_por_horario', methods=['GET'])
def start_ocorrencias_por_horario():
  """
  Iniciar o processo para criar views de ocorrências por horário.
  ---
  tags:
    - View Ocorrências por Horário
  responses:
    200:
    description: Processo de ETL para ocorrências por horário iniciado com sucesso!
    500:
    description: Erro ao executar o processo para ocorrências por horário.
  """
  try:
    ocorrencias_por_horario = OcorrenciasPorHorario()
    ocorrencias_por_horario.run_ocorrencias_por_horario()
    return "Processo de ETL para ocorrências por horário finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para ocorrências por horário: {e}", 500

@app.route('/view_ocorrencias_por_manchete', methods=['GET'])
def view_ocorrencias_por_manchete():
  """
  Iniciar o processo para criar views de Ocorrências por Manchete
  ---
  tags:
    - View Ocorrências por Manchete
  responses:
    200:
    description: View de Ocorrências por Manchete executado com sucesso!
    500:
    description: Erro ao executar o View de Ocorrências por Manchete.
  """
  try:
    ocorrencias_por_manchete = OcorrenciasPorManchete()
    ocorrencias_por_manchete.run_ocorrencias_por_manchete()
    return "View de Ocorrências por Manchete executado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o View de Ocorrências por Manchete: {e}", 500

@app.route('/view_falhas_por_causa', methods=['GET'])
def ingest_falhas_por_causa():
  """
  Iniciar o processo para criar views de Falhas por Causa
  ---
  tags:
    - View Falhas por Causa
  responses:
    200:
    description: ETL de Falhas por Causa executado com sucesso!
    500:
    description: Erro ao executar ETL de Falhas por Causa.
  """
  try:
    falhas_por_causa = FalhasPorCausa()
    falhas_por_causa.run_falhas_por_causa()
    return "ETL de Falhas por Causa executado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar ETL de Falhas por Causa: {e}", 500

@app.route('/view_falhas_por_id_equipamento', methods=['GET'])
def ingest_falhas_por_id_equipamento():
  """
  Iniciar o processo para criar views de Falhas por ID_EQUIPAMENTO
  ---
  tags:
    - View Falhas por ID_EQUIPAMENTO
  responses:
    200:
    description: ETL de Falhas por ID_EQUIPAMENTO executado com sucesso!
    500:
    description: Erro ao executar ETL de Falhas por ID_EQUIPAMENTO.
  """
  try:
    falhas_por_id_equipamento = FalhasPorIdEquipamento()
    falhas_por_id_equipamento.run_falhas_por_id_equipamento()
    return "ETL de Falhas por ID_EQUIPAMENTO executado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar ETL de Falhas por ID_EQUIPAMENTO: {e}", 500

@app.route('/view_falhas_por_trecho', methods=['GET'])
def start_falhas_por_trecho():
  """
  Iniciar o processo para criar views de falhas por trecho.
  ---
  tags:
    - View Falhas por Trecho
  responses:
    200:
    description: Processo de ETL para falhas por trecho iniciado com sucesso!
    500:
    description: Erro ao executar o processo para falhas por trecho.
  """
  try:
    falhas_por_trecho = FalhasPorTrecho()
    falhas_por_trecho.run_falhas_por_trecho()
    return "Processo de ETL para falhas por trecho finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para falhas por trecho: {e}", 500

@app.route('/view_ocorrencias_por_trecho', methods=['GET'])
def start_ocorrencias_por_trecho():
  """
  Iniciar o processo para criar views de ocorrências por trecho.
  ---
  tags:
    - View Ocorrências por Trecho
  responses:
    200:
    description: Processo de ETL para ocorrências por trecho iniciado com sucesso!
    500:
    description: Erro ao executar o processo para ocorrências por trecho.
  """
  try:
    ocorrencias_por_trecho = OcorrenciasPorTrecho()
    ocorrencias_por_trecho.run_ocorrencias_por_trecho()
    return "Processo de ETL para ocorrências por trecho finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para ocorrências por trecho: {e}", 500

@app.route('/view_ocorrencias_por_dia', methods=['GET'])
def start_ocorrencias_por_dia():
  """
  Iniciar o processo para criar views de ocorrências por dia.
  ---
  tags:
    - View Ocorrências por Dia
  responses:
    200:
    description: Processo de ETL para ocorrências por dia iniciado com sucesso!
    500:
    description: Erro ao executar o processo para ocorrências por dia.
  """
  try:
    ocorrencias_por_dia = OcorrenciasPorDia()
    ocorrencias_por_dia.run_ocorrencias_por_dia()
    return "Processo de ETL para ocorrências por dia finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para ocorrências por dia: {e}", 500

@app.route('/view_falhas_por_dia', methods=['GET'])
def start_falhas_por_dia():
  """
  Iniciar o processo para criar views de falhas por dia.
  ---
  tags:
    - View Falhas por Dia
  responses:
    200:
    description: Processo de ETL para falhas por dia iniciado com sucesso!
    500:
    description: Erro ao executar o processo para falhas por dia.
  """
  try:
    falhas_por_dia = FalhasPorDia()
    falhas_por_dia.run_falhas_por_dia()
    return "Processo de ETL para falhas por dia finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para falhas por dia: {e}", 500

@app.route('/view_ocorrencias_por_descricao', methods=['GET'])
def start_ocorrencias_por_descricao():
  """
  Iniciar o processo para criar views de ocorrências por descrição.
  ---
  tags:
    - View Ocorrências por Descrição
  responses:
    200:
    description: Processo de ETL para ocorrências por descrição iniciado com sucesso!
    500:
    description: Erro ao executar o processo para ocorrências por descrição.
  """
  try:
    ocorrencias_por_descricao = OcorrenciasPorDescricao()
    ocorrencias_por_descricao.run_ocorrencias_por_descricao()
    return "Processo de ETL para ocorrências por descrição finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para ocorrências por descrição: {e}", 500
  
@app.route('/view_falhas_por_descricao', methods=['GET'])
def start_falhas_por_descricao():
  """
  Iniciar o processo para criar views de falhas por descrição.
  ---
  tags:
    - View Falhas por Descrição
  responses:
    200:
    description: Processo de ETL para falhas por descrição iniciado com sucesso!
    500:
    description: Erro ao executar o processo para falhas por descrição.
  """
  try:
    falhas_por_descricao = FalhasPorDescricao()
    falhas_por_descricao.run_falhas_por_descricao()
    return "Processo de ETL para falhas por descrição finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para falhas por descrição: {e}", 500
  
@app.route('/view_falhas_por_localidade', methods=['GET'])
def start_falhas_por_localidade():
  """
  Iniciar o processo para criar views de falhas por localidade.
  ---
  tags:
    - View Falhas por Localidade
  responses:
  200:
  description: Processo de ETL para falhas por localidade iniciado com sucesso!
  500:
  description: Erro ao executar o processo para falhas por localidade.
  """
  try:
    falhas_por_localidade = FalhasPorLocalidade()
    falhas_por_localidade.run_falhas_por_localidade()
    return "Processo de ETL para falhas por localidade finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para falhas por localidade: {e}", 500
  
@app.route('/view_falhas_por_horario', methods=['GET'])
def start_falhas_por_horario():
  """
  Iniciar o processo para criar views de falhas por horário.
  ---
  tags:
    - View Falhas por Horário
  responses:
    200:
    description: Processo de ETL para falhas por horário iniciado com sucesso!
    500:
    description: Erro ao executar o processo para falhas por horário.
  """
  try:
    falhas_por_horario = FalhasPorHorario()
    falhas_por_horario.run_falhas_por_horario()
    return "Processo de ETL para falhas por horário finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para falhas por horário: {e}", 500
  
@app.route('/view_falhas_por_situacao', methods=['GET'])
def start_falhas_por_situacao():
  """
  Iniciar o processo para criar views de falhas por situação.
  ---
  tags:
    - View Falhas por Situação
  responses:
    200:
    description: Processo de ETL para falhas por situação iniciado com sucesso!
    500:
    description: Erro ao executar o processo para falhas por situação.
  """
  try:
    falhas_por_situacao = FalhasPorSituacao()
    falhas_por_situacao.run_falhas_por_situacao()
    return "Processo de ETL para falhas por situação finalizado com sucesso!", 200
  except Exception as e:
    return f"Erro ao executar o processo para falhas por situação: {e}", 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)

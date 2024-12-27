import os
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from clickhouse_driver import Client
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)

class ClickHouseService:
    def __init__(self):
        self.client = Client(
            host=os.getenv("CLICKHOUSE_HOST"),
            port=int(os.getenv("CLICKHOUSE_PORT")),
            user=os.getenv("CLICKHOUSE_USER"),
            password=os.getenv("CLICKHOUSE_PASSWORD")
        )

    def get_ocorrencias_por_manchete(self, data_inicio, data_fim, manchetes=None):
        manchetes_condition = ""
        if manchetes and len(manchetes) > 0:
            manchetes_str = "', '".join(manchetes)
            manchetes_condition = f"AND Manchete IN ('{manchetes_str}')"
        
        query = f"""
        SELECT Manchete, Quantidade_Ocorrencias 
        FROM grupo1.view_ocorrencias_por_manchete
        WHERE DataOcorrencia BETWEEN '{data_inicio}' AND '{data_fim}'
        {manchetes_condition}
        ORDER BY Quantidade_Ocorrencias DESC
        """
        return self.client.execute(query)

    def get_todas_manchetes(self):
        query = """
        SELECT DISTINCT Manchete
        FROM grupo1.view_ocorrencias_por_manchete
        ORDER BY Manchete
        """
        return self.client.execute(query)


    def get_falhas_por_causa(self, limit):
        query = f"""
         SELECT 
             Causa,
             total_falhas as Quantidade_Falhas
         FROM grupo1.view_falhas_por_causa
         WHERE Causa != 'N/A'
         ORDER BY Quantidade_Falhas DESC
         LIMIT {limit}
         """
        return self.client.execute(query)

    def get_falhas_por_equipamento(self, limit):
        query = f"""
         SELECT 
             ID_EQUIPAMENTO,
             total_falhas as Quantidade_Falhas
         FROM grupo1.view_falhas_por_id_equipamento
         WHERE total_falhas < (
             SELECT MAX(total_falhas) 
             FROM grupo1.view_falhas_por_id_equipamento
         )
         ORDER BY Quantidade_Falhas DESC
         LIMIT {limit}
         """
        return self.client.execute(query)

    def get_ocorrencias_por_horario(self, hora_inicio, hora_fim):
        query = f"""
        SELECT 
            Horario,
            total_ocorrencias as Quantidade_Ocorrencias
        FROM grupo1.ocorrencias_por_horario
        WHERE Horario BETWEEN {hora_inicio} AND {hora_fim}
        ORDER BY Horario
        """
        return self.client.execute(query)

    def get_ocorrencias_por_trecho(self, limit):
        query = f"""
        SELECT 
            Trecho,
            total_ocorrencias as Quantidade_Ocorrencias,
            tipo_trecho
        FROM grupo1.view_ocorrencias_com_tipo
        WHERE total_ocorrencias < (
            SELECT MAX(total_ocorrencias) 
            FROM grupo1.view_ocorrencias_com_tipo
        )
        ORDER BY Quantidade_Ocorrencias DESC
        LIMIT {limit}
        """
        return self.client.execute(query)

    def get_falhas_por_trecho(self, limit):
        query = f"""
        SELECT 
            Trecho,
            total_falhas as Quantidade_Falhas
        FROM grupo1.falhas_por_trecho
        ORDER BY Quantidade_Falhas DESC
        LIMIT {limit}
        """
        return self.client.execute(query)

    def get_ocorrencias_por_dia(self):
        query = """
        SELECT data_ocorrencia AS Data, total_ocorrencias AS Quantidade_Ocorrencias 
        FROM grupo1.ocorrencias_por_dia 
        WHERE data_ocorrencia IS NOT NULL 
        AND data_ocorrencia != toDate('1970-01-01')
        ORDER BY Data DESC
        LIMIT 1
        """
        return self.client.execute(query)

    def get_ocorrencias_por_descricao(self, limit):
        query = f"""
        SELECT 
            Descricao,
            DataOcorrencia AS Data,
            Quantidade_Ocorrencias
        FROM grupo1.view_ocorrencias_por_descricao
        ORDER BY Quantidade_Ocorrencias DESC
        LIMIT {limit}
        """
        return self.client.execute(query)

    def get_falhas_por_dia(self):
        query = """
        SELECT data_falha AS Data, total_falhas AS Quantidade_Falhas 
        FROM grupo1.falhas_por_dia 
        WHERE data_falha IS NOT NULL 
        AND data_falha != toDate('1970-01-01')
        ORDER BY Data DESC
        LIMIT 1
        """
        return self.client.execute(query)

    def get_falhas_por_descricao(self, limit):
        query = f"""
        SELECT 
            Descricao,
            DataFalha AS Data,
            total_falhas AS Quantidade_Falhas
        FROM grupo1.view_falhas_por_descricao
        ORDER BY Quantidade_Falhas DESC
        LIMIT {limit}
        """
        return self.client.execute(query)

    def get_falhas_por_localidade(self, limit):
        query = f"""
        SELECT 
            Localidade,
            DataFalha AS Data,
            total_falhas AS Quantidade_Falhas
        FROM grupo1.view_falhas_por_localidade
        ORDER BY Quantidade_Falhas DESC
        LIMIT {limit}
        """
        return self.client.execute(query)

    def get_falhas_por_horario(self, hora_inicio, hora_fim):
        query = f"""
        SELECT 
            Horario,
            DataFalha AS Data,
            total_falhas AS Quantidade_Falhas
        FROM grupo1.falhas_por_horario
        WHERE Horario BETWEEN {hora_inicio} AND {hora_fim}
        ORDER BY Horario
        """
        return self.client.execute(query)

    def get_falhas_por_situacao(self, limit):
        query = f"""
        SELECT 
            Situacao,
            DataFalha AS Data,
            total_falhas AS Quantidade_Falhas
        FROM grupo1.falhas_por_situacao
        ORDER BY Quantidade_Falhas DESC
        LIMIT {limit}
        """
        return self.client.execute(query)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        expected_token = os.getenv('API_TOKEN')

        if not expected_token:
            return jsonify({'message': 'Token não configurado no servidor'}), 500

        if expected_token != 'xpress123':  
            return jsonify({'message': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorated
@app.route('/api/ocorrencias_por_manchete', methods=['GET'])
@token_required
def get_ocorrencias_manchete():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    manchetes = request.args.getlist('manchetes')
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_ocorrencias_por_manchete(data_inicio, data_fim, manchetes)
        return jsonify({
            "data": [{"Manchete": manchete, "Quantidade_Ocorrencias": qtd} 
                    for manchete, qtd in dados]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todas_manchetes', methods=['GET'])
@token_required
def get_todas_manchetes():
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_todas_manchetes()
        return jsonify({
            "data": [{"Manchete": manchete} for manchete, in dados]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

@app.route('/api/falhas_por_causa/<int:limit>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'limit',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Quantidade de causas a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de falhas por causa'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_falhas_causa(limit):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_falhas_por_causa(limit)
        return jsonify({
            "data": [
                {"Causa": causa, "Quantidade_Falhas": qtd} 
                for causa, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/falhas_por_equipamento/<int:limit>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'limit',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Quantidade de equipamentos a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de falhas por equipamento'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_falhas_equipamento(limit):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_falhas_por_equipamento(limit)
        return jsonify({
            "data": [
                {"ID_Equipamento": id_eq, "Quantidade_Falhas": qtd} 
                for id_eq, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ocorrencias_por_horario/<int:hora_inicio>/<int:hora_fim>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'hora_inicio',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Hora inicial (0-23)'
        },
        {
            'name': 'hora_fim',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Hora final (0-23)'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de ocorrências por horário'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_ocorrencias_horario(hora_inicio, hora_fim):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_ocorrencias_por_horario(hora_inicio, hora_fim)
        return jsonify({
            "data": [
                {"Hora": hora, "Quantidade_Ocorrencias": qtd} 
                for hora, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ocorrencias_por_trecho/<int:limit>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'limit',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Quantidade de trechos a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de ocorrências por trecho'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_ocorrencias_trecho(limit):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_ocorrencias_por_trecho(limit)
        return jsonify({
            "data": [
                {
                    "Trecho": trecho, 
                    "Quantidade_Ocorrencias": qtd,
                    "Tipo_Trecho": tipo
                } 
                for trecho, qtd, tipo in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/falhas_por_trecho/<int:limit>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'limit',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Quantidade de trechos a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de falhas por trecho'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_falhas_trecho(limit):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_falhas_por_trecho(limit)
        return jsonify({
            "data": [
                {"Trecho": trecho, "Quantidade_Falhas": qtd} 
                for trecho, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/ocorrencias_por_dia', methods=['GET'])
@token_required
@swag_from({
    'responses': {
        200: {'description': 'Ocorrências do último dia'},
        401: {'description': 'Token inválido'}
    }
})
def get_ocorrencias_dia():
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_ocorrencias_por_dia()
        return jsonify({
            "data": [{"Data": data, "Quantidade_Ocorrencias": qtd} for data, qtd in dados]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/ocorrencias_por_descricao/<int:limit>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'limit',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Quantidade de ocorrências por descrição a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de ocorrências por descrição'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_ocorrencias_descricao(limit):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_ocorrencias_por_descricao(limit)
        return jsonify({
            "data": [
                {"Descricao": desc, "Data": data, "Quantidade_Ocorrencias": qtd} 
                for desc, data, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/falhas_por_dia', methods=['GET'])
@token_required
@swag_from({
    'responses': {
        200: {'description': 'Falhas do último dia'},
        401: {'description': 'Token inválido'}
    }
})
def get_falhas_dia():
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_falhas_por_dia()
        return jsonify({
            "data": [{"Data": data, "Quantidade_Falhas": qtd} for data, qtd in dados]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/falhas_por_descricao/<int:limit>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'limit',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Quantidade de falhas por descrição a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de falhas por descrição'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_falhas_descricao(limit):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_falhas_por_descricao(limit)
        return jsonify({
            "data": [
                {"Descricao": desc, "Data": data, "Quantidade_Falhas": qtd} 
                for desc, data, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/falhas_por_localidade/<int:limit>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'limit',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Quantidade de falhas por localidade a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de falhas por localidade'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_falhas_localidade(limit):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_falhas_por_localidade(limit)
        return jsonify({
            "data": [
                {"Localidade": localidade, "Data": data, "Quantidade_Falhas": qtd} 
                for localidade, data, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/falhas_por_horario/<int:hora_inicio>/<int:hora_fim>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'hora_inicio',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Hora inicial (0-23)'
        },
        {
            'name': 'hora_fim',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Hora final (0-23)'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de falhas por horário'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_falhas_horario(hora_inicio, hora_fim):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_falhas_por_horario(hora_inicio, hora_fim)
        return jsonify({
            "data": [
                {"Horario": horario, "Data": data, "Quantidade_Falhas": qtd} 
                for horario, data, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/falhas_por_situacao/<int:limit>', methods=['GET'])
@token_required
@swag_from({
    'parameters': [
        {
            'name': 'limit',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Quantidade de falhas por situação a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de falhas por situação'
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def get_falhas_situacao(limit):
    try:
        clickhouse = ClickHouseService()
        dados = clickhouse.get_falhas_por_situacao(limit)
        return jsonify({
            "data": [
                {"Situacao": situacao, "Data": data, "Quantidade_Falhas": qtd} 
                for situacao, data, qtd in dados
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
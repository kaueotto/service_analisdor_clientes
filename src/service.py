from flask import Flask, jsonify, request

from adapter import users,kafka
from data import models
from security import security
import json

app = Flask(__name__)

# poetry run flask --app src/service.py --debug run


# @app.route('/cadastro', methods=['POST'])
# def cadastro():
#     data = request.get_json()
#     try:
#         user = users.Users(data)
#         token = user.new_user()
#         return jsonify({'mensagem': token}), 200
#     except ValueError as ve:
#         return jsonify({'error': str(ve)}), 400
    
@app.route('/cadastro', methods=['POST'])
def cadastros():
    kafka_controller = kafka.KafkaAdapter()
    kafka_controller.produzir_mensagem(json.dumps(request.get_json()).encode('utf-8'),'novo_cadastro','topico-cadastros')
    return jsonify({'mensagem': 'Mensagem Inserida'}), 200

 
from confluent_kafka import Producer
from flask import Flask, jsonify, request

from controllers import users,kafka
from data import models
from security import security


app = Flask(__name__)

# poetry run flask --app src/service.py --debug run


@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    try:
        user = users.Users(data)
        token = user.new_user()
        return jsonify({'mensagem': token}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    
@app.route('/testekafka', methods=['POST'])
def kafkaateste():
    kaf = kafka.KafkaController()
    retorno = kaf.produzir_mensagem(kaf.criar_produtor(),'topico-cadastros',data = request.get_json())
    return retorno
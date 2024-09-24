import json

from flask import Flask, jsonify, request

from adapter import kafka
from security import security
from threading import Thread
from controller import consumer_cadastros

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
    dados = request.get_json()
    dados['tipo'] = 'cadastro'
    kafka_controller = kafka.KafkaAdapter()
    kafka_controller.produzir_mensagem(
        json.dumps(dados).encode('utf-8'),
        'novo_cadastro',
        'topico-cadastros',
    )
    return jsonify({'mensagem': 'Mensagem Inserida'}), 200


if __name__ == '__main__':
    flask_thread = Thread(target = app.run, kwargs={'host': 'localhost','port': '8081'})
    consumer_cadastros_thread = Thread(target=consumer_cadastros.consumer_cadastros)

    flask_thread.start()
    consumer_cadastros_thread.start()
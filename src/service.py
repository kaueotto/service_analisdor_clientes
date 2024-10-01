import json

from flask import Flask, jsonify, request

from adapter import kafka
from security import security
from threading import Thread
from controller import consumer_cadastros

app = Flask(__name__)

@app.route('/cadastro/modelos',methods=['POST'])
def cadastro_modelos():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]
    if not token:
        return jsonify({'message': 'Token é necessário!'}),401
    decoded_token = security.verify_token(token)
    if decoded_token: 
        dados = request.get_json()
        novo_json = {'tipo': 'dados_treinamento','dados': dados}
        kafka_controller = kafka.KafkaAdapter()
        kafka_controller.produzir_mensagem(
             json.dumps(novo_json).encode('utf-8'),
             'novo_cadastro',
             'topico-cadastros',
        )
        return jsonify({'mensagem': 'Mensagem Inserida'}), 200
    
@app.route('/cadastro/cliente', methods=['POST'])
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

    flask_thread.join()
    consumer_cadastros_thread.join()
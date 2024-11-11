#!/usr/bin/env python3
import json

from flask import Flask, jsonify, request

from adapter import kafka
from security import security
from threading import Thread
from controller import consumer_cadastros,consumer_fila_pedidos,processamento_pedidos

app = Flask(__name__)

@app.route('/cadastro/modelos', methods=['POST'])
def cadastro_modelos():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    if not token:
        return jsonify({'message': 'Token é necessário!'}), 401
    cli_valido, dto = security.verify_token(token)
    if not cli_valido:
        return jsonify({'message': 'Token inválido ou usuário não autorizado!'}), 403
    dados = request.get_json()
    if not dados:
        return jsonify({'message': 'Dados do modelo são necessários!'}), 400
    
    novo_json = {'tipo': 'dados_treinamento', 'dados': dados, 'context': dto.to_dict()}
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

@app.route('/fila/pedidos',methods=['POST'])
def fila_pedidos():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    if not token:
        return jsonify({'message': 'Token é necessário!'}), 401
    cli_valido, dto = security.verify_token(token)
    if not cli_valido:
        return jsonify({'message': 'Token inválido ou usuário não autorizado!'}), 403
    dados = request.get_json()
    if not dados:
        return jsonify({'message': 'Dados do modelo são necessários!'}), 400
    novo_json = {'tipo': 'pedido', 'dados': dados, 'context': dto.to_dict()}
    kafka_controller = kafka.KafkaAdapter()
    kafka_controller.produzir_mensagem(
        json.dumps(novo_json).encode('utf-8'),
        'pedido',
        'topico-fila-processamento',
    )
    return jsonify({'mensagem': 'Mensagem Inserida'}), 200

if __name__ == '__main__':
    flask_thread = Thread(target = app.run, kwargs={'host': 'localhost','port': '8081'})
    consumer_cadastros_thread = Thread(target=consumer_cadastros.consumer_cadastros)
    consumer_fila_pedidos_thread = Thread(target=consumer_fila_pedidos.consumer_fila_pedidos)
    processamento_pedidos_thread = Thread(target=processamento_pedidos.processa_fila_pedidos)

    flask_thread.start()
    consumer_cadastros_thread.start()
    consumer_fila_pedidos_thread.start()
    processamento_pedidos_thread.start()

    flask_thread.join()
    consumer_cadastros_thread.join()
    consumer_fila_pedidos_thread.join()
    processamento_pedidos_thread.join()
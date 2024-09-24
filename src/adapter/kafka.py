from kafka import KafkaConsumer, KafkaProducer

from config import configs
import json
import entity
from entity import cliente

class KafkaAdapter:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=configs.ENDERECO_KAFKA)

    def produzir_mensagem(self, mensagem, key, topico):
        if key is not None and not isinstance(
            key, (bytes, bytearray, memoryview)
        ):
            key = key.encode('utf-8')
        self.producer.send(topico, key=key, value=mensagem)
        self.producer.flush()

    def consumir_mensagem(self, groupid, topico):
        consumer = KafkaConsumer(
            bootstrap_servers=configs.ENDERECO_KAFKA,
            auto_offset_reset='earliest'
        )
        consumer.subscribe([topico])
        for message in consumer:
            if message.value:
                try:
                    mensagem_decodificada = message.value.decode('utf-8')
                    if mensagem_decodificada.strip().startswith('{') and mensagem_decodificada.strip().endswith('}'):
                        dados = json.loads(message.value)
                        if dados.get('tipo') == 'cadastro':
                            cli = cliente.Cliente.new_cliente(dados.get('clinome'), dados.get('cliemail'))
                            print(f"Mensagem recebida e processada: {cli}")
                        if dados.get('tipo') == 'modelos':
                            ...
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}, mensagem: {message.value}")
            else:
                print("Mensagem vazia recebida")

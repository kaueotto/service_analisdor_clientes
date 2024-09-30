from kafka import KafkaConsumer, KafkaProducer

from config import configs
import json
from entity import cliente
import time

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
            topico,
            bootstrap_servers=configs.ENDERECO_KAFKA,
            group_id=groupid,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: x.decode('utf-8')
        )
        while True:
            mensagem = consumer.poll(timeout_ms=1000)
            if mensagem:
                for tp, messages in mensagem.items():
                    for message in messages:
                        try:
                            dados = json.loads(message.value)
                            match dados.get('tipo'):
                                case 'cadastro':
                                    print('aaa')
                                    cli = cliente.Cliente.new_cliente(dados.get('clinome'), dados.get('cliemail'))
                                    print(f"Cliente cadastrado: {cli}")
                        except ValueError as ve:
                            print(f"Erro: {ve}")
                        except Exception as e:
                            print(f"Erro inesperado: {e}") 
                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar JSON: {e}, mensagem: {message.value}")
            else:
                time.sleep(5)
        
from confluent_kafka import Producer, Consumer
from config import configs

class KafkaController:
    def __init__(self):
        self.bootstrap_servers = configs.ENDERECO_KAFKA
        self.group_id = None

    def criar_produtor(self):
        conf = {'bootstrap.servers': self.bootstrap_servers}
        return Producer(conf)

    def criar_consumidor(self, topicos):
        conf = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        }
        consumidor = Consumer(conf)
        consumidor.subscribe(topicos)
        return consumidor

    def produzir_mensagem(self, produtor, topico, mensagem):
        produtor.produce(topico, mensagem)
        produtor.flush()

    def consumir_mensagem(self, consumidor):
        mensagem = consumidor.poll(timeout=1.0)
        if mensagem is not None:
            return mensagem.value().decode('utf-8')
        return None

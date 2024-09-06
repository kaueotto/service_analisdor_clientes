from config import configs
from kafka import KafkaProducer,KafkaConsumer

class KafkaEntity:

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=configs.ENDERECO_KAFKA)

    def produzir_mensagem(self, mensagem, key, topico):
        if key is not None and not isinstance(key, (bytes, bytearray, memoryview)):
            key = key.encode('utf-8')
        self.producer.send(topico,key=key,value=mensagem)
        self.producer.flush()

    def consumir_mensagem(self,key,topico):
        ...

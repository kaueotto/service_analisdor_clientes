from kafka import KafkaConsumer, KafkaProducer

from config import configs

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
            enable_auto_commit=False,
            value_deserializer=lambda x: x.decode('utf-8')
        )
        while True:
            mensagem = consumer.poll(timeout_ms=1000)
            if mensagem:
                consumer.commit()
                return mensagem.items()
            
        
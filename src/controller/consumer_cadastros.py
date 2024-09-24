from adapter.kafka import KafkaAdapter
from time import sleep
import json

def consumer_cadastros():
    adapter = KafkaAdapter()
    try:
        while True:
            # Consumir mensagens do Kafka
            print(1)
            mensagem = adapter.consumir_mensagem('grupo-cadastros', 'topico-cadastros')
            print(2)
            if mensagem is None or mensagem == b'':  # Verifica se a mensagem não está vazia
                print("Mensagem vazia ou não recebida")
                continue
            
            try:
                # Tenta carregar a mensagem como JSON
                dados = json.loads(mensagem)
                print(f"Mensagem recebida: {dados}")
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}, mensagem: {mensagem}")
            
            sleep(1)
    except Exception as e:
        print(f"Erro ao consumir mensagens: {e}")

from adapter.kafka import KafkaAdapter
import json

def consumer_cadastros():
    adapter = KafkaAdapter()
    try:
        while True:
            mensagem = adapter.consumir_mensagem('grupo-cadastros', 'topico-cadastros')
            if mensagem is None or mensagem == b'':
                print("Mensagem vazia ou não recebida")
                continue
            try:
                dados = json.loads(mensagem)
                print(f"Mensagem recebida: {dados}")
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}, mensagem: {mensagem}")
                pass
    except Exception as e:
        print(f"Erro ao consumir mensagens: {e}")
        pass

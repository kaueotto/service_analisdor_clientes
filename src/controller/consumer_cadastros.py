from adapter.kafka import KafkaAdapter
from entity import cliente, dados_modelos
from controller import training_model
import json
import threading

def consumer_cadastros():
    adapter = KafkaAdapter()
    try:
        while True:
            mensagems = adapter.consumir_mensagem('grupo-cadastros', 'topico-cadastros')
            print('mensagems: ', mensagems)
            if mensagems is None:
                print("Mensagem vazia ou não recebida")
                continue
            try:
                for tp, messages in mensagems:
                    for message in messages:
                        try:
                            dados = json.loads(message.value)
                            match dados.get('tipo'):
                                case 'cadastro':
                                    cli = cliente.Cliente.new_cliente(dados.get('clinome'), dados.get('cliemail'))
                                    print(f"Cliente cadastrado: {cli}")
                                case 'dados_treinamento':
                                    for dado in dados['dados']:
                                        dados_mod = dados_modelos.Dados_modelos.new_dados_modelos(5, **dado)
                                        print(dados_mod)
                                        if dado['end_json'] == 1:
                                            threadtreinamento = threading.Thread(
                                                target=training_model.treinar_modelo_randomForest, args=(5,)
                                            )
                                            threadtreinamento.start()
                                            threadtreinamento.join()
                        except ValueError as ve:
                            print(f"Erro: {ve}")
                        except Exception as e:
                            print(f"Erro inesperado: {e}")
                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar JSON: {e}, mensagem: {message.value}")

            except json.JSONDecodeError as e:
                pass
    except Exception as e:
        print(f"Erro ao consumir mensagens: {e}")
        pass

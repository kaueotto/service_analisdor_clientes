import json
import threading

from adapter.kafka import KafkaAdapter
from controller import training_model
from entity import cliente, dados_modelos
from entity.dto import dto_cliente


def consumer_cadastros():
    adapter = KafkaAdapter()
    try:
        while True:
            # topico-fila-processamento
            mensagems = adapter.consumir_mensagem(
                'grupo-cadastros', 'topico-cadastros'
            )
            if mensagems is None:
                print('Mensagem vazia ou não recebida')
                continue
            try:
                for tp, messages in mensagems:
                    for message in messages:
                        try:
                            dados = json.loads(message.value)
                            context = dados.get('context', {})
                            dtoCliente = dto_cliente.dto_cliente(
                                CliId=context.get('CliId')
                            )
                            match dados.get('tipo'):
                                case 'cadastro':
                                    cli = cliente.Cliente.new_cliente(
                                        dados.get('clinome'),
                                        dados.get('cliemail'),
                                    )
                                    print(f'Cliente cadastrado: {cli}')
                                case 'dados_treinamento':
                                    for dado in dados['dados']:
                                        dados_mod = dados_modelos.Dados_modelos.new_dados_modelos(
                                            dtoCliente.CliId, **dado
                                        )
                                        if dado['end_json'] == 1:
                                            threadtreinamento = threading.Thread(
                                                target=training_model.treinar_modelo_randomForest,
                                                args=(dtoCliente.CliId,),
                                            )
                                            threadtreinamento.start()
                        except ValueError as ve:
                            print(f'Erro: {ve}')
                        except Exception as e:
                            print(f'Erro inesperado: {e}')
                        except json.JSONDecodeError as e:
                            print(
                                f'Erro ao decodificar JSON: {e}, mensagem: {message.value}'
                            )

            except json.JSONDecodeError as e:
                pass
    except Exception as e:
        print(f'Erro ao consumir mensagens: {e}')
        pass

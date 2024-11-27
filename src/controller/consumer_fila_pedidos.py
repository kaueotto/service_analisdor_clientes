import json

from adapter.kafka import KafkaAdapter
from entity import fila
from entity.dto import dto_cliente


def consumer_fila_pedidos():
    adapter = KafkaAdapter()
    try:
        while True:
            mensagems = adapter.consumir_mensagem(
                'grupo-cadastros', 'topico-fila-processamento'
            )
            if mensagems is None:
                print('Mensagem vazia ou não recebida')
                continue
            try:
                for tp, messages in mensagems:
                    for message in messages:
                        try:
                            dados = json.loads(message.value)
                            chaveexterna = dados.get('dados', {})['pedid']
                            context = dados.get('context', {})
                            dtoCliente = dto_cliente.dto_cliente(
                                CliId=context.get('CliId')
                            )
                            match dados.get('tipo'):
                                case 'pedido':
                                    fila.Fila.new_pedido_fila(
                                        dtoCliente.CliId, dados, chaveexterna
                                    )
                        except Exception as e:
                            print(f'Erro Inesperado {e}')
            except Exception as e:
                print(f'Erro Inesperado {e}')
    except Exception as e:
        print(f'Erro Inesperado {e}')

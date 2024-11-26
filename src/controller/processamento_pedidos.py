import json
import pickle
import pandas as pd
from lime.lime_tabular import LimeTabularExplainer
from entity import orm, modelos, fila
from entity.dto import dto_fila, dto_modelos
def processa_fila_pedidos():
    QH = orm.QueryHelper()
    while True:
        try:
            fila_instance = QH.buscar_por_atributo(fila.Fila, FilaResultado=None)
            if fila_instance:
                fila_dto = dto_fila.dto_fila.from_model(fila_instance)
                modelo_instance = QH.buscar_por_atributo(modelos.Modelos, ModId=fila_dto.FilaModId)
                modelo_dto = dto_modelos.dto_modelos.from_model(modelo_instance)

                modelo_treinado = pickle.loads(modelo_dto.ModTreinado)
                if modelo_treinado is None:
                    print("Erro: O modelo treinado não pôde ser carregado.")
                    continue

                dados_sacado = json.loads(fila_dto.FilaInfoSacado).get("dados", None)
                if dados_sacado is None:
                    print("Erro: Dados do sacado são None.")
                    continue

                # Verifica se todos os campos necessários estão presentes
                campos_necessarios = ["CliLimCredTot", "clisimples", "cliMicroEmpreendedor", "CliConsFinal", 
                                      "HistPagPONTUAL", "HistPagAVISTA", "HistPag8_15", "HistPag16_30", 
                                      "HistPag31_60", "HistPag_60"]
                for campo in campos_necessarios:
                    if campo not in dados_sacado or dados_sacado[campo] is None:
                        print(f"Erro: O campo '{campo}' está faltando ou é None.")
                        continue

                dados_df = pd.DataFrame([dados_sacado])
                if dados_df.isnull().any().any():
                    print("Erro: Existem valores nulos no DataFrame de entrada.")
                    continue

                # Completa colunas faltantes
                missing_cols = set(modelo_treinado.feature_names_in_) - set(dados_df.columns)
                for col in missing_cols:
                    dados_df[col] = 0  # Ou um valor padrão apropriado

                dados_df = dados_df[modelo_treinado.feature_names_in_]
                previsao = modelo_treinado.predict(dados_df)
                if previsao is None or len(previsao) == 0:
                    print("Erro: A previsão retornou um valor inválido.")
                    continue

                previsao = int(previsao[0])

                # Explicar o resultado com LIME
                explainer = LimeTabularExplainer(
                    training_data=dados_df.values,  # Dados de treinamento usados para construir o modelo
                    feature_names=modelo_treinado.feature_names_in_,
                    mode='classification' if modelo_treinado.predict(dados_df) else 'regression'
                )
                
                # Gerar explicação para a previsão
                exp = explainer.explain_instance(
                    data_row=dados_df.values[0],  # A linha para explicar
                    predict_fn=modelo_treinado.predict_proba  # Função de previsão do modelo
                )
                
                # Obter a explicação em um formato mais legível
                explicacao = exp.as_list()

                # Armazenar o resultado e o motivo da previsão
                QH.alterar_registros(
                    fila.Fila, 
                    {'FilaId': fila_dto.FilaId}, 
                    FilaResultado=previsao, 
                    
                    FilaMotivoResultado=json.dumps(dict(explicacao))  # Converte para JSON
                )
                
                print(f"Previsão para o pedido {fila_dto.FilaId}: {previsao}")
                print(f"Motivo da previsão: {explicacao}")

        except Exception as e:
            print(f"Erro ao processar pedido na fila: {e}")

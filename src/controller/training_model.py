import pandas as pd
import pickle
from entity import orm, dados_modelos, modelos
from entity.dto.dto_dados_modelo import dto_dados_modelo
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

def montar_dataframe(lista):
    dados_lista = []
    for dado in lista:
        dto = dto_dados_modelo(
            id=dado.id,
            cliid=dado.cliid,
            IdCliente=dado.IdCliente,
            status=dado.status,
            pedid=dado.pedid,
            CliLimCredTot=dado.CliLimCredTot,
            clisimples=dado.clisimples,
            cliMicroEmpreendedor=dado.cliMicroEmpreendedor,
            CliConsFinal=dado.CliConsFinal,
            HistPagPONTUAL=dado.HistPagPONTUAL,
            HistPagAVISTA=dado.HistPagAVISTA,
            HistPag8_15=dado.HistPag8_15,
            HistPag16_30=dado.HistPag16_30,
            HistPag31_60=dado.HistPag31_60,
            HistPag_60=dado.HistPag_60,
            QtConsultado=dado.QtConsultado,
            RelaFornec0_6Meses=dado.RelaFornec0_6Meses,
            RelaFornec6Mes_1Ano=dado.RelaFornec6Mes_1Ano,
            RelaFornec1_3Anos=dado.RelaFornec1_3Anos,
            RelaFornec3_5Anos=dado.RelaFornec3_5Anos,
            RelaFornec5_10Anos=dado.RelaFornec5_10Anos,
            RelaFornec10Anos=dado.RelaFornec10Anos,
            RelaFornecINAT=dado.RelaFornecINAT,
            PefinNumOcorrencia=dado.PefinNumOcorrencia,
            PefinValorTotal=dado.PefinValorTotal,
            RefinNumOcorrencia=dado.RefinNumOcorrencia,
            RefinValorTotal=dado.RefinValorTotal,
            DividasVencNumOcorrencia=dado.DividasVencNumOcorrencia,
            DividasVencValorTotal=dado.DividasVencValorTotal,
            FalenConcNumOcorrencia=dado.FalenConcNumOcorrencia,
            CheqSFundoNumOcorrencia=dado.CheqSFundoNumOcorrencia,
            RechequeNumOcorrencia=dado.RechequeNumOcorrencia,
            PartFalenNumOcorrencia=dado.PartFalenNumOcorrencia
        )
        dados_lista.append(dto.__dict__)
    df = pd.DataFrame(dados_lista)
    return df

def treinar_modelo_randomForest(idcliente):
    try:
        QH = orm.QueryHelper()
        lista = QH.buscar_lista(dados_modelos.Dados_modelos, cliid=idcliente)
        df = montar_dataframe(lista)
        df['status'] = df['status'].map({'bloqueado': 0, 'liberado': 1})
        df = df.fillna(0)
        df = df.drop(columns=['id', 'cliid', 'IdCliente','pedid'])
        
        X = df.drop('status', axis=1)
        y = df['status']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        print('Modelo treinado com sucesso!')

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        print(f'Acurácia: {accuracy * 100:.2f}%')
        print('Matriz de Confusão:')
        print(conf_matrix)

        modelo_serializado = pickle.dumps(model)
        retorno = modelos.Modelos.new_modelo(cliid=idcliente, modelo=modelo_serializado)
        print(retorno)
        retorno = dados_modelos.Dados_modelos.delete_dados_modelos(idcliente)
        print(retorno)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
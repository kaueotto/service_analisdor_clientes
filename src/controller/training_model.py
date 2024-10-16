import pandas as pd
from entity import orm, dados_modelos
from entity.dto.dto_dados_modelo import dto_dados_modelo
import seaborn as sns
import matplotlib.pyplot as plt


def montar_dataframe(lista):
    dados_lista = []
    for dado in lista:
        dto = dto_dados_modelo(
            id=dado.id,
            cliid=dado.cliid,
            IdCliente=dado.IdCliente,
            status=dado.status,
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
    QH = orm.QueryHelper()
    lista = QH.buscar_lista(dados_modelos.Dados_modelos, cliid=idcliente)
    df = montar_dataframe(lista)
    df['status'] = df['status'].map({'bloqueado': 0, 'liberado': 1})
    df = df.fillna(0)
    df = df.drop(columns=['id','cliid','IdCliente'])
    

    return 'Modelo treinado'

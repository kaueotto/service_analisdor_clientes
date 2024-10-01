from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from sqlalchemy import Integer, String, Float, Boolean, Column
from entity.orm import Base
from entity import orm



class Dados_modelos(Base):
    __tablename__ = 'dados_modelos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliid = Column(Integer, nullable=False)
    IdCliente = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    CliLimCredTot = Column(Float, nullable=True)
    clisimples = Column(Integer, nullable=True)
    cliMicroEmpreendedor = Column(Integer, nullable=True)
    CliConsFinal = Column(Boolean, nullable=True)
    HistPagPONTUAL = Column(Float, nullable=True)
    HistPagAVISTA = Column(Float, nullable=True) 
    HistPag8_15 = Column(Float, nullable=True)
    HistPag16_30 = Column(Float, nullable=True)
    HistPag31_60 = Column(Float, nullable=True)
    HistPag_60 = Column(Float, nullable=True)
    QtConsultado = Column(Float, nullable=True)
    RelaFornec0_6Meses = Column(Float, nullable=True) 
    RelaFornec6Mes_1Ano = Column(Float, nullable=True) 
    RelaFornec1_3Anos = Column(Float, nullable=True) 
    RelaFornec3_5Anos = Column(Float, nullable=True) 
    RelaFornec5_10Anos = Column(Float, nullable=True) 
    RelaFornec10Anos = Column(Float, nullable=True) 
    RelaFornecINAT = Column(Float,nullable=True)
    PefinNumOcorrencia = Column(Float, nullable=True)
    PefinValorTotal = Column(Float, nullable=True)
    RefinNumOcorrencia = Column(Float, nullable=True) 
    RefinValorTotal = Column(Float, nullable=True) 
    DividasVencNumOcorrencia = Column(Float, nullable=True) 
    DividasVencValorTotal = Column(Float, nullable=True) 
    FalenConcNumOcorrencia = Column(Float, nullable=True) 
    CheqSFundoNumOcorrencia = Column(Float, nullable=True) 
    RechequeNumOcorrencia = Column(Float, nullable=True) 
    PartFalenNumOcorrencia = Column(Float, nullable=True)     
  
    start_json = Column(Boolean, nullable=False, default=False)
    end_json = Column(Boolean, nullable=False, default=False) 

    @classmethod
    def new_dados_modelos(cls,Id,**filtros):
        
        QH = orm.QueryHelper()

        try:
            QH.inserir_registro(cls,cliid=Id,**filtros)
            return "Novo registro adicionado com sucesso."
        except Exception as e:
            print(f"Erro ao adicionar dados_modelos: {e}")
            raise
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary

from entity.orm import Base
from entity import orm

class Modelos(Base):
    __tablename__ = 'modelos'

    ModId = Column(Integer, primary_key=True, autoincrement=True)
    ModCliId = Column(Integer, ForeignKey('cliente.CliId'), nullable=False)
    ModTreinado = Column(LargeBinary, default=False, nullable=False)
    ModAtivo = Column(Boolean, default=True, nullable=False)
    ModDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def new_modelo(cls,cliid,modelo):
        QH = orm.QueryHelper()
        try:
            filtros = {"ModCliId":cliid,"ModAtivo":True}
            novos_dados = {"ModAtivo":False}
            QH.alterar_registros(cls,filtros,**novos_dados)
            QH.inserir_registro(cls,ModCliId=cliid,ModTreinado=modelo)
            return 'Modelo inserido com sucesso!'
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")
            raise
    
    

    



from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary
from sqlalchemy.orm import relationship

from entity.orm import Base
from entity import orm

class Modelos(Base):
    __tablename__ = 'modelos'

    ModId = Column(Integer, primary_key=True, autoincrement=True)
    ModCliId = Column(Integer, ForeignKey('cliente.CliId'), nullable=False)
    ModTreinado = Column(LargeBinary, default=False, nullable=False)
    ModAtivo = Column(Boolean, default=True, nullable=False)
    ModDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)

   # cliente = relationship('Cliente', back_populates='modelos')
   # filas = relationship('Fila', back_populates='modelo')
    
    @classmethod
    def new_modelo(cls,cliid,modelo):
        QH = orm.QueryHelper()
        try:
            QH.inserir_registro(cls,ModCliId=cliid,ModTreinado=modelo)
            return 'Modelo inserido com sucesso!'
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")
            raise

    



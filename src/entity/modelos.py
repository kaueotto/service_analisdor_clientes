from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from entity.orm import Base


class Modelos(Base):
    __tablename__ = 'modelos'

    ModId = Column(Integer, primary_key=True, autoincrement=True)
    ModCliId = Column(Integer, ForeignKey('cliente.CliId'), nullable=False)
    ModTreinado = Column(Boolean, default=False, nullable=False)
    ModAtivo = Column(Boolean, default=True, nullable=False)
    ModDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)

   # cliente = relationship('Cliente', back_populates='modelos')
   # filas = relationship('Fila', back_populates='modelo')
    
    @classmethod
    def new_modelo(cls,cliid):
        ...



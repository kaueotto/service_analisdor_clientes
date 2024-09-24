from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from entity import Base


class Fila(Base):
    __tablename__ = 'fila'

    FilaId = Column(Integer, primary_key=True, autoincrement=True)
    FilaInfoSacado = Column(Text, nullable=False)
    FilaCliId = Column(Integer, ForeignKey('cliente.CliId'), nullable=False)
    FilaModId = Column(Integer, ForeignKey('modelos.ModId'), nullable=True)
    FilaDataInclusao = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    FilaDataEnvioCliente = Column(DateTime, nullable=True)
    FilaResultado = Column(String(255), nullable=True)
    FilaMotivoResultado = Column(String(255), nullable=True)

    #cliente = relationship('Cliente', back_populates='filas')
    #modelo = relationship('Modelos', back_populates='filas')

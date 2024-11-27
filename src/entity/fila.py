import json
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from entity import modelos, orm
from entity.dto import dto_fila, dto_modelos
from entity.orm import Base


class Fila(Base):
    __tablename__ = 'fila'

    FilaId = Column(Integer, primary_key=True, autoincrement=True)
    FilaInfoSacado = Column(Text, nullable=False)
    FilaChaveExterna = Column(Integer, nullable=False)
    FilaCliId = Column(Integer, ForeignKey('cliente.CliId'), nullable=False)
    FilaModId = Column(Integer, ForeignKey('modelos.ModId'), nullable=True)
    FilaDataInclusao = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    FilaDataEnvioCliente = Column(DateTime, nullable=True)
    FilaResultado = Column(String(255), nullable=True)
    FilaMotivoResultado = Column(Text, nullable=True)

    @classmethod
    def new_pedido_fila(cls, cliid, dados, chaveexterna):
        QH = orm.QueryHelper()
        try:
            modelo_instance = QH.buscar_por_atributo(
                modelos.Modelos, ModCliId=cliid, ModAtivo=True
            )
            if modelo_instance:
                modelo_dto = dto_modelos.dto_modelos.from_model(
                    modelo_instance
                )
                QH.inserir_registro(
                    cls,
                    FilaCliId=cliid,
                    FilaChaveExterna=chaveexterna,
                    FilaModId=modelo_dto.ModId,
                    FilaInfoSacado=json.dumps(dados),
                )
                return 'Pedido inserido na fila com sucesso'
            else:
                return 'Nenhum modelo ativo encontrado para o cliente'
        except Exception as e:
            return f'Erro ao inserir pedido na fila: {e}'

    @classmethod
    def buscar_resultado(cls, pedid):
        QH = orm.QueryHelper()
        try:
            pedido_processado = QH.buscar_por_atributo(
                cls, FilaChaveExterna=pedid
            )
            if pedido_processado:
                fila_dto = dto_fila.dto_fila.from_model(pedido_processado)

                return fila_dto.FilaResultado, fila_dto.FilaMotivoResultado
            else:
                return 'Nenhum modelo ativo encontrado para o cliente'
        except Exception as e:
            return f'Erro ao inserir pedido na fila: {e}'

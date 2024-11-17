from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from entity.orm import Base
from entity import orm
from security import security


class Cliente(Base):
    __tablename__ = 'cliente'

    CliId = Column(Integer, primary_key=True, autoincrement=True)
    CliNome = Column(String(255), nullable=False)
    CliEmail = Column(String(255), nullable=False)
    CliDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)
    CliDataExclusao = Column(DateTime, nullable=True)
    CliToken = Column(String(255), nullable=False)

    @classmethod
    def new_cliente(cls, name: str, email: str) -> str:
        QH = orm.QueryHelper()
        try:
            existing_cliente = QH.buscar_por_atributo(cls,CliNome=name)
            if existing_cliente:
                raise ValueError(
                    f"Cliente com o nome '{name}' já está cadastrado."
                )
            token = security.create_token(name)
            QH.inserir_registro(cls,CliNome=name,CliEmail=email,CliToken=token)
            return token
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")
            raise

    @classmethod
    def valida_cliente(cls,cliId) -> bool:
        QH = orm.QueryHelper()

        try:
            a = QH.buscar_por_atributo(cls,cliId=cliId,CliDataExclusao=None)
            print(a)
            return True
        except Exception as e:
            print(f"Erro ao validar usuario: {e}")
            return False
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from entity.__init__ import Base, new_session
from security import security


class Cliente(Base):
    __tablename__ = 'cliente'

    CliId = Column(Integer, primary_key=True, autoincrement=True)
    CliNome = Column(String(255), nullable=False)
    CliEmail = Column(String(255), nullable=False)
    CliDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)
    CliDataExclusao = Column(DateTime, nullable=True)
    CliToken = Column(String(255), nullable=False)

    modelos = relationship('Modelos', back_populates='cliente')
    filas = relationship('Fila', back_populates='cliente')

    @classmethod
    def new_cliente(cls, name: str, email: str) -> str:
        new_cliente = cls(
            CliNome=name, CliEmail=email, CliToken=security.create_token(name)
        )
        session = new_session()

        existing_cliente = session.query(cls).filter_by(CliNome=name).first()

        if existing_cliente:
            raise ValueError(
                f"Cliente com o nome '{name}' já está cadastrado."
            )

        session.add(new_cliente)
        session.commit()
        return new_cliente.CliToken

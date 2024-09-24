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

    #modelos = relationship('Modelos', back_populates='cliente')
    #filas = relationship('Fila', back_populates='cliente')

    @classmethod
    def new_cliente(cls, name: str, email: str) -> str:
        print('entrou cadastro')
        print(name)
        print(email)
        session = new_session()
        print(session)
        try:
            existing_cliente = session.query(cls).filter_by(CliNome=name).first()
            print(existing_cliente)
            if existing_cliente:
                raise ValueError(
                    f"Cliente com o nome '{name}' já está cadastrado."
                )
            print(10)
            new_cliente = cls(
                CliNome=name, 
                CliEmail=email, 
                CliToken=security.create_token(name)
            )
            print(11)
            session.add(new_cliente)
            session.commit()
            return new_cliente.CliToken
        except Exception as e:
            # Adicionar tratamento de erro se necessário
            print(f"Erro ao adicionar cliente: {e}")
            session.rollback()  # Reverte qualquer alteração se ocorrer um erro
            raise
        finally:
            session.close()  # Garante que a sessão será fechada

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from config import configs
from security import security

Base = declarative_base()


def new_session():
    connection_string = f'mssql+pyodbc://{configs.SERVER}/{configs.DATABASE}?driver={configs.DRIVER}&trusted_connection=yes'
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


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


class Modelos(Base):
    __tablename__ = 'modelos'

    ModId = Column(Integer, primary_key=True, autoincrement=True)
    ModCliId = Column(Integer, ForeignKey('cliente.CliId'), nullable=False)
    ModTreinado = Column(Boolean, default=False, nullable=False)
    ModAtivo = Column(Boolean, default=True, nullable=False)
    ModDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)

    cliente = relationship('Cliente', back_populates='modelos')
    filas = relationship('Fila', back_populates='modelo')


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

    cliente = relationship('Cliente', back_populates='filas')
    modelo = relationship('Modelos', back_populates='filas')
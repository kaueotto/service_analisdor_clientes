from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from config import configs

# Definir a base declarativa
Base = declarative_base()

# Definir a classe Cliente
class Cliente(Base):
    __tablename__ = 'cliente'

    CliId = Column(Integer, primary_key=True, autoincrement=True)
    CliNome = Column(String(255), nullable=False)
    CliEmail = Column(String(255), nullable=False)
    CliDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)
    CliDataExclusao = Column(DateTime, nullable=True)
    CliToken = Column(String(255), nullable=False)

    # Relacionamento com a tabela Modelos
    modelos = relationship('Modelos', back_populates='cliente')
    # Relacionamento com a tabela Fila
    filas = relationship('Fila', back_populates='cliente')

# Definir a classe Modelos
class Modelos(Base):
    __tablename__ = 'modelos'

    ModId = Column(Integer, primary_key=True, autoincrement=True)
    ModCliId = Column(Integer, ForeignKey('cliente.CliId'), nullable=False)
    ModTreinado = Column(Boolean, default=False, nullable=False)
    ModAtivo = Column(Boolean, default=True, nullable=False)
    ModDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento com a tabela Cliente
    cliente = relationship('Cliente', back_populates='modelos')
    # Relacionamento com a tabela Fila
    filas = relationship('Fila', back_populates='modelo')

# Definir a classe Fila
class Fila(Base):
    __tablename__ = 'fila'

    FilaId = Column(Integer, primary_key=True, autoincrement=True)
    FilaInfoSacado = Column(Text, nullable=False)
    FilaCliId = Column(Integer, ForeignKey('cliente.CliId'), nullable=False)
    FilaModId = Column(Integer, ForeignKey('modelos.ModId'), nullable=True)
    FilaDataInclusao = Column(DateTime, default=datetime.utcnow, nullable=False)
    FilaDataEnvioCliente = Column(DateTime, nullable=True)
    FilaResultado = Column(String(255), nullable=True)
    FilaMotivoResultado = Column(String(255), nullable=True)

    # Relacionamento com a tabela Cliente
    cliente = relationship('Cliente', back_populates='filas')
    # Relacionamento com a tabela Modelos
    modelo = relationship('Modelos', back_populates='filas')

# Criar engine e session

server = configs.SERVER
database = configs.DATABASE
driver = configs.DRIVER

connection_string = f"mssql+pyodbc://{server}/{database}?driver={driver}&trusted_connection=yes"

engine = create_engine(connection_string)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Exemplo de como adicionar um novo cliente
novo_cliente = Cliente(
    CliNome='Nome do Cliente',
    CliEmail='cliente@example.com',
    CliToken='token-unico-123'
)

session.add(novo_cliente)
session.commit()

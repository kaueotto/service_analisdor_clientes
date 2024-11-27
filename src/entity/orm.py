from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,declarative_base

from config import configs

Base = declarative_base()

class QueryHelper:
    def __init__(self):
        connection_string = f'mssql+pyodbc://{configs.SERVER}/{configs.DATABASE}?driver={configs.DRIVER}&trusted_connection=yes'
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def buscar_por_atributo(self, model_class, **filtros):
        return self.session.query(model_class).filter_by(**filtros).first()

    def inserir_registro(self, model_class, **dados):
        novo_registro = model_class(**dados)
        self.session.add(novo_registro)
        self.session.commit()
        return novo_registro

    def alterar_registro(self, model_class, filtros, **novos_dados):
        registro = self.session.query(model_class).filter_by(**filtros).first()
        if registro:
            for chave, valor in novos_dados.items():
                setattr(registro, chave, valor)
            self.session.commit()
        return registro

    def alterar_registros(self, model_class, filtros, **novos_dados):
        try:
            registros = self.session.query(model_class).filter_by(**filtros)
            registros.update(novos_dados, synchronize_session="fetch")
            self.session.commit()
            return registros.all()
        except Exception as e:
            self.session.rollback()
            print(f"Erro ao atualizar registros: {e}")
            return None

    def deletar_registro(self, model_class, **filtros):
        registros = self.session.query(model_class).filter_by(**filtros)
        if registros.count() > 0:
            registros.delete(synchronize_session='fetch')
            self.session.commit()
        return f'Registros {registros.count()} deletados com sucesso'
    
    def buscar_lista(self, model_class, **filtros):
        return self.session.query(model_class).filter_by(**filtros).all()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import configs

Base = declarative_base()

from sqlalchemy.orm import Session

class QueryHelper:
    def __init__(self):
        connection_string = f'mssql+pyodbc://{configs.SERVER}/{configs.DATABASE}?driver={configs.DRIVER}&trusted_connection=yes'
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    # Buscar registro
    def buscar_por_atributo(self, model_class, **filtros):
        """
        Busca o primeiro registro que corresponde aos filtros fornecidos.
        """
        return self.session.query(model_class).filter_by(**filtros).first()

    # Inserir registro
    def inserir_registro(self, model_class, **dados):
        """
        Insere um novo registro no banco de dados com os dados fornecidos.
        """
        novo_registro = model_class(**dados)  # Cria uma nova instância da classe
        self.session.add(novo_registro)       # Adiciona o novo registro à sessão
        self.session.commit()                 # Confirma a transação no banco
        return novo_registro                  # Retorna o registro inserido

    # Alterar registro
    def alterar_registro(self, model_class, filtros, **novos_dados):
        """
        Atualiza os dados do primeiro registro que corresponde aos filtros fornecidos.
        """
        registro = self.session.query(model_class).filter_by(**filtros).first()
        if registro:
            for chave, valor in novos_dados.items():
                setattr(registro, chave, valor)  # Altera o valor do atributo
            self.session.commit()                # Confirma a transação no banco
        return registro

    # Deletar registro
    def deletar_registro(self, model_class, **filtros):
        """
        Deleta o primeiro registro que corresponde aos filtros fornecidos.
        """
        registro = self.session.query(model_class).filter_by(**filtros).first()
        if registro:
            self.session.delete(registro)  # Marca o registro para ser deletado
            self.session.commit()           # Confirma a transação no banco
        return registro

# # Exemplo de uso
# def buscar_registro(session, model_class, **filtros):
#     query_helper = QueryHelper(session)
#     return query_helper.buscar_por_atributo(model_class, **filtros)

# def inserir_registro(session, model_class, **dados):
#     query_helper = QueryHelper(session)
#     return query_helper.inserir_registro(model_class, **dados)

# def alterar_registro(session, model_class, filtros, **novos_dados):
#     query_helper = QueryHelper(session)
#     return query_helper.alterar_registro(model_class, filtros, **novos_dados)

# def deletar_registro(session, model_class, **filtros):
#     query_helper = QueryHelper(session)
#     return query_helper.deletar_registro(model_class, **filtros)

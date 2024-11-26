from datetime import datetime

    

class dto_fila:
    def __init__(self,
                FilaId = None,
                FilaInfoSacado = None,
                FilaCliId = None,
                FilaModId = None,
                FilaDataInclusao = None,
                FilaDataEnvioCliente = None,
                FilaResultado = None,
                FilaChaveExterna = None,
                FilaMotivoResultado = None):
        self.FilaId = FilaId
        self.FilaChaveExterna = FilaChaveExterna
        self.FilaInfoSacado = FilaInfoSacado
        self.FilaCliId = FilaCliId
        self.FilaModId = FilaModId
        self.FilaDataInclusao = FilaDataInclusao
        self.FilaDataEnvioCliente = FilaDataEnvioCliente
        self.FilaResultado = FilaResultado
        self.FilaMotivoResultado = FilaMotivoResultado

    @classmethod
    def from_model(cls, model_instance):
        """Construtor alternativo para criar dto_modelos a partir de um objeto Modelos"""
        return cls(
            FilaId=model_instance.FilaId,
            FilaInfoSacado=model_instance.FilaInfoSacado,
            FilaCliId=model_instance.FilaCliId,
            FilaModId = model_instance.FilaModId,
            FilaDataInclusao = model_instance.FilaDataInclusao,
            FilaDataEnvioCliente = model_instance.FilaDataEnvioCliente,
            FilaResultado = model_instance.FilaResultado,
            FilaMotivoResultado = model_instance.FilaMotivoResultado,
            FilaChaveExterna = model_instance.FilaChaveExterna
        )    

    
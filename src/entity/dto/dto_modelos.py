from datetime import datetime

class dto_modelos:
    def __init__(self,
                ModId = None,
                ModCliId = None,
                ModTreinado = None,
                ModAtivo = None,
                ModDataInclusao = None):
        self.ModId = ModId
        self.ModCliId = ModCliId
        self.ModTreinado = ModTreinado
        self.ModAtivo = ModAtivo
        self.ModDataInclusao = ModDataInclusao

    @classmethod
    def from_model(cls, model_instance):
        """Construtor alternativo para criar dto_modelos a partir de um objeto Modelos"""
        return cls(
            ModId=model_instance.ModId,
            ModCliId=model_instance.ModCliId,
            ModTreinado=model_instance.ModTreinado,
            ModAtivo=model_instance.ModAtivo,
            ModDataInclusao=model_instance.ModDataInclusao
        )    
    

    def __str__(self):
        return (f"dto_modelos(ModId={self.ModId}, ModCliId='{self.ModCliId}', "
                f"ModTreinado='{self.ModTreinado}', ModAtivo={self.ModAtivo}, "
                f"ModDataInclusao={self.ModDataInclusao}')")
    
    def to_dict(self):
        return {
            'ModId': self.ModId,
            'ModCliId': self.ModCliId,
            'ModTreinado': self.ModTreinado,
            'ModAtivo': self.ModAtivo,
            'ModDataInclusao': self.ModDataInclusao.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.ModDataInclusao, datetime) else self.ModDataInclusao
        }    


    
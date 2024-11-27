from datetime import datetime


class dto_cliente:
    def __init__(
        self,
        CliId=None,
        CliNome=None,
        CliEmail=None,
        CliDataInclusao=None,
        CliDataExclusao=None,
        CliToken=None,
    ):
        self.CliId = CliId
        self.CliNome = CliNome
        self.CliEmail = CliEmail
        self.CliDataInclusao = CliDataInclusao
        self.CliDataExclusao = CliDataExclusao
        self.CliToken = CliToken

    def __str__(self):
        return (
            f"dto_cliente(CliId={self.CliId}, CliNome='{self.CliNome}', "
            f"CliEmail='{self.CliEmail}', CliDataInclusao={self.CliDataInclusao}, "
            f"CliDataExclusao={self.CliDataExclusao}, CliToken='{self.CliToken}')"
        )

    def to_dict(self):
        return {
            'CliId': self.CliId,
            'CliNome': self.CliNome,
            'CliEmail': self.CliEmail,
            'CliDataInclusao': self.CliDataInclusao.strftime(
                '%Y-%m-%d %H:%M:%S'
            )
            if isinstance(self.CliDataInclusao, datetime)
            else self.CliDataInclusao,
            'CliDataExclusao': self.CliDataExclusao.strftime(
                '%Y-%m-%d %H:%M:%S'
            )
            if isinstance(self.CliDataExclusao, datetime)
            else self.CliDataExclusao,
            'CliToken': self.CliToken,
        }

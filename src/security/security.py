import jwt

from config import configs
from entity import cliente, orm
from entity.dto import dto_cliente


def create_token(data) -> str:
    payload = {'data': data}
    token = jwt.encode(payload, configs.TOKEN, algorithm='HS256')
    return token


def verify_token(token) -> bool:
    try:
        QH = orm.QueryHelper()
        cli = QH.buscar_por_atributo(cliente.Cliente, CliToken=token)
        if cli:
            dto = dto_cliente.dto_cliente(
                CliId=cli.CliId,
                CliNome=cli.CliNome,
                CliEmail=cli.CliEmail,
                CliDataInclusao=cli.CliDataInclusao,
                CliDataExclusao=cli.CliDataExclusao,
                CliToken=cli.CliToken,
            )
            if dto.CliDataExclusao is None:
                return True, dto
            else:
                return False, ''
        else:
            return False, ''
    except jwt.InvalidTokenError as e:
        return e

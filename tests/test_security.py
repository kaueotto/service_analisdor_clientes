import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from unittest.mock import patch

import jwt

from src.config import configs
from src.entity.cliente import Cliente
from src.security.security import create_token, verify_token

# Mocks para dados
mock_cliente = Cliente(
    CliId=26,
    CliNome='agoravai',
    CliEmail='agoravai@gmail.com.br',
    CliDataInclusao='2024-01-01',
    CliDataExclusao=None,
    CliToken='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiYWdvcmF2YWkifQ.ZdOIXPD5RPtF93KFXKH0_HFAvsjvAgCIzTZjKRXyy9M',
)


def test_create_token():
    data = 'agoravai'
    token = create_token(data)
    decoded = jwt.decode(token, configs.TOKEN, algorithms=['HS256'])
    assert decoded == {'data': data}


@patch(
    'src.entity.orm.QueryHelper.buscar_por_atributo', return_value=mock_cliente
)
def test_verify_token_valid(mock_buscar_por_atributo):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiYWdvcmF2YWkifQ.ZdOIXPD5RPtF93KFXKH0_HFAvsjvAgCIzTZjKRXyy9M'
    is_valid, dto = verify_token(token)
    assert is_valid is True
    assert dto.CliId == mock_cliente.CliId
    assert dto.CliNome == mock_cliente.CliNome
    assert dto.CliEmail == mock_cliente.CliEmail


@patch('src.entity.orm.QueryHelper.buscar_por_atributo', return_value=None)
def test_verify_token_invalid_client(mock_buscar_por_atributo):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyIgICAgIjoiYW1vcmEifQ.LOxw2PXhFpchpBV0dAZ-OEXnbOH1dsoZotWRF123123'
    is_valid, dto = verify_token(token)
    assert is_valid is False
    assert dto == ''

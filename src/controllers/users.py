import json

from data.models import Cliente


class Users:
    def __init__(self, data: json) -> None:
        self.name = data['clinome']
        self.email = data['cliemail']

    def new_user(self) -> str:
        token = Cliente.new_cliente(self.name, self.email)
        return token

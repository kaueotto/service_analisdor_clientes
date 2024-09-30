import jwt

from config import configs


def create_token(data) -> str:
    payload = {'    ': data}
    print(payload)
    print(configs.TOKEN)
    token = jwt.encode(payload, configs.TOKEN, algorithm='HS256')
    return token

def verify_token(token) -> str:
    try:
        decoded_token = jwt.decode(token, configs.TOKEN, algorithms='HS256')
        return decoded_token
    except jwt.InvalidTokenError:
        return 'Token inválido!'
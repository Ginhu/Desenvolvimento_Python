from datetime import datetime
import jwt
from jwt import InvalidSignatureError

from tdd.erros import TokenInvalido, ImpossivelVerificarTimeout, JwtExpirado

key = '1key'


def gera_jwt(dados: dict, dh: bool = False) -> str:
    dicionario = dict(dados)
    if dh:
        dicionario['criado_em'] = datetime.now().astimezone().isoformat()

    token = jwt.encode(dicionario, key, algorithm='HS256')
    return token


def descriptografa_jwt(token: str, expira_em: int = 0) -> dict:
    try:
        descript_jwt = jwt.decode(token, key, algorithms='HS256')
    except InvalidSignatureError:
        raise TokenInvalido('Token fornecido não é válido')

    if expira_em <= 0:
        return descript_jwt

    if 'criado_em' not in descript_jwt:
        raise ImpossivelVerificarTimeout('Não é possível verificar timeout')

    datetime_agora = datetime.now().astimezone()
    criado_em = datetime.fromisoformat(descript_jwt['criado_em'])

    if (datetime_agora - criado_em).seconds <= expira_em:
        return descript_jwt
    raise JwtExpirado('Tempo de uso do link expirado, favor gerar um novo')

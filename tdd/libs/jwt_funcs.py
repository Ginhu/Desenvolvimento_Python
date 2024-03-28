from datetime import datetime
import jwt
from jwt import InvalidSignatureError

from tdd.erros import TokenInvalido, ImpossivelVerificarTimeout, JwtExpirado

key = 'key'


def gera_jwt(dados: dict, dh=False, chave=key) -> str:
    dicionario = dict(dados)
    if dh:
        dicionario['criado_em'] = datetime.now().astimezone().isoformat()

    token = jwt.encode(dicionario, chave, algorithm='HS256')
    return token


def descriptografa_jwt(token: str, expira_em=0, chave=key) -> dict:
    try:
        descript_jwt = jwt.decode(token, chave, algorithms='HS256')
    except InvalidSignatureError:
        raise TokenInvalido('Token fornecido não é válido')

    if expira_em <= 0:
        return descript_jwt

    if 'criado_em' not in descript_jwt:
        raise ImpossivelVerificarTimeout('Não é possível verificar timeout')

    datetime_agora = datetime.now().astimezone()
    criado_em = datetime.fromisoformat(descript_jwt['criado_em'])

    if (datetime_agora - criado_em).seconds + 1 < expira_em:
        return descript_jwt

    raise JwtExpirado('Tempo de uso do link expirado, favor gerar um novo')

from datetime import datetime
import jwt
from jwt import InvalidSignatureError

from tdd.erros import TokenInvalido, ImpossivelVerificarTimeout, JwtExpirado

key = 'key'


def gera_jwt(dados: dict, dh: bool = False) -> str:
    if dh is False:
        token = jwt.encode(dados, key, algorithm='HS256')
        return token
    else:
        dados['criado_em'] = datetime.now().astimezone().isoformat()
        token = jwt.encode(dados, key, algorithm='HS256')
        return token


def descriptografa_jwt(token: str, expira_em: int = 0) -> dict:
    try:
        descript_jwt = jwt.decode(token, key, algorithms='HS256')
    except InvalidSignatureError:
        raise TokenInvalido('Token fornecido não é válido')

    if expira_em <= 0:
        return descript_jwt
    elif expira_em > 0 and ('criado_em' not in descript_jwt.keys()):
        raise ImpossivelVerificarTimeout('Não é possível verificar timeout')
    else:
        datetime_agora = datetime.now().astimezone()
        criado_em = datetime.fromisoformat(descript_jwt['criado_em'])

        if (datetime_agora - criado_em).seconds < expira_em:
            return descript_jwt
        else:
            raise JwtExpirado('Tempo de uso do link expirado, favor gerar um novo')

from datetime import datetime
import jwt
from jwt import InvalidSignatureError

from tdd.erros import TokenInvalido, ImpossivelVerificarTimeout

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
        pass

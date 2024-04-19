from tdd import config


def autentica_token(token):
    if not token:
        return False

    token = token.split(' ')[1]
    if token != config.token_acesso:
        return False

    return True

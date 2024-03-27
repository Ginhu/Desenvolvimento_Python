class TddErro(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)


class NaoEncontrado(TddErro):
    ...


class TokenInvalido(TddErro):
    ...


class ImpossivelVerificarTimeout(TddErro):
    ...

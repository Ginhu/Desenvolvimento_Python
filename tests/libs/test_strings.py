from tdd.libs.strings import retorna_somente_numeros


def test_retorna_somente_numeros():
    telefone_teste_não_limpo = '(11) 5515-3138qwertyuiop´[\
        ]]~çlkkjhhgfdsazxcvvbnmm,,.;/"!@#$%¨¨&*()_+{`^}?:><|!@#$%¨&*()_+=-'

    telefone_teste_limpo = '1155153138'

    assert telefone_teste_limpo == retorna_somente_numeros(telefone_teste_não_limpo)

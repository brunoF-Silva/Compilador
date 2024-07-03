# from AnalisadorLexico import AnalisadorLexico
# from AnalisadorSintatico import AnalisadorSintatico
# from AnalisadorSemantico import AnalisadorSemantico


# def main():
#     arquivo = "testes/exemplo.c"

#     analisador_lexico = AnalisadorLexico(arquivo)
#     analisador_lexico.analisar_e_mostrar_resultado()

#     tokens = analisador_lexico.obter_tokens()

#     analisador_sintatico = AnalisadorSintatico(tokens)
#     analisador_sintatico.analisar_e_traduzir()

#     analisador_semantico = AnalisadorSemantico(tokens)
#     analisador_semantico.analisar()


# if __name__ == "__main__":
#     main()

from AnalisadorLexico import AnalisadorLexico
from AnalisadorSintatico import AnalisadorSintatico, ErroSintaticoException


def main():
    arquivo = "exemplo5.c"

    analisador_lexico = AnalisadorLexico(arquivo)
    analisador_lexico.analisar_e_mostrar_resultado()

    tokens = analisador_lexico.obter_tokens()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    analisador_sintatico = AnalisadorSintatico(tokens)
    try:
        analisador_sintatico.analisar_e_traduzir()
    except ErroSintaticoException as e:
        print(e)


if __name__ == "__main__":
    main()



















# from AnalisadorLexico import AnalisadorLexico
# # from AnalisadorSintatico import AnalisadorSintatico
# from AnalisadorSemantico import AnalisadorSintatico
# def main():
#     arquivo = "testes\exemplo5.c"


#     analisador_lexico = AnalisadorLexico(arquivo)
#     analisador_lexico.analisar_e_mostrar_resultado()

#     tokens = analisador_lexico.obter_tokens()

#     analisador_sintatico = AnalisadorSintatico(tokens)
#     analisador_sintatico.analisar_e_traduzir()

# if __name__ == "__main__":
#     main()

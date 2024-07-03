'''
Curso: Ciência da Computação
Campus Universitário de Palmas
Disciplina: Compiladores
Professora Dra.: Anna Paula de Souza Parentes Rodrigues
Alunos: Bruno Ferreira da Silva e Izabela Caldeira Sena Ferreira

'''

from AnalisadorLexico import AnalisadorLexico
from AnalisadorSintaticoESemantico import AnalisadorSintatico, ErroSintaticoException


def main():
    arquivo = "exemplo1.c"

    analisador_lexico = AnalisadorLexico(arquivo)
    analisador_lexico.analisar_e_mostrar_resultado()

    tokens = analisador_lexico.obter_tokens()
    print("\nAnálise Sintática e Semântica\n")
    analisador_sintatico = AnalisadorSintatico(tokens)
    try:
        analisador_sintatico.analisar_e_traduzir()
    except ErroSintaticoException as e:
        print(e)


if __name__ == "__main__":
    main()

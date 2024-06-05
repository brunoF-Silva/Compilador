from AnalisadorLexico import AnalisadorLexico
from AnalisadorSintatico import AnalisadorSintatico

def main():
    # arquivo = "testes\exemplo.c"
    arquivo = "exemplo.c"


    analisador_lexico = AnalisadorLexico(arquivo)
    analisador_lexico.analisar_e_mostrar_resultado()

    tokens = analisador_lexico.obter_tokens()

    analisador_sintatico = AnalisadorSintatico(tokens)
    analisador_sintatico.analisar()

if __name__ == "__main__":
    main()

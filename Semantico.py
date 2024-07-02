from AnalisadorLexico import Token

class ErroSintaticoException(Exception):
    def __init__(self, token_atual, classe_esperada=None):
        self.token_atual = token_atual
        self.classe_esperada = classe_esperada

    def __str__(self):
        if self.classe_esperada is not None:
            return f"Erro sintático: Classe esperada: {self.classe_esperada}, obtida: {self.token_atual}"
        else:
            return f"Erro sintático: Token inesperado: {self.token_atual}"


class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.traducao = ""
        self.funcoes = {}
        self.variaveis = {}

    def analisar_e_traduzir(self):
        self.program()

        if self.indice < len(self.tokens):
            raise ErroSintaticoException(
                self.tokens[self.indice], "Token adicional após o fim do programa.")

        with open("traducao.py", "w") as arquivo_saida:
            arquivo_saida.write(self.traducao)

        print("Análise sintática concluída com sucesso. A tradução foi salva no arquivo 'traducao.py'.")

    def checarToken(self, tipo, valor=None):
        if self.indice >= len(self.tokens):
            return False
        token_atual = self.tokens[self.indice]
        print('checarToken vai analisar ', token_atual.tipo, token_atual.valor)
        if valor is not None:
            print('retornou  valor e tipo', valor)
            print(token_atual.tipo == tipo and token_atual.valor == valor)
            return token_atual.tipo == tipo and token_atual.valor == valor
        print('retornou só tipo: ', token_atual.tipo)
        return token_atual.tipo == tipo

    def consumir(self, tipo, valor=None):
        print('>>>>consumir chama checarToken passando', tipo, valor)
        if self.checarToken(tipo, valor):
            print(f"Consumindo token: {self.tokens[self.indice]}")
            self.indice += 1
            print('FIM DE CONSUMIR')
        else:
            return False
            token_esperado = f"{tipo}('{valor}')" if valor else tipo
            raise ErroSintaticoException(
                self.tokens[self.indice], token_esperado)

        
    def expression(self):
        print('-------nova expressão, a próxima é: ', self.tokens[self.indice+1].valor)
        self.traducao += self.tokens[self.indice].valor
        print('!!!!consumir foi chamada passando', self.tokens[self.indice].tipo, self.tokens[self.indice].valor)
        self.consumir(self.tokens[self.indice].tipo)
        print("FIM  DE EXPRESSION")
        
    def returnStmt(self):
        print("RETUUUUUUUUURRRRRRRRNNNN")
        self.consumir("Palavra reservada", "return")
        self.traducao += "return "
        if not self.checarToken("Delimitador", ";"):
            print("VAMO CHAMAR EXPRESSION POIS NADA DE ; NO RETURN")
            self.expression()
            print('++++++++++ Saiu de expression mais vamos de novo')
        self.consumir("Delimitador", ";")
        print("FIM DE RETURN STATEMENT")
        
    def program(self):
        while not self.checarToken("EOF"):
            self.declaration()
            self.traducao += "\n"
        self.consumir("EOF")

    def declaration(self):
        if self.checarToken("Palavra reservada", "fun"):
            self.funDecl()
        elif self.checarToken("Palavra reservada", "var"):
            self.varDecl()
        else:
            self.statement()

    def funDecl(self):
        self.consumir("Palavra reservada", "fun")
        nome_funcao = self.tokens[self.indice].valor
        self.consumir("Identificador")
        self.funcoes[nome_funcao] = []
        self.consumir("Delimitador", "(")
        if not self.checarToken("Delimitador", ")"):
            self.funcoes[nome_funcao] = self.parameters()
        self.consumir("Delimitador", ")")
        self.block()

    def parameters(self):
        parametros = []
        parametros.append(self.tokens[self.indice].valor)
        self.consumir("Identificador")
        while self.checarToken("Delimitador", ","):
            self.consumir("Delimitador", ",")
            parametros.append(self.tokens[self.indice].valor)
            self.consumir("Identificador")
        return parametros

    def varDecl(self):
        self.consumir("Palavra reservada", "var")
        nome_var = self.tokens[self.indice].valor
        self.consumir("Identificador")
        self.variaveis[nome_var] = None
        self.traducao += nome_var
        if self.checarToken("Operador", "="):
            self.consumir("Operador", "=")
            self.traducao += " = "
            self.expression()
        self.consumir("Delimitador", ";")
        self.traducao += "\n"

    def statement(self):
        if self.checarToken("Palavra reservada", "for"):
            self.forStmt()
        elif self.checarToken("Palavra reservada", "if"):
            self.ifStmt()
        elif self.checarToken("Palavra reservada", "print"):
            self.printStmt()
        elif self.checarToken("Palavra reservada", "return"):
            self.returnStmt()
        elif self.checarToken("Palavra reservada", "while"):
            self.whileStmt()
        elif self.checarToken("Delimitador", "{"):
            self.block()
        else:
            self.exprStmt()

    def exprStmt(self):
        self.assignment()
        if self.checarToken("Delimitador", ";"):
            self.consumir("Delimitador", ";")
            self.traducao += "\n"
        else:
            raise ErroSintaticoException(
                f"{self.tokens[self.indice].tipo} '{self.tokens[self.indice].valor}'")
# Novo código:   
    # def exprStmt(self):
    #     if self.checarToken("Palavra reservada", "return"):
    #         self.returnStmt()
    #     else:
    #         self.assignment()
    #         if self.checarToken("Delimitador", ";"):
    #             self.consumir("Delimitador", ";")
    #             self.traducao += "\n"
    #         else:
    #             raise ErroSintaticoException(
    #                 f"{self.tokens[self.indice].tipo} '{self.tokens[self.indice].valor}'")


    def forStmt(self):
        self.consumir("Palavra reservada", "for")
        self.consumir("Delimitador", "(")
        self.traducao += "for "
        if self.checarToken("Palavra reservada", "var"):
            self.varDecl()
        elif self.checarToken("Delimitador", ";"):
            self.consumir("Delimitador", ";")
            self.traducao += "; "
        else:
            self.exprStmt()
            self.traducao += "; "
        if not self.checarToken("Delimitador", ";"):
            self.expression()
        self.consumir("Delimitador", ";")
        self.traducao += "; "
        if not self.checarToken("Delimitador", ")"):
            self.expression()
        self.consumir("Delimitador", ")")
        self.statement()

    def ifStmt(self):
        self.consumir("Palavra reservada", "if")
        self.consumir("Delimitador", "(")
        self.expression()
        self.consumir("Delimitador", ")")
        self.statement()

    def printStmt(self):
        self.consumir("Palavra reservada", "print")
        self.traducao += "print("
        self.expression()
        self.traducao += ")"
        self.consumir("Delimitador", ";")

#Novo código:
    # def returnStmt(self):
    #     self.consumir("Palavra reservada", "return")
    #     self.traducao += "return "
    #     if not self.checarToken("Delimitador", ";"):
    #         self.expression()
    #     self.consumir("Delimitador", ";")


    def whileStmt(self):
        self.consumir("Palavra reservada", "while")
        self.consumir("Delimitador", "(")
        self.expression()
        self.consumir("Delimitador", ")")
        self.statement()

    def block(self):
        self.consumir("Delimitador", "{")
        while not self.checarToken("Delimitador", "}"):
            self.declaration()
        self.consumir("Delimitador", "}")

    def assignment(self):
        if self.checarToken("Identificador"):
            nome_var = self.tokens[self.indice].valor
            self.consumir("Identificador")
            if self.checarToken("Operador", "="):
                self.consumir("Operador", "=")
                if nome_var not in self.variaveis and nome_var not in self.funcoes:
                    raise ErroSintaticoException(
                        f"Variável '{nome_var}' não declarada.")
                self.traducao += nome_var + " = "
                self.assignment()
            else:
                self.primary()
        else:
            self.expression()

# código que eu me confundi (mas acho que é igual ao de baixo, portanto julgo ser o original)
# def primary(self):
#     if self.checarToken("Identificador"):
#         nome_var = self.tokens[self.indice].valor
#         if nome_var not in self.variaveis and nome_var not in self.funcoes:
#             raise ErroSintaticoException(f"Variável ou função '{nome_var}' não declarada.")
#         self.traducao += nome_var
#         self.consumir("Identificador")
#         if self.checarToken("Delimitador", "("):
#             self.consumir("Delimitador", "(")
#             if nome_var not in self.funcoes:
#                 raise ErroSintaticoException(f"'{nome_var}' não é uma função.")
#             self.argumentos()
#             self.consumir("Delimitador", ")")
#     elif self.checarToken("Constante Textual"):
#         self.traducao += self.tokens[self.indice].valor
#         self.consumir("Constante Textual")
#     elif self.checarToken("Inteiro"):
#         self.traducao += self.tokens[self.indice].valor
#         self.consumir("Inteiro")
#     elif self.checarToken("Ponto Flutuante"):
#         self.traducao += self.tokens[self.indice].valor
#         self.consumir("Ponto Flutuante")
#     elif self.checarToken("Delimitador", "("):
#         self.consumir("Delimitador", "(")
#         self.expression()
#         self.consumir("Delimitador", ")")
#     else:
#         raise ErroSintaticoException(f"Token inesperado: {self.tokens[self.indice]}")
    
#     if self.checarToken("Operador", "*") or self.checarToken("Operador", "/"):
#         self.traducao += self.tokens[self.indice].valor
#         self.consumir("Operador")

#     if self.checarToken("Operador", "+") or self.checarToken("Operador", "-"):
#         raise ErroSintaticoException(f"Operador inesperado: {self.tokens[self.indice]}")

    def primary(self):
        if self.checarToken("Identificador"):
            nome_var = self.tokens[self.indice].valor
            if nome_var not in self.variaveis and nome_var not in self.funcoes:
                raise ErroSintaticoException(
                    f"Variável ou função '{nome_var}' não declarada.")
            self.traducao += nome_var
            self.consumir("Identificador")
            if self.checarToken("Delimitador", "("):
                self.consumir("Delimitador", "(")
                if nome_var not in self.funcoes:
                    raise ErroSintaticoException(
                        f"'{nome_var}' não é uma função.")
                self.argumentos()
                self.consumir("Delimitador", ")")
        elif self.checarToken("Constante Textual"):
            self.traducao += self.tokens[self.indice].valor
            self.consumir("Constante Textual")
        elif self.checarToken("Inteiro"):
            self.traducao += self.tokens[self.indice].valor
            self.consumir("Inteiro")
        elif self.checarToken("Ponto Flutuante"):
            self.traducao += self.tokens[self.indice].valor
            self.consumir("Ponto Flutuante")
        else:
            raise ErroSintaticoException(
                f"Token inesperado: {self.tokens[self.indice]}")

    def argumentos(self):
        if not self.checarToken("Delimitador", ")"):
            self.expression()
            while self.checarToken("Delimitador", ","):
                self.consumir("Delimitador", ",")
                self.expression()

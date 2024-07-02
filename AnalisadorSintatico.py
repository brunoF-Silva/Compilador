'''
Universidade Federal do Tocantins
Campus Universitário de Palmas
Disciplina: Compiladores
Profª. Dra. Anna Paula de Souza Parentes Rodrigues
Alunos: Bruno Ferreira da Silva e Izabela Caldeira Sena Ferreira
'''
# from AnalisadorLexico import Token

# class ErroSintaticoException(Exception):
#     def __init__(self, token_atual, classe_esperada=None):
#         self.token_atual = token_atual
#         self.classe_esperada = classe_esperada

#     def __str__(self):
#         if self.classe_esperada is not None:
#             return f"Erro sintático: Classe esperada: {self.classe_esperada}, obtida: {self.token_atual}"
#         else:
#             return f"Erro sintático: Token inesperado: {self.token_atual}"

# class AnalisadorSintatico:
#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.indice = 0

#     def analisar(self):
#         self.program() 

#         if self.indice < len(self.tokens):
#             raise ErroSintaticoException(self.tokens[self.indice], "Token adicional após o fim do programa.")




#     def program(self):
#         #Enquanto não encontrar EOF, para cada token consuma 
#         while not self.checarToken(Token("Delimitador", "EOF")):
#             self.declaration() # Começa todo o processo de verificação
#         self.consumir(Token("Delimitador", "EOF"))


#     def checarToken(self, tipo, valor=None):
#         token_atual = self.tokens[self.indice]

#         if isinstance(tipo, str):
#             return token_atual.tipo == tipo and (valor is token_atual.valor or token_atual.valor == valor)
#         elif isinstance(tipo, Token):
#             return token_atual.tipo == tipo.tipo and (tipo.valor is token_atual.valor or token_atual.valor == tipo.valor)
#         else:
#             raise ErroSintaticoException(token_atual, f"Tipo de token inválido: {tipo}")

#     def declaration(self):
#         if self.checarToken(Token("Palavra reservada", "fun")):
#             self.funDecl()
#         elif self.checarToken(Token("Palavra reservada", "var")):
#             self.varDecl()
#         else:
#             self.statement()

#     def statement(self):
#         if self.checarToken(Token("Palavra reservada", "for")):
#             self.forStmt()
#         elif self.checarToken(Token("Palavra reservada", "if")):
#             self.ifStmt()
#         elif self.checarToken(Token("Palavra reservada", "print")):
#             self.printStmt()
#         elif self.checarToken(Token("Palavra reservada", "return")):
#             self.returnStmt()
#         elif self.checarToken(Token("Palavra reservada", "while")):
#             self.whileStmt()
#         elif self.checarToken(Token("Delimitador", "{")):
#             self.block()
#         else:
#             self.exprStmt()
            
#     def forStmt(self):
#         self.consumir(Token("Palavra reservada", "for"))
#         self.consumir(Token("Delimitador", "("))

#         if self.checarToken(Token("Palavra reservada", "var")):
#             self.varDecl()
#         elif self.checarToken(Token("Delimitador", ";")):
#             self.consumir(Token("Delimitador", ";"))
#         else:
#             self.exprStmt()
        
#         if not self.checarToken(Token("Delimitador", ";")):
#             self.expression() # cria um uma atribuição (assignment)
#         self.consumir(Token("Delimitador", ";"))
        
#         if not self.checarToken(Token("Delimitador", ")")):
#             self.expression()
#         self.consumir(Token("Delimitador", ")"))

#         self.statement()
    
#     def ifStmt(self):
#         self.consumir(Token("Palavra reservada", "if"))
#         self.consumir(Token("Delimitador", "("))
#         self.expression()
#         self.consumir(Token("Delimitador", ")"))

#         self.statement()

#         while self.checarToken(Token("Palavra reservada", "else")):
#             self.consumir(Token("Palavra reservada", "else"))

#             if self.checarToken(Token("Palavra reservada", "if")):
#                 self.consumir(Token("Palavra reservada", "if"))
#                 self.consumir(Token("Delimitador", "("))
#                 self.expression()
#                 self.consumir(Token("Delimitador", ")"))
#             self.statement()

#     # verifica se print está correto
#     def printStmt(self):
#         self.consumir(Token("Palavra reservada", "print"))
#         self.expression()
#         self.consumir(Token("Delimitador", ";"))

#     def returnStmt(self):
#         self.consumir(Token("Palavra reservada", "return"))
#         if not self.checarToken(Token("Delimitador", ";")):
#             self.expression()
#         self.consumir(Token("Delimitador", ";"))

#     def whileStmt(self):
#         self.consumir(Token("Palavra reservada", "while"))
#         self.consumir(Token("Delimitador", "("))
#         self.expression()
#         self.consumir(Token("Delimitador", ")"))
        
#         self.statement()

#     def block(self):
#         self.consumir(Token("Delimitador", "{"))
#         while not self.checarToken(Token("Delimitador", "}")):
#             self.declaration() # começa a verificação outra vez  
#         self.consumir(Token("Delimitador", "}"))

#     def exprStmt(self):
#         self.assignment() # Verifica uma atribuição ou a lógica or ...
#         if self.checarToken(Token("Delimitador", ";")):
#             self.consumir(Token("Delimitador", ";"))
#         else:
#             raise ErroSintaticoException(f"{self.tokens[self.indice].tipo} '{self.tokens[self.indice].valor}'")

#     def consumir(self, token_esperado):
#         if self.checarToken(token_esperado):
#             print(f"Consumindo token: {self.tokens[self.indice]}")
#             self.indice += 1
#         else:
#             raise ErroSintaticoException(self.tokens[self.indice].valor, classe_esperada=token_esperado.valor)



#     def funDecl(self):
#         self.consumir(Token("Palavra reservada", "fun"))
#         self.function()

#     def function(self):
#         self.consumir(Token("Identificador", self.tokens[self.indice].valor))
#         self.consumir(Token("Delimitador", "("))
#         if not self.checarToken(Token("Delimitador", ")")):
#             self.parameters()
#         self.consumir(Token("Delimitador", ")"))
#         self.block()

#     def parameters(self):
#         self.consumir(Token("Identificador", self.tokens[self.indice].valor))
#         while self.checarToken(Token("Delimitador", ",")):
#             self.consumir(Token("Delimitador", ","))
#             self.consumir(Token("Identificador", self.tokens[self.indice].valor))

#     def varDecl(self):
#         self.consumir(Token("Palavra reservada", "var"))
#         self.consumir(Token("Identificador", self.tokens[self.indice].valor))
#         if self.checarToken(Token("Operador", "=")):
#             self.consumir(Token("Operador", "="))
#             self.expression()
#         self.consumir(Token("Delimitador", ";"))
    
#     # Cria um assignment que é a porta de entrada para verificar, em ordem,
#     # o que um token é e se sua existência está correta para as regras da linguagem
#     def expression(self):
#         self.assignment()
        
#     # Verifica uma atribuição ou a lógica or
#     def assignment(self):
#         #Se o token for um identificador
#         if self.checarToken(Token("Identificador", self.tokens[self.indice].valor)):
#             self.consumir(Token("Identificador", self.tokens[self.indice].valor)) #consome ele pois é válido
#             if self.checarToken(Token("Operador", "=")): # Se for referente a uma atribuicao
#                 self.consumir(Token("Operador", "="))#consome o igual 
#                 self.assignment()#cria assignement  que define a operacao (+- ou outro =) para aplicar uma lógica de or
#             else:
#                 self.tokenAnterior() #retorna o valor do token anterior, decrementa o índice
#                 self.logic_or() 
#         else:
#             self.logic_or()

#     def tokenAnterior(self):
#         if self.indice > 0:
#             self.indice -= 1
#             return self.tokens[self.indice].valor
        
#     def logic_or(self):
#         # Após verificarmos a lógica and, verificaremos a lógica or
#         self.logic_and()
#         while self.checarToken(Token("Palavra reservada", "or")):
#             self.consumir(Token("Palavra reservada", "or"))
#             # Chamamos and de novo, pois além de verificar todos os outros tipos de token existentes, ele verifica a existencia de outros ands 
#             self.logic_and()
            
#     def logic_and(self):
#         #  8 - Após verificar um token com todas as suas possibilidades de existência, verificamos a lógica and
#         self.equality()
#         while self.checarToken(Token("Palavra reservada", "and")):
#             self.consumir(Token("Palavra reservada", "and"))
#             # Se for uma palavra and verifique os operadores após and
#             self.equality()

#     def equality(self): # 7 - Consome operadores de igualdade
#         self.comparison()
#         while self.checarToken(Token("Operador", "!=")) or self.checarToken(Token("Operador", "==")):
#             if self.checarToken(Token("Operador", "!=")):
#                 self.consumir(Token("Operador", "!="))
#             elif self.checarToken(Token("Operador", "==")):
#                 self.consumir(Token("Operador", "=="))
#             else:
#                 raise ErroSintaticoException(self.tokens[self.indice], "Operador de inválido")

#             self.comparison()

#     def comparison(self): # 6 - Consome operadores de comparação
#         self.term()
#         while self.checarToken(Token("Operador", ">")) or self.checarToken(Token("Operador", ">=")) or \
#             self.checarToken(Token("Operador", "<")) or self.checarToken(Token("Operador", "<=")):
#             if self.checarToken(Token("Operador", ">")):
#                 self.consumir(Token("Operador", ">"))
#             elif self.checarToken(Token("Operador", ">=")):
#                 self.consumir(Token("Operador", ">="))
#             elif self.checarToken(Token("Operador", "<")):
#                 self.consumir(Token("Operador", "<"))
#             elif self.checarToken(Token("Operador", "<=")):
#                 self.consumir(Token("Operador", "<="))
#             else:
#                 raise ErroSintaticoException(self.tokens[self.indice], "Operador de inválido")

#             self.term()

#     def term(self): # 5 - Consome operações de adição e subtração
#         self.factor()
#         while self.checarToken(Token("Operador", "+")) or self.checarToken(Token("Operador", "-")):
#             if self.checarToken(Token("Operador", "+")):
#                 self.consumir(Token("Operador", "+"))
#             elif self.checarToken(Token("Operador", "-")):
#                 self.consumir(Token("Operador", "-"))
#             else:
#                 raise ErroSintaticoException(self.tokens[self.indice], "Operador de inválido")

#             self.factor()

#     def factor(self): # 4 - Consome operações de divisão e multiplicação
#         self.unary()
#         while self.checarToken(Token("Operador", "/")) or self.checarToken(Token("Operador", "*")):
#             if self.checarToken(Token("Operador", "/")):
#                 self.consumir(Token("Operador", "/"))
#             elif self.checarToken(Token("Operador", "*")):
#                 self.consumir(Token("Operador", "*"))
#             else: # esse erro nao faz sentido
#                 raise ErroSintaticoException(self.tokens[self.indice], "Operador de inválido")

#             self.unary()

#     def unary(self): # 1 - verifica se o token atual é operador unário ou chama call
#         if self.checarToken(Token("Operador", "!")):
#             self.consumir(Token("Operador", "!"))
#             self.unary()
#         elif self.checarToken(Token("Operador", "-")):
#             self.consumir(Token("Operador", "-"))
#             self.unary()
#         else:
#             self.call()

#     def call(self): # 3 - Lógica da chamada de métodos e funções
#         self.primary()
#         while self.checarToken(Token("Delimitador", "(")) or self.checarToken(Token("Operador", ".")):
#             if self.checarToken(Token("Delimitador", "(")):
#                 self.consumir(Token("Delimitador", "("))
#                 if not self.checarToken(Token("Delimitador", ")")):
#                     self.arguments() # Verifica a lógica dos argumentos
#                 self.consumir(Token("Delimitador", ")"))
#             else:
#                 self.consumir(Token("Operador", "."))
#                 self.consumir(Token("Identificador", self.tokens[self.indice].valor))
#                 if self.checarToken(Token("Delimitador", "(")):
#                     self.consumir(Token("Delimitador", "("))
#                     if not self.checarToken(Token("Delimitador", ")")):
#                         self.arguments()
#                     self.consumir(Token("Delimitador", ")"))

#     def primary(self): # 2 - Consome tudo que não precisa de lógica (menos ())
#         if self.checarToken(Token("Palavra reservada", "true")):
#             self.consumir(Token("Palavra reservada", "true"))
#         elif self.checarToken(Token("Palavra reservada", "false")):
#             self.consumir(Token("Palavra reservada", "false"))
#         elif self.checarToken(Token("Palavra reservada", "nil")):
#             self.consumir(Token("Palavra reservada", "nil"))
#         elif self.checarToken(Token("Palavra reservada", "this")):
#             self.consumir(Token("Palavra reservada", "this"))
#         elif self.checarToken(Token("Inteiro", self.tokens[self.indice].valor)):
#             self.consumir(Token("Inteiro", self.tokens[self.indice].valor))
#         elif self.checarToken(Token("Ponto Flutuante", self.tokens[self.indice].valor)):
#             self.consumir(Token("Ponto Flutuante", self.tokens[self.indice].valor))
#         elif self.checarToken(Token("Constante Textual", self.tokens[self.indice].valor)):
#             self.consumir(Token("Constante Textual", self.tokens[self.indice].valor))
#         elif self.checarToken(Token("Identificador", self.tokens[self.indice].valor)):
#             self.consumir(Token("Identificador", self.tokens[self.indice].valor))
#         elif self.checarToken(Token("Delimitador", "(")):
#             self.consumir(Token("Delimitador", "("))
#             self.expression() # Cria outro arguments e começa tudo outra vez
#             self.consumir(Token("Delimitador", ")"))
#         elif self.checarToken(Token("Palavra reservada", "super")):
#             self.consumir(Token("Palavra reservada", "super"))
#             self.consumir(Token("Operador", "."))
#             self.consumir(Token("Identificador", self.tokens[self.indice -1].valor))
#         else:
#             raise ErroSintaticoException(f"{self.tokens[self.indice].tipo} '{self.tokens[self.indice].valor}'")
        
        
#     def arguments(self):
#         self.expression()
        
#         while self.checarToken(Token("Delimitador", ",")):
#             self.consumir(Token("Delimitador", ","))
#             self.expression()


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

    def analisar_e_traduzir(self):
        self.program()

        if self.indice < len(self.tokens):
            raise ErroSintaticoException(
                self.tokens[self.indice], "Token adicional após o fim do programa.")

        with open("traducao.py", "w") as arquivo_saida:
            arquivo_saida.write(self.traducao)

        print("Análise sintática concluída com sucesso. A tradução foi salva no arquivo 'traducao.py'.")

    # def checarToken(self, tipo, valor=None):
    #     token_atual = self.tokens[self.indice]

    #     if isinstance(tipo, str):
    #         return token_atual.tipo == tipo and (valor is token_atual.valor or token_atual.valor == valor)
    #     elif isinstance(tipo, Token):
    #         return token_atual.tipo == tipo.tipo and (tipo.valor is token_atual.valor or token_atual.valor == tipo.valor)
    #     else:
    #         raise ErroSintaticoException(
    #             token_atual, f"Tipo de token inválido: {tipo}")
    def checarToken(self, tipo, valor=None):
        token_atual = self.tokens[self.indice]

        if valor is not None:
            return token_atual.tipo == tipo and token_atual.valor == valor
        else:
            return token_atual.tipo == tipo
        
    def consumir(self, token_esperado):
        if self.checarToken(token_esperado):
            print(f"Consumindo token: {self.tokens[self.indice]}")
            self.indice += 1
        else:
            raise ErroSintaticoException(
                self.tokens[self.indice].valor, classe_esperada=token_esperado.valor)

    def program(self):
        while not self.checarToken(Token("Delimitador", "EOF")):
            self.declaration()
            self.traducao += "\n"
        self.consumir(Token("Delimitador", "EOF"))

    def declaration(self):
        if self.checarToken(Token("Palavra reservada", "fun")):
            self.funDecl()
        elif self.checarToken(Token("Palavra reservada", "var")):
            self.varDecl()
        else:
            self.statement()

    def funDecl(self):
        self.consumir(Token("Palavra reservada", "fun"))
        self.function()

    def varDecl(self):
        self.consumir(Token("Palavra reservada", "var"))
        self.consumir(Token("Identificador", self.tokens[self.indice].valor))
        self.traducao += self.tokens[self.indice - 1].valor
        if self.checarToken(Token("Operador", "=")):
            self.consumir(Token("Operador", "="))
            self.traducao += " = "
            self.expression()
        self.consumir(Token("Delimitador", ";"))
        self.traducao += "\n"

    def statement(self):
        if self.checarToken(Token("Palavra reservada", "for")):
            self.forStmt()
        elif self.checarToken(Token("Palavra reservada", "if")):
            self.ifStmt()
        elif self.checarToken(Token("Palavra reservada", "print")):
            self.printStmt()
        elif self.checarToken(Token("Palavra reservada", "return")):
            self.returnStmt()
        elif self.checarToken(Token("Palavra reservada", "while")):
            self.whileStmt()
        elif self.checarToken(Token("Delimitador", "{")):
            self.block()
        else:
            self.exprStmt()

    def exprStmt(self):
        self.assignment()
        if self.checarToken(Token("Delimitador", ";")):
            self.consumir(Token("Delimitador", ";"))
            self.traducao += "\n"
        else:
            raise ErroSintaticoException(
                f"{self.tokens[self.indice].tipo} '{self.tokens[self.indice].valor}'")

    def forStmt(self):
        self.consumir(Token("Palavra reservada", "for"))
        self.consumir(Token("Delimitador", "("))
        self.traducao += "for "
        if self.checarToken(Token("Palavra reservada", "var")):
            self.varDecl()
        elif self.checarToken(Token("Delimitador", ";")):
            self.consumir(Token("Delimitador", ";"))
            self.traducao += "; "
        else:
            self.exprStmt()
            self.traducao += "; "
        if not self.checarToken(Token("Delimitador", ";")):
            self.expression()
        self.consumir(Token("Delimitador", ";"))
        self.traducao += "; "
        if not self.checarToken(Token("Delimitador", ")")):
            self.expression()
        self.consumir(Token("Delimitador", ")"))
        self.traducao += ":\n"

        self.statement()

    def ifStmt(self):
        self.consumir(Token("Palavra reservada", "if"))
        self.consumir(Token("Delimitador", "("))
        self.traducao += "if "
        self.expression()
        self.consumir(Token("Delimitador", ")"))

        self.statement()
        self.traducao += "\n"

        while self.checarToken(Token("Palavra reservada", "else")):
            self.consumir(Token("Palavra reservada", "else"))

            if self.checarToken(Token("Palavra reservada", "if")):
                self.traducao += "elif "
                self.consumir(Token("Palavra reservada", "if"))
                self.consumir(Token("Delimitador", "("))
                self.expression()
                self.consumir(Token("Delimitador", ")"))
            else:
                self.traducao += "else"

            self.statement()
            self.traducao += "\n"

    def printStmt(self):
        self.consumir(Token("Palavra reservada", "print"))
        self.traducao += "print("
        self.expression()
        self.traducao += ")"
        self.consumir(Token("Delimitador", ";"))

    def returnStmt(self):
        self.consumir(Token("Palavra reservada", "return"))
        self.traducao += "return "
        if not self.checarToken(Token("Delimitador", ";")):
            self.expression()
        self.consumir(Token("Delimitador", ";"))

    def whileStmt(self):
        self.consumir(Token("Palavra reservada", "while"))
        self.traducao += "while "
        self.consumir(Token("Delimitador", "("))
        self.expression()
        self.consumir(Token("Delimitador", ")"))

        self.statement()

    def block(self):
        self.consumir(Token("Delimitador", "{"))
        self.traducao += ":\n"
        self.traducao += "\t"
        while not self.checarToken(Token("Delimitador", "}")):
            self.declaration()
        self.consumir(Token("Delimitador", "}"))

    def expression(self):
        self.assignment()

    def assignment(self):

        if self.checarToken(Token("Identificador", self.tokens[self.indice].valor)):
            self.consumir(
                Token("Identificador", self.tokens[self.indice].valor))
            # self.traducao += self.tokens[self.indice - 1].valor
            if self.checarToken(Token("Operador", "=")):
                self.traducao += self.tokens[self.indice - 1].valor
                self.consumir(Token("Operador", "="))
                self.traducao += " = "
                self.assignment()
            else:
                self.tokenAnterior()
                self.logic_or()
        else:
            self.logic_or()

    def logic_or(self):
        self.logic_and()
        while self.checarToken(Token("Palavra reservada", "or")):
            self.consumir(Token("Palavra reservada", "or"))
            self.traducao += " or "
            self.logic_and()

    def logic_and(self):
        self.equality()
        while self.checarToken(Token("Palavra reservada", "and")):
            self.consumir(Token("Palavra reservada", "and"))
            self.traducao += " and "
            self.equality()

    def equality(self):
        self.comparison()
        while self.checarToken(Token("Operador", "!=")) or self.checarToken(Token("Operador", "==")):
            if self.checarToken(Token("Operador", "!=")):
                self.consumir(Token("Operador", "!="))
                self.traducao += " != "
            elif self.checarToken(Token("Operador", "==")):
                self.consumir(Token("Operador", "=="))
                self.traducao += " == "
            else:
                raise ErroSintaticoException(
                    self.tokens[self.indice], "Operador de inválido")

            self.comparison()

    def comparison(self):
        self.term()
        while self.checarToken(Token("Operador", ">")) or self.checarToken(Token("Operador", ">=")) or \
                self.checarToken(Token("Operador", "<")) or self.checarToken(Token("Operador", "<=")):
            if self.checarToken(Token("Operador", ">")):
                self.consumir(Token("Operador", ">"))
                self.traducao += " > "
            elif self.checarToken(Token("Operador", ">=")):
                self.consumir(Token("Operador", ">="))
                self.traducao += " >= "
            elif self.checarToken(Token("Operador", "<")):
                self.consumir(Token("Operador", "<"))
                self.traducao += " < "
            elif self.checarToken(Token("Operador", "<=")):
                self.consumir(Token("Operador", "<="))
                self.traducao += " <= "
            else:
                raise ErroSintaticoException(
                    self.tokens[self.indice], "Operador de inválido")

            self.term()

    def term(self):
        self.factor()
        while self.checarToken(Token("Operador", "+")) or self.checarToken(Token("Operador", "-")):
            if self.checarToken(Token("Operador", "+")):
                self.consumir(Token("Operador", "+"))
                self.traducao += " + "
            elif self.checarToken(Token("Operador", "-")):
                self.consumir(Token("Operador", "-"))
                self.traducao += " - "
            else:
                raise ErroSintaticoException(
                    self.tokens[self.indice], "Operador de inválido")

            self.factor()

    def factor(self):
        self.unary()
        while self.checarToken(Token("Operador", "/")) or self.checarToken(Token("Operador", "*")):
            if self.checarToken(Token("Operador", "/")):
                self.consumir(Token("Operador", "/"))
                self.traducao += " / "
            elif self.checarToken(Token("Operador", "*")):
                self.consumir(Token("Operador", "*"))
                self.traducao += " * "
            else:
                raise ErroSintaticoException(
                    self.tokens[self.indice], "Operador de inválido")

            self.unary()

    def unary(self):
        if self.checarToken(Token("Operador", "!")):
            self.consumir(Token("Operador", "!"))
            self.traducao += "not "
            self.unary()
        elif self.checarToken(Token("Operador", "-")):
            self.consumir(Token("Operador", "-"))
            self.traducao += "-"
            self.unary()
        else:
            self.call()

    def call(self):
        self.primary()
        while self.checarToken(Token("Delimitador", "(")) or self.checarToken(Token("Operador", ".")):
            if self.checarToken(Token("Delimitador", "(")):
                self.consumir(Token("Delimitador", "("))
                self.traducao += "("
                if not self.checarToken(Token("Delimitador", ")")):
                    self.arguments()
                self.consumir(Token("Delimitador", ")"))
                self.traducao += ")"
            else:
                self.consumir(Token("Operador", "."))
                self.traducao += "."
                self.consumir(
                    Token("Identificador", self.tokens[self.indice].valor))
                self.traducao += self.tokens[self.indice].valor
                if self.checarToken(Token("Delimitador", "(")):
                    self.consumir(Token("Delimitador", "("))
                    self.traducao += "("
                    if not self.checarToken(Token("Delimitador", ")")):
                        self.arguments()
                    self.consumir(Token("Delimitador", ")"))
                    self.traducao += ")"

    def primary(self):
        if self.checarToken(Token("Palavra reservada", "true")):
            self.consumir(Token("Palavra reservada", "true"))
            self.traducao += "True"
        elif self.checarToken(Token("Palavra reservada", "false")):
            self.consumir(Token("Palavra reservada", "false"))
            self.traducao += "False"
        elif self.checarToken(Token("Palavra reservada", "nil")):
            self.consumir(Token("Palavra reservada", "nil"))
            self.traducao += "None"
        elif self.checarToken(Token("Palavra reservada", "this")):
            self.consumir(Token("Palavra reservada", "this"))
            self.traducao += "self"
        elif self.checarToken(Token("Inteiro", self.tokens[self.indice].valor)):
            self.consumir(Token("Inteiro", self.tokens[self.indice].valor))
            self.traducao += self.tokens[self.indice - 1].valor
        elif self.checarToken(Token("Ponto Flutuante", self.tokens[self.indice].valor)):
            self.consumir(
                Token("Ponto Flutuante", self.tokens[self.indice].valor))
            self.traducao += self.tokens[self.indice - 1].valor
        elif self.checarToken(Token("Constante Textual", self.tokens[self.indice].valor)):
            self.consumir(Token("Constante Textual",
                          self.tokens[self.indice].valor))
            self.traducao += self.tokens[self.indice - 1].valor
        elif self.checarToken(Token("Identificador", self.tokens[self.indice].valor)):
            self.consumir(
                Token("Identificador", self.tokens[self.indice].valor))
            self.traducao += self.tokens[self.indice - 1].valor
        elif self.checarToken(Token("Delimitador", "(")):
            self.consumir(Token("Delimitador", "("))
            self.expression()
            self.consumir(Token("Delimitador", ")"))
        elif self.checarToken(Token("Palavra reservada", "super")):
            self.consumir(Token("Palavra reservada", "super"))
            self.traducao += "super."
            self.consumir(Token("Operador", "."))
            self.consumir(
                Token("Identificador", self.tokens[self.indice - 1].valor))
            self.traducao += self.tokens[self.indice - 1].valor
        else:
            raise ErroSintaticoException(
                f"{self.tokens[self.indice].tipo} '{self.tokens[self.indice].valor}'")

    def function(self):
        self.consumir(Token("Identificador", self.tokens[self.indice].valor))
        self.traducao += "def " + self.tokens[self.indice - 1].valor
        self.consumir(Token("Delimitador", "("))
        self.traducao += "("
        if not self.checarToken(Token("Delimitador", ")")):
            self.parameters()
        self.consumir(Token("Delimitador", ")"))
        self.traducao += ")"
        self.block()

    def parameters(self):
        self.consumir(Token("Identificador", self.tokens[self.indice].valor))
        self.traducao += self.tokens[self.indice - 1].valor
        while self.checarToken(Token("Delimitador", ",")):
            self.consumir(Token("Delimitador", ","))
            self.traducao += ", "
            self.consumir(
                Token("Identificador", self.tokens[self.indice].valor))
            self.traducao += self.tokens[self.indice - 1].valor

    def arguments(self):
        self.expression()

        while self.checarToken(Token("Delimitador", ",")):
            self.consumir(Token("Delimitador", ","))
            self.traducao += ", "
            self.expression()

    def tokenAnterior(self):
        if self.indice > 0:
            self.indice -= 1
            return self.tokens[self.indice].valor

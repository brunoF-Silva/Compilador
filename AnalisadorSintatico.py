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
        self.variaveis_declaradas = set()
        self.var_int = set()
        self.var_float = set()
        self.var_str = set()

    def analisar_e_traduzir(self):
        self.program()

        if self.indice < len(self.tokens):
            raise ErroSintaticoException(
                self.tokens[self.indice], "Token adicional após o fim do programa.")

        with open("traducao.py", "w") as arquivo_saida:
            arquivo_saida.write(self.traducao)

        print("Análise sintática concluída com sucesso. A tradução foi salva no arquivo 'traducao.py'.")

    def checarToken(self, tipo, valor=None):
        token_atual = self.tokens[self.indice]

        if isinstance(tipo, str):
            return token_atual.tipo == tipo and (valor is token_atual.valor or token_atual.valor == valor)
        elif isinstance(tipo, Token):
            return token_atual.tipo == tipo.tipo and (tipo.valor is token_atual.valor or token_atual.valor == tipo.valor)
        else:
            raise ErroSintaticoException(
                token_atual, f"Tipo de token inválido: {tipo}")

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
        elif self.checarToken(Token("Palavra reservada", "int")):
            self.varDecl()
        elif self.checarToken(Token("Palavra reservada", "float")):
            self.varDecl()
        elif self.checarToken(Token("Palavra reservada", "var")):
            self.varDecl()
        else:
            self.statement()

    def funDecl(self):
        self.consumir(Token("Palavra reservada", "fun"))
        self.function()

    def varDecl(self):
        print('Declaração ', self.tokens[self.indice].valor)
        if self.checarToken('Palavra reservada', 'int'):
            identificador = self.tokens[self.indice].valor
            self.consumir(Token("Palavra reservada", "int"))
            if self.indice + 1 < len(self.tokens):
                if self.tokens[self.indice+1].valor == '=':
                    if self.indice + 2 < len(self.tokens):
                        if isinstance(self.converter_texto(self.tokens[self.indice+2].valor), int):
                            self.var_int.add(self.tokens[self.indice].valor)
                            
                        else:
                            raise ErroSintaticoException(
                                f"Variável '{self.tokens[self.indice].valor}' não é do tipo inteiro.")
                            
        if self.checarToken('Palavra reservada', 'float'):
            identificador = self.tokens[self.indice].valor
            self.consumir(Token("Palavra reservada", "float"))
            if self.indice + 1 < len(self.tokens):
                if self.tokens[self.indice+1].valor == '=':
                    if self.indice + 2 < len(self.tokens):
                        if isinstance(self.converter_texto(self.tokens[self.indice+2].valor), float):
                            self.var_float.add(self.tokens[self.indice].valor)
                        else:
                            raise ErroSintaticoException(
                                f"Variável '{self.tokens[self.indice].valor}' não é do tipo float.")
                            
        if self.checarToken('Palavra reservada', 'var'):
            identificador = self.tokens[self.indice].valor
            self.consumir(Token("Palavra reservada", "var"))
            if self.indice + 1 < len(self.tokens):
                if self.tokens[self.indice+1].valor == '=':
                    if self.indice + 2 < len(self.tokens):
                        if isinstance(self.converter_texto(self.tokens[self.indice+2].valor), str):
                            self.var_str.add(self.tokens[self.indice].valor)

                        else:
                            raise ErroSintaticoException(
                                f"Variável '{self.tokens[self.indice].valor}' não é do tipo str.")
        
        # self.consumir(Token("Palavra reservada", "var"))
        identificador = self.tokens[self.indice].valor
        self.consumir(Token("Identificador", self.tokens[self.indice].valor))
        self.variaveis_declaradas.add(identificador)
        self.traducao += self.tokens[self.indice - 1].valor
        if self.checarToken(Token("Operador", "=")):
            self.consumir(Token("Operador", "="))
            self.traducao += " = "
            self.expression()
        self.consumir(Token("Delimitador", ";"))
        self.traducao += "\n"
        
    def assignment(self):
        print('ATRIBUICAO')
        if self.checarToken(Token("Identificador", self.tokens[self.indice].valor)):
            print('AAAAAAAAAA---------------------------- ', self.var_float)
            identificador = self.tokens[self.indice].valor
            print(identificador)
            if identificador not in self.variaveis_declaradas:
                raise ErroSintaticoException(
                    f"Variável '{identificador}' não declarada.")
                
            if identificador in self.var_int:
                if self.indice + 1 < len(self.tokens):
                    if self.tokens[self.indice+1].valor == '=':
                        if self.indice + 2 < len(self.tokens):
                            print('!!!!!!!!!!vamos ver ', self.tokens[self.indice+2].valor)
                            if isinstance(self.converter_texto(self.tokens[self.indice+2].valor), int) and identificador in self.var_int:
                                print('É INTTTTTTTTT')
                            else:
                                raise ErroSintaticoException(
                                    f"Variável '{self.tokens[self.indice].valor}' não é do tipo inteiro.")
                                
            if identificador in self.var_float:
                print('CUUUUUU')
                if self.indice + 1 < len(self.tokens):
                    if self.tokens[self.indice+1].valor == '=':
                        if self.indice + 2 < len(self.tokens):
                            print('!!!!!!!!!!vamos ver ', self.tokens[self.indice+2].valor)
                            if isinstance(self.converter_texto(self.tokens[self.indice+2].valor), float) and identificador in self.var_float:
                                print('É float')
                            else:
                                raise ErroSintaticoException(
                                    f"Variável '{self.tokens[self.indice].valor}' não é do tipo float.")
                                
            if identificador in self.var_str:
                if self.indice + 1 < len(self.tokens):
                    if self.tokens[self.indice+1].valor == '=':
                        if self.indice + 2 < len(self.tokens):
                            print('!!!!!!!!!!vamos ver ', self.tokens[self.indice+2].valor)
                            if isinstance(self.converter_texto(self.tokens[self.indice+2].valor), str) and identificador in self.var_str:
                                print('É float')
                            else:
                                raise ErroSintaticoException(
                                    f"Variável '{self.tokens[self.indice].valor}' não é do tipo float.")
            self.consumir(
                Token("Identificador", self.tokens[self.indice].valor))
            # self.traducao += self.tokens[self.indice - 1].valor
            if self.checarToken(Token("Operador", "=")):
                print('jjjjjjj')
                self.traducao += self.tokens[self.indice - 1].valor
                self.consumir(Token("Operador", "="))
                self.traducao += " = "
                self.assignment()
            else:
                print('kkkkkk')
                self.tokenAnterior()
                self.logic_or()
        else:
            self.logic_or()
    # def assignment(self):
    #     print('OI')
    #     if self.checarToken(Token("Identificador", self.tokens[self.indice].valor)):
    #         print('oiiii')
    #         identificador = self.tokens[self.indice].valor
    #         if identificador not in self.variaveis_declaradas:
    #             raise ErroSintaticoException(
    #                 f"Variável '{identificador}' não declarada.")
    #         self.consumir(
    #             Token("Identificador", self.tokens[self.indice].valor))
    #         # self.traducao += self.tokens[self.indice - 1].valor
    #         if self.checarToken(Token("Operador", "=")):
    #             self.traducao += self.tokens[self.indice - 1].valor
    #             self.consumir(Token("Operador", "="))
    #             self.traducao += " = "
    #             self.assignment()
    #         else:
    #             self.tokenAnterior()
    #             self.logic_or()
    #     else:
    #         print('oi')
    #         self.logic_or()
            
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


    def converter_texto(self, texto):
        try:
            # Tenta converter para inteiro
            valor = int(texto)
            return valor
        except ValueError:
            try:
                # Se falhar, tenta converter para ponto flutuante
                valor = float(texto)
                return valor
            except ValueError:
                # Se ambos falharem, retorna como texto
                return texto


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
        print('_______________')
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
        elif self.checarToken(Token("Numero", self.tokens[self.indice].valor)):
            self.consumir(Token("Numero", self.tokens[self.indice].valor))
            self.traducao += self.tokens[self.indice - 1].valor
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
            identificador = self.tokens[self.indice].valor
            if identificador not in self.variaveis_declaradas:
                raise ErroSintaticoException(
                    f"Variável '{identificador}' não declarada.")
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
        identificador = self.tokens[self.indice].valor
        self.variaveis_declaradas.add(identificador)
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
        print('------->')
        # identificador = self.tokens[self.indice].valor
        # self.variaveis_declaradas.add(identificador)
        if(self.checarToken("Palavra reservada", "int")):
            self.consumir(Token("Palavra reservada", "int"))
            identificador = self.tokens[self.indice].valor
            self.variaveis_declaradas.add(identificador)
            self.var_int.add(identificador)
            self.consumir(Token("Identificador", self.tokens[self.indice].valor))
            self.traducao += self.tokens[self.indice - 1].valor
            while self.checarToken(Token("Delimitador", ",")):
                self.consumir(Token("Delimitador", ","))
                self.traducao += ", "
                self.consumir(
                    Token("Identificador", self.tokens[self.indice].valor))
                self.traducao += self.tokens[self.indice - 1].valor
        if(self.checarToken("Palavra reservada", "var")):
            self.consumir(Token("Palavra reservada", "var"))
            identificador = self.tokens[self.indice].valor
            self.var_txt.add(identificador)
            self.consumir(Token("Identificador", self.tokens[self.indice].valor))
            self.traducao += self.tokens[self.indice - 1].valor
            while self.checarToken(Token("Delimitador", ",")):
                self.consumir(Token("Delimitador", ","))
                self.traducao += ", "
                self.consumir(
                    Token("Identificador", self.tokens[self.indice].valor))
                self.traducao += self.tokens[self.indice - 1].valor

    def arguments(self):
        print('UUUUUUUUUUU')
        self.expression()

        while self.checarToken(Token("Delimitador", ",")):
            self.consumir(Token("Delimitador", ","))
            self.traducao += ", "
            self.expression(True)
            
    def tokenAnterior(self):
            if self.indice > 0:
                self.indice -= 1
                return self.tokens[self.indice].valor
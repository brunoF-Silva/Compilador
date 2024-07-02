class ErroSemanticoException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Erro semântico: {self.message}"


class AnalisadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.symbol_table = SymbolTable()

    def analisar(self):
        self.program()

    def checarToken(self, tipo, valor=None):
        token_atual = self.tokens[self.indice]

        if valor is not None:
            return token_atual.tipo == tipo and token_atual.valor == valor
        else:
            return token_atual.tipo == tipo

    def consumir(self, token_esperado):
        if self.checarToken(token_esperado.tipo, token_esperado.valor):
            self.indice += 1
        else:
            raise ErroSintaticoException(
                self.tokens[self.indice], token_esperado)

    def program(self):
        while not self.checarToken("Delimitador", "EOF"):
            self.declaration()
        self.consumir(Token("Delimitador", "EOF", 0, 0))

    def declaration(self):
        if self.checarToken("Palavra reservada", "fun"):
            self.funDecl()
        elif self.checarToken("Palavra reservada", "var"):
            self.varDecl()
        else:
            self.statement()

    def funDecl(self):
        self.consumir(Token("Palavra reservada", "fun", 0, 0))
        name = self.tokens[self.indice].valor
        self.consumir(Token("Identificador", name, 0, 0))
        self.symbol_table.declare(name, "function")
        self.consumir(Token("Delimitador", "(", 0, 0))
        self.symbol_table.enter_scope()
        if not self.checarToken("Delimitador", ")"):
            self.parameters()
        self.consumir(Token("Delimitador", ")", 0, 0))
        self.block()
        self.symbol_table.leave_scope()

    def varDecl(self):
        self.consumir(Token("Palavra reservada", "var", 0, 0))
        name = self.tokens[self.indice].valor
        self.consumir(Token("Identificador", name, 0, 0))
        if self.checarToken("Operador", "="):
            self.consumir(Token("Operador", "=", 0, 0))
            self.expression()
        self.symbol_table.declare(name, "variable")
        self.consumir(Token("Delimitador", ";", 0, 0))

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
        self.expression()
        self.consumir(Token("Delimitador", ";", 0, 0))

    def forStmt(self):
        self.consumir(Token("Palavra reservada", "for", 0, 0))
        self.consumir(Token("Delimitador", "(", 0, 0))
        self.symbol_table.enter_scope()
        if self.checarToken("Palavra reservada", "var"):
            self.varDecl()
        elif self.checarToken("Delimitador", ";"):
            self.consumir(Token("Delimitador", ";", 0, 0))
        else:
            self.exprStmt()
        if not self.checarToken("Delimitador", ";"):
            self.expression()
        self.consumir(Token("Delimitador", ";", 0, 0))
        if not self.checarToken("Delimitador", ")"):
            self.expression()
        self.consumir(Token("Delimitador", ")", 0, 0))
        self.statement()
        self.symbol_table.leave_scope()

    def ifStmt(self):
        self.consumir(Token("Palavra reservada", "if", 0, 0))
        self.consumir(Token("Delimitador", "(", 0, 0))
        self.expression()
        self.consumir(Token("Delimitador", ")", 0, 0))
        self.statement()
        while self.checarToken("Palavra reservada", "else"):
            self.consumir(Token("Palavra reservada", "else", 0, 0))
            if self.checarToken("Palavra reservada", "if"):
                self.consumir(Token("Palavra reservada", "if", 0, 0))
                self.consumir(Token("Delimitador", "(", 0, 0))
                self.expression()
                self.consumir(Token("Delimitador", ")", 0, 0))
            self.statement()

    def printStmt(self):
        self.consumir(Token("Palavra reservada", "print", 0, 0))
        self.expression()
        self.consumir(Token("Delimitador", ";", 0, 0))

    def returnStmt(self):
        self.consumir(Token("Palavra reservada", "return", 0, 0))
        if not self.checarToken("Delimitador", ";"):
            self.expression()
        self.consumir(Token("Delimitador", ";", 0, 0))

    def whileStmt(self):
        self.consumir(Token("Palavra reservada", "while", 0, 0))
        self.consumir(Token("Delimitador", "(", 0, 0))
        self.expression()
        self.consumir(Token("Delimitador", ")", 0, 0))
        self.statement()

    def block(self):
        self.consumir(Token("Delimitador", "{", 0, 0))
        self.symbol_table.enter_scope()
        while not self.checarToken("Delimitador", "}"):
            self.declaration()
        self.consumir(Token("Delimitador", "}", 0, 0))
        self.symbol_table.leave_scope()

    def expression(self):
        self.assignment()

    def assignment(self):
        if self.checarToken("Identificador", self.tokens[self.indice].valor):
            name = self.tokens[self.indice].valor
            self.consumir(Token("Identificador", name, 0, 0))
            if self.checarToken("Operador", "="):
                self.consumir(Token("Operador", "=", 0, 0))
                self.assignment()
                var_type = self.symbol_table.lookup(name)
                if var_type is None:
                    raise ErroSemanticoException(
                        f"Variável '{name}' não declarada")
            else:
                self.tokenAnterior()
                self.logic_or()
        else:
            self.logic_or()

    def logic_or(self):
        self.logic_and()
        while self.checarToken("Palavra reservada", "or"):
            self.consumir(Token("Palavra reservada", "or", 0, 0))
            self.logic_and()

    def logic_and(self):
        self.equality()
        while self.checarToken("Palavra reservada", "and"):
            self.consumir(Token("Palavra reservada", "and", 0, 0))
            self.equality()

    def equality(self):
        self.comparison()
        while self.checarToken("Operador", "==") or self.checarToken("Operador", "!="):
            if self.checarToken("Operador", "=="):
                self.consumir(Token("Operador", "==", 0, 0))
            elif self.checarToken("Operador", "!="):
                self.consumir(Token("Operador", "!=", 0, 0))
            self.comparison()

    def comparison(self):
        self.term()
        while self.checarToken("Operador", ">") or self.checarToken("Operador", ">=") or self.checarToken("Operador", "<") or self.checarToken("Operador", "<="):
            if self.checarToken("Operador", ">"):
                self.consumir(Token("Operador", ">", 0, 0))
            elif self.checarToken("Operador", ">="):
                self.consumir(Token("Operador", ">=", 0, 0))
            elif self.checarToken("Operador", "<"):
                self.consumir(Token("Operador", "<", 0, 0))
            elif self.checarToken("Operador", "<="):
                self.consumir(Token("Operador", "<=", 0, 0))
            else:
                raise ErroSemanticoException(f"Operador inválido")
            self.term()

    def term(self):
        self.factor()
        while self.checarToken("Operador", "+") or self.checarToken("Operador", "-"):
            if self.checarToken("Operador", "+"):
                self.consumir(Token("Operador", "+", 0, 0))
            elif self.checarToken("Operador", "-"):
                self.consumir(Token("Operador", "-", 0, 0))
            else:
                raise ErroSemanticoException(f"Operador inválido")
            self.factor()

    def factor(self):
        self.unary()
        while self.checarToken("Operador", "*") or self.checarToken("Operador", "/"):
            if self.checarToken("Operador", "*"):
                self.consumir(Token("Operador", "*", 0, 0))
            elif self.checarToken("Operador", "/"):
                self.consumir(Token("Operador", "/", 0, 0))
            else:
                raise ErroSemanticoException(f"Operador inválido")
            self.unary()

    def unary(self):
        if self.checarToken("Operador", "!") or self.checarToken("Operador", "-"):
            if self.checarToken("Operador", "!"):
                self.consumir(Token("Operador", "!", 0, 0))
            elif self.checarToken("Operador", "-"):
                self.consumir(Token("Operador", "-", 0, 0))
            else:
                raise ErroSemanticoException(f"Operador inválido")
            self.unary()
        else:
            self.primary()

    def primary(self):
        if self.checarToken("Literal", self.tokens[self.indice].valor):
            self.consumir(
                Token("Literal", self.tokens[self.indice].valor, 0, 0))
        elif self.checarToken("Palavra reservada", "true") or self.checarToken("Palavra reservada", "false"):
            self.consumir(Token("Palavra reservada",
                          self.tokens[self.indice].valor, 0, 0))
        elif self.checarToken("Identificador", self.tokens[self.indice].valor):
            name = self.tokens[self.indice].valor
            var_type = self.symbol_table.lookup(name)
            if var_type is None:
                raise ErroSemanticoException(
                    f"Variável '{name}' não declarada")
            self.consumir(Token("Identificador", name, 0, 0))
        elif self.checarToken("Delimitador", "("):
            self.consumir(Token("Delimitador", "(", 0, 0))
            self.expression()
            self.consumir(Token("Delimitador", ")", 0, 0))
        else:
            raise ErroSemanticoException(
                f"Token inválido: {self.tokens[self.indice]}")

    def tokenAnterior(self):
        self.indice -= 1

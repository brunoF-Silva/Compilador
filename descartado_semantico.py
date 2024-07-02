class AnalisadorSemantico(AnalisadorSintatico):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.escopos = [{}]  # Pilha de escopos
    
    def declarar_variavel(self, nome):
        if nome in self.escopos[-1]:
            raise ErroSemanticoException(f"Variável '{nome}' já declarada no escopo atual.")
        self.escopos[-1][nome] = None  # Declara a variável no escopo atual
    
    def definir_variavel(self, nome, valor):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                escopo[nome] = valor
                return
        raise ErroSemanticoException(f"Variável '{nome}' não declarada.")
    
    def buscar_variavel(self, nome):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        raise ErroSemanticoException(f"Variável '{nome}' não declarada.")
    
    def varDecl(self):
        self.consumir(Token("Palavra reservada", "var"))
        nome_var = self.tokens[self.indice].valor
        self.consumir(Token("Identificador", nome_var))
        self.declarar_variavel(nome_var)
        if self.checarToken(Token("Operador", "=")):
            self.consumir(Token("Operador", "="))
            valor = self.expression()
            self.definir_variavel(nome_var, valor)
        self.consumir(Token("Delimitador", ";"))
    
    def assignment(self):
        if self.checarToken(Token("Identificador", self.tokens[self.indice].valor)):
            nome_var = self.tokens[self.indice].valor
            self.consumir(Token("Identificador", nome_var))
            if self.checarToken(Token("Operador", "=")):
                self.consumir(Token("Operador", "="))
                valor = self.assignment()
                self.definir_variavel(nome_var, valor)
            else:
                self.tokenAnterior()
                self.logic_or()
        else:
            self.logic_or()

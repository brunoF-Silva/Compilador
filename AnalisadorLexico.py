# import re


# class Token:
#     def __init__(self, tipo, valor, linha, coluna):
#         self.tipo = tipo
#         self.valor = valor
#         self.linha = linha
#         self.coluna = coluna

#     def __str__(self):
#         return f"{self.tipo}('{self.valor}') na linha {self.linha}, coluna {self.coluna}"


# class AnalisadorLexico:
#     def __init__(self, arquivo):
#         self.arquivo = arquivo
#         self.tokens = []

#     def analisar_e_mostrar_resultado(self):
#         try:
#             with open(self.arquivo, 'r') as arquivo:
#                 codigo = arquivo.read()
#                 self.analisar(codigo)
#                 for token in self.tokens:
#                     print(token)
#         except FileNotFoundError:
#             print(f"Arquivo {self.arquivo} não encontrado.")

#     def analisar(self, codigo):
#         padroes = {
#             'Palavra reservada': r'\b(class|fun|if|else|while|for|return|var|print|true|false|nil|and|or|this|super)\b',
#             'Operador': r'(\+|-|\*|\/|!=|==|<=|>=|<|>|=|!)',
#             'Delimitador': r'(\(|\)|\{|\}|\[|\]|,|;|\.|:)',
#             'Identificador': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
#             'Constante Textual': r'"[^"\n]*"',
#             'Ponto Flutuante': r'\b\d+\.\d+\b',
#             'Inteiro': r'\b\d+\b'
#         }

#         linha, coluna = 1, 1
#         i = 0
#         while i < len(codigo):
#             match = None
#             for tipo, padrao in padroes.items():
#                 regex = re.compile(padrao)
#                 match = regex.match(codigo, i)
#                 if match:
#                     valor = match.group(0)
#                     self.tokens.append(Token(tipo, valor, linha, coluna))
#                     i += len(valor)
#                     coluna += len(valor)
#                     break
#             if not match:
#                 if codigo[i] in [' ', '\t']:
#                     coluna += 1
#                 elif codigo[i] == '\n':
#                     linha += 1
#                     coluna = 1
#                 else:
#                     raise SyntaxError(
#                         f"Caractere inválido '{codigo[i]}' na linha {linha}, coluna {coluna}")
#                 i += 1

#     def obter_tokens(self):
#         return self.tokens

import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"Token({self.tipo}, {self.valor})"

class AnalisadorLexico:
    palavra_reservada = ["fun","int", "char", "long", "short", "float", "double", "void",
                         "if", "else", "for", "do", "break", "continue",  "struct", "switch",
                         "case", "default", "return", "var",  "while", "print", "true", "false",
                         "nil", "this", "or", "and"]

    operadores = r"\|\||&&|==|!=|<|>|<=|>=|\+|-|\*|/|%|--|\+\+|->|!|\.|="

    delimitadores = r"\(|\)|\[|\]|\{|\}|;|,"

    identificadores = r'[a-zA-Z_][a-zA-Z0-9_]*\b'

    inteiros = r'[+-]?\d+\b'

    ponto_flutuante = r'[+-]?\d+\.\d+'

    constante_textual = r'["\'][^"\']*["\']'

    def __init__(self, arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                conteudo = re.sub('//.*', ' ', conteudo)
                conteudo = re.sub('(/\*(.|\n)*?\*/)', ' ', conteudo)
                self.tokens = self.tokenizar(conteudo)
                self.indice = 0
                self.token_atual = None

        except FileNotFoundError:
            print(f"Arquivo '{arquivo}' não encontrado.")

    def tokenizar(self, conteudo):
        regex = re.compile(
            r'[+-]?\d+\.\d+|\+|\b\d+\b|[a-zA-Z_]+[a-zA-Z0-9_]*\b|["\'][^"\']*["\']|->|&&|\|\||\-\-|\+\+|[-+*/%&=!><\|]=?|[-+*/%&=!><\|]|\||\(|\)|\[|\]|\{|\}|\.|,|;')

        # regex = re.compile(
        #      r'\+|\d+[a-zA-Z_]*\b|[a-zA-Z_]+[a-zA-Z0-9_]*\b|["\'][^"\']*["\']|[+-]?\d+\.\d+|->|&&|\|\||\-\-|\+\+|[-+*/%&=!><\|]=?|[-+*/%&=!><\|]|\||\(|\)|\[|\]|\{|\}|\.|,|;')
        valores_tokens = regex.findall(conteudo)
        tokens = [self.obter_tipo_token(valor) for valor in valores_tokens]
        tokens.append(Token("Delimitador", "EOF"))
        return tokens

    def obter_tipo_token(self, valor):
        if valor in self.palavra_reservada:
            return Token("Palavra reservada", valor)
        elif re.match(self.operadores, valor):
            return Token("Operador", valor)
        # elif re.match(self.inteiros, valor):
        #     return Token("Numero", valor)  # Inteiro
        elif re.match(self.ponto_flutuante, valor):
            return Token("Ponto Flutuante", valor)  # Ponto Flutuante
        elif re.match(self.inteiros, valor):
            return Token("Inteiro", valor)  # Ponto Flutuante
        elif valor in self.delimitadores:
            return Token("Delimitador", valor)
        elif re.match(self.identificadores, valor):
            return Token("Identificador", valor)
        elif re.match(self.constante_textual, valor):
            return Token("Constante Textual", valor)
        else:
            return Token("Desconhecido", valor)
        
    def proximo_token(self):
        if self.indice < len(self.tokens):
            self.token_atual = self.tokens[self.indice]
            self.indice += 1
        else:
            self.token_atual = Token("Delimitador", "EOF")
        return self.token_atual

    def analisar(self):
        resultado = []
        while True:
            try:
                token = self.proximo_token()
                resultado.append((token.tipo, token.valor))
                if token.valor == "EOF":
                    break
                if re.match(r'\d+[a-zA-Z_]+\b|[a-zA-Z_]+[™]\b', token.valor):
                    raise Exception(f"Token inválido: {token.valor}")
            except Exception as e:
                resultado.append(("Erro Léxico", f"Erro: token inválido ({str(e)})"))
                break

        return resultado

    def mostrar_resultado(self, resultado):
        for tipo, valor in resultado:
            print(f"Tipo: {tipo}\tValor: {valor}")

    def obter_tokens(self):
        return self.tokens

    def analisar_e_mostrar_resultado(self):
        resultado = self.analisar()
        self.mostrar_resultado(resultado)
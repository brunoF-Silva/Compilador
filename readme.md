## Curso: Ciência da Computação
## Campus Universitário de Palmas
#### Disciplina: Compiladores
#### Professora Dra.: Anna Paula de Souza Parentes Rodrigues
#### Alunos: Bruno Ferreira da Silva e Izabela Caldeira Sena Ferreira

**Semestre:** 2024.1

## Compiladores - Trabalho Final

### Descrição:
Este projeto apresenta um compilador que integra um analisador léxico, um analisador sintático e um analisador semântico. O compilador é projetado para reconhecer códigos escritos na linguagem C- e traduzi-los para Python, proporcionando uma ferramenta útil para a conversão e análise de código entre essas duas linguagens.

O analisador léxico é responsável por ler o código-fonte e dividir o texto em tokens. Esses tokens são as menores unidades de significado do código, como palavras-chave, identificadores, operadores e símbolos. A análise léxica facilita a identificação e classificação desses elementos, preparando o terreno para a próxima etapa do processo de compilação.

O analisador sintático recebe os tokens do analisador léxico e organiza esses tokens em uma estrutura de árvore que representa a estrutura gramatical do código-fonte. Esta fase verifica se a sequência de tokens respeita as regras sintáticas da linguagem C-. O analisador sintático embutido com o semântico garante uma transição fluida para a verificação semântica.

O analisador semântico, por sua vez, foca na verificação de tipo em declarações e atribuições, além de garantir que todas as variáveis e métodos sejam declarados corretamente antes de serem utilizados. Este componente é crucial para garantir que o código não só esteja sintaticamente correto, mas também faça sentido em termos de lógica de programação e regras de tipagem.

Em conjunto, esses analisadores trabalham para transformar o código escrito em C- em um código equivalente em Python, facilitando a migração e análise de programas entre essas duas linguagens. Este projeto não apenas exemplifica a criação de um compilador, mas também destaca a importância de uma análise semântica no processo de compilação.

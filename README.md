# Universidade Federal de Santa Catarina

# Departamento de Informática e Estatística - INE/CTC
14 de Fevereiro de 2022

Trabalho de Implementação - INE 5421

Integrantes do grupo:
- Artur Ribeiro Alfa (17103919)
- Leonardo Vieira Nunes (19102923)
- Matheus Felipe Bertonceli Bueno (19100539)


# Instruções de instalação
Para este projeto foi utilizada a versão 3.8 da linguagem de programação Python, e as seguintes bibliotecas

_json_\
_pathlib_\
Ambas fazem parte da biblioteca padrão do Python, não necessitando instalações extras


# Execução
Para executar o programa, execute o arquivo _main.py_ usando o interpretador python\
executando o seguinte comando dentro do diretório raiz do projeto:\
`python3 main.py`

Uma vez rodando o programa, você pode selecionar uma das operações disponíveis digitando o número correspondente e pressionando _ENTER_

1. Conversão de um AFND para AFD
2. Reconhecimento de sentenças em AF
3. Minimização de automato finito
4. União de dois automatos
5. Intersecção de dois automatos
6. Conversão de ER para AFD

Uma vez selecionada a operação, será pedido que especifique um arquivo json (sem a extensão _.json_) para servir de base para o autômato. Certifique-se do arquivo estar na pasta _test_.

Para a conversão de Expressão Regular para AFD, apenas digite a ER no terminal.

Após o término da operação selecionada, caso queira salvar o resultado em um arquivo, especifique o nome do arquivo novo da mesma forma.

## MyOperatingJSON
Esta classe consiste no objeto que estrutura a quíntupla de um automato finito, sejam elas:
- states: conjunto de todos os estados do automato;
- initial_state: estado inicial do automato;
- final_state: conjunto de estados finais do automato;
- transitions: lista contendo as transições do automato, onde cada transição possui os parâmetros state_from, state_to e transition_symbol.
- symbols: conjunto de símbolos do automato.
## Conversão de um AFND para AFD
A determinização deve receber um autômato finito não deterministico e deve retonar um autômato equivalente sem epsilon transições. Para implementar a determinização, além de encapsular o automato de entrada como um objeto da classe MyOperatingJSON, foi utilizado um atributo do tipo dicionário chamado epsilon_transitions, onde a chave corresponde a origem de um estado com epsilon transição e valor para o conjunto de todos os estados alcançáveis por aquele estado via epsilon transição.

## Reconhecimento de sentenças em AF
A operação de reconhecimento deve receber uma sentença, um autômato e, retornar se aquela sentença é válida para aquele automato. Não foram utilizadas outras estruturas além da própria estrutura do automato para esta operação.

## Minimização de automato finito
O processo de minimização deve receber um autômato finito (deterministico ou não) que irá retornar um novo autômato equivalente ao anterior com um número mínimo de estados.

Para este trabalho, foi aplicado o teorema de Myhill Nerode para realizar a minimização do autômato. Para conseguirmos minimizar o autômato finito não deterministico, este é determinimizado antes de ser minimizado.

Link para o teorema utilizado: https://www.cs.columbia.edu/~tal/3261/sp18/MyhillNerode.pdf

Foram utilizadas as seguintes estruturas de dados para implementar a minimização:

- tabelaEstados: Dicionário Python para verificar se determinado par de estados já foi marcado;
- inicial: Estado inicial do automato original;
- estados: Lista de estados do automato original;
- simbolos: Lista de simbolos do automato original;
- finais: Lista de estados finais do automato original;
- repetirMarcacao: Booleano para indicar se deve haver repetição do processo de marcar os pares de estados na tabelaEstados. Inicialmente setado como False e, caso houver alguma modificação na tabela, é setado para True;
- EstadosOtimizados: Lista com todos os estados, combinados ou não, que serão inseridos no novo automato;
- EstadosCombinados: Lista que armazena os conjuntos de estados que podem ser minimizados para um único estado;
- automato: automato original (já determinizado);
- new_automata: automato original minimizado.

## União de dois automatos
A união deve receber dois automatos finitos e retornar a união dos mesmos. Não foram utilizadas outras estruturas além da própria estrutura do automato para esta operação.
## Intersecção de dois automatos
A intersecção deve receber dois automatos finitos e retornar a intersecção dos mesmos. Não foram utilizadas outras estruturas além da própria estrutura do automato para esta operação.
from Vertex import Vertex
import random

def guess(choices: list):
    """
    Abstrai a escolha não-determinística de uma solução
    dentre as soluções possíveis.

    Parâmetros
    ----------
        - choices (list): Lista de soluções possíveis.
    
    Retorno
    -------
        - choice (bool | None): Escolha aleatória selecionada.
    """

    return random.choice(choices)

def non_deterministic_3_coloring(G: dict, C: list) -> bool:
    """
    Algoritmo não-determinístico para o problema da 3-coloração
    em sua versão de decisão (Um dos requisitos para ser da classe NP).

    Parâmetros
    ----------
        - G (dict): Grafo composto pela lista de vértices
        e lista de arestas.
        - C (list): Lista de cores possíveis de tamanho K = 3.
    
    Retorno
    -------
        - result (bool): Resultado indicando se é possível ou não
        colorir o grafo G com as 3 cores de C, de forma que não
        haja vértices adjacentes com a mesma cor.
    """

    V = G["V"]
    E = G["E"]

    # Etapa de escolha
    for v in V:
        v.set_color(guess(C))

    # Etapa de verificação
    for e in E:
        if V[e[0]].get_color() == V[e[1]].get_color():
            return False
    return True

def run_petersen():
    """
    Executa o algoritmo não determinístico para o grafo de Petersen.
    """

    # Grafo de Petersen
    G = {
        "V": [Vertex(i) for i in range(0,10)],
        "E": [
            (0,1), (0,2), (0,3),
            (1,4), (1,8), (2,6),
            (2,7), (3,5), (3,9),
            (4,5), (4,7), (5,6),
            (6,8), (7,9), (8,9)
        ]
    }

    # Enquanto o algoritmo não-determinístico não encontrar
    # uma solução válida, ele é invocado novamente.
    result = False
    while not result:
        result = non_deterministic_3_coloring(G, ["red", "green", "blue"])
        if result: # Se encontrar uma solução válida
            # Exibe as cores de cada vértice
            for v in G["V"]:
                print(v)


if __name__ == "__main__":
    run_petersen()

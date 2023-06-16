from Vertex import Vertex

def f1(Ip: str) -> tuple:
    """
    Função que mapeia a entrada do problema 3-SAT
    para uma entrada do problema da 3-coloração.

    Parâmetros
    ----------
        - Ip (str): Expressão booleana na Forma Normal Conjutiva.
        Deve ser da forma: (x OR y) AND (w OR z OR ~x).
    
    Retorno
    -------
        - G (dict): Grafo contendo a lista de vértices e lista de arestas.
        - C (list): Lista de cores possíveis de tamanho K = 3.
    """

    # Inicializa o grafo com os 3 vértices iniciais
    # formando um triângulo (T - F - B - T)
    graph = {
        "V": [
            Vertex("T"),
            Vertex("F"),
            Vertex("B")
        ],
        "E": [(0,1), (1,2), (0,2)]
    }
    # Contador de índice dos vértices
    index_vertex = 3

    # Extrai das cláusulas os literais sem a negação
    clausules = Ip.split(" AND ")
    literals = []
    for i in range(len(clausules)):
        clausules[i] = clausules[i].replace("(", "").replace(")", "")
        temp_literals = clausules[i].split(" OR ")
        for literal in temp_literals:
            temp_literal = literal.replace("~", "")
            if temp_literal not in literals:
                literals.append(temp_literal)

    # Cria os vértices xi e ~xi de cada literal xi
    # e conecta-os com o vértice base (B) formando triângulos
    # (xi - ~xi - B - xi)
    for literal in literals:
        new_vertex = Vertex(literal)
        new_vertex_neg = Vertex("~" + literal)
        graph["V"].append(new_vertex)
        graph["V"].append(new_vertex_neg)

        graph["E"].append((index_vertex, index_vertex + 1))
        graph["E"].append((index_vertex, 2))
        graph["E"].append((index_vertex + 1, 2))

        index_vertex += 2

    # Cria as portas OR de cada cláusula
    for clausule in clausules:
        literals = clausule.split(" OR ")
        if len(literals) == 1:
            # Cláusula com 1 literal (x): O vértice do literal é automaticamente conectado
            # com o vértice False (F), para ser verdadeiro
            index_literal1 = -1
            for i in range(len(graph["V"])):
                if graph["V"][i].get_name() == literals[0]:
                    index_literal1 = i
                    break
            
            graph["E"].append((index_literal1, 1))
        elif len(literals) == 2:
            # Cláusula com 2 literais (x V y): Cria uma porta OR de vértices formando um triângulo
            # (input1 - input2 - output - input1) de maneira que o vértice x é conectado a uma
            # entrada, o vértice y à outra e a saída é conectada aos vértices (B) e (F),
            # obrigando a saída da cláusula ser verdadeira
            index_literal1 = -1
            index_literal2 = -1
            for i in range(len(graph["V"])):
                if graph["V"][i].get_name() == literals[0]:
                    index_literal1 = i
                    break
            for i in range(len(graph["V"])):
                if graph["V"][i].get_name() == literals[1]:
                    index_literal2 = i
                    break
            
            graph["V"].append(Vertex("inp1"))
            graph["V"].append(Vertex("inp2"))
            graph["V"].append(Vertex("out"))

            graph["E"].append((index_vertex, index_vertex + 1))
            graph["E"].append((index_vertex, index_vertex + 2))
            graph["E"].append((index_vertex + 1, index_vertex + 2))
            
            graph["E"].append((index_literal1, index_vertex))
            graph["E"].append((index_literal2, index_vertex + 1))
            
            graph["E"].append((index_vertex + 2, 1))
            graph["E"].append((index_vertex + 2, 2))

            index_vertex += 3
        elif len(literals) == 3:
            # Cláusula com 3 literais ((x V y) V z): Cria duas portas OR, uma conectando dois literais e
            # outra conectando a saída da primeira porta em uma entrada e o último literal em outra
            # e conectando a última saída nos vértices (B) e (F) para a cláusula ser verdadeira
            index_literal1 = -1
            index_literal2 = -1
            index_literal3 = -1
            for i in range(len(graph["V"])):
                if graph["V"][i].get_name() == literals[0]:
                    index_literal1 = i
                    break
            for i in range(len(graph["V"])):
                if graph["V"][i].get_name() == literals[1]:
                    index_literal2 = i
                    break
            for i in range(len(graph["V"])):
                if graph["V"][i].get_name() == literals[2]:
                    index_literal3 = i
                    break
            
            graph["V"].append(Vertex("inp1"))
            graph["V"].append(Vertex("inp2"))
            graph["V"].append(Vertex("out"))

            graph["V"].append(Vertex("inp1"))
            graph["V"].append(Vertex("inp2"))
            graph["V"].append(Vertex("out"))

            graph["E"].append((index_vertex, index_vertex + 1))
            graph["E"].append((index_vertex, index_vertex + 2))
            graph["E"].append((index_vertex + 1, index_vertex + 2))
            
            graph["E"].append((index_literal1, index_vertex))
            graph["E"].append((index_literal2, index_vertex + 1))

            graph["E"].append((index_vertex + 2, index_vertex + 3))
            graph["E"].append((index_literal3, index_vertex + 4))
            
            graph["E"].append((index_vertex + 3, index_vertex + 4))
            graph["E"].append((index_vertex + 3, index_vertex + 5))
            graph["E"].append((index_vertex + 4, index_vertex + 5))
            
            graph["E"].append((index_vertex + 5, 1))
            graph["E"].append((index_vertex + 5, 2))

            index_vertex += 6
    
    # Retorna uma instância do problema 3-coloração
    # Um grafo G e um conjunto de 3 cores (True, False, None)
    return graph, [True, False, None]

def is_safe(G: dict, v: int, color) -> bool:
    """
    Verifica se um vértice pode receber uma cor verificando
    as cores dos vértices vizinhos.

    Parâmetro
    ---------
        - G (dict): Grafo contendo a lista de vértices
        e lista de arestas;
        - v (int): Índice do vértice a ser analisado.
        - color (Any): Possível cor para o vértice v.
    
    Retorno
    -------
        - result (bool): Resultado indicando se a cor
        pode ser atribuída para o vértice ou não.
    """

    for edge in G["E"]:
        if v == edge[0]:
            if G["V"][edge[1]].get_color() == color:
                return False
        elif v == edge[1]:
            if G["V"][edge[0]].get_color() == color:
                return False
    
    return True

def backtracking_3colorable(G: dict, C: list, idx_vertex: int, init: int):
    """
    Algoritmo que soluciona o problema da 3-coloração
    utilizando o paradigma backtracking. Partindo do vértice
    que abstrai a solução da expressão booleana do 3-SAT, passa
    por cada vértice atribuindo sua cor, verificando sempre se a cor
    selecionada é válida com base nos vértices vizinhos.

    Parâmetros
    ----------
        - G (dict): Grafo contendo a lista de vértices
        e a lista de arestas;
        - C (list): Lista de tamanho K = 3 contendo as cores possíves;
        - idx_vertex (int): Índice do vértice atual;
        - init (int): Posição do vértice colorido inicialmente.
    """

    # Condição de parada: Atingir o último
    # vértice colorido do caso-base
    if idx_vertex == init:
        for v in G["V"]:
            print(v)
    else:
        for color in C:
            if is_safe(G, idx_vertex, color):
                G["V"][idx_vertex].set_color(color)
                backtracking_3colorable(G, C, idx_vertex - 1, init)

def Aq(Iq: tuple) -> dict:
    """
    Função que executa o algoritmo que resolve o problema da 3-coloração.

    Parâmetro
    ---------
        - Iq (tuple): Resultado da entrada mapeada do problema 3-SAT.
    
    Retorno
    -------
        - G (dict): Grafo resolvido (colorido).
    """

    G = Iq[0]
    C = Iq[1]

    # Caso-base: O triângulo inicial (T - B - F - T) colorido
    G["V"][0].set_color(True)
    G["V"][1].set_color(False)
    G["V"][2].set_color(None)
    
    backtracking_3colorable(G, C, len(G["V"]) - 1, 2)
    return G

def f2(Sq: dict) -> bool:
    """
    Função que mapeia a saída do problema da 3-coloração
    para a saída do problema 3-SAT.

    Parâmetro
    ---------
        - Sq (dict): Grafo contendo a lista de vértices e
        lista de arestas;
    
    Retorno
    -------
        - result (bool): Resultado True ou False indicando
        a resolução da satisfabilidade da expressão lógica.
    """
    
    not_literals = ["T", "F", "B", "inp1", "inp2", "out"]
    Sp = []

    print("\nValores de literais para o 3-SAT:")
    for v in Sq["V"]:
        if v.get_name() not in not_literals:
            print("{} = {}".format(v.get_name(), v.get_color()))
            if v.get_color():
                Sp.append(v.get_name())

    return Sp

if __name__ == "__main__":
    # Ip = "(x) AND (x OR y OR z) AND (z)"
    Ip = "(u OR ~v OR w) AND (v OR x OR ~y)"
    # Ip = "(u OR v OR w)"

    # Mapeamento da entrada do problema 3-SAT
    # para uma entrada do problema da 3-coloração
    Iq = f1(Ip)
    # Resolução do problema da 3-coloração
    # para a entrada mapeada Iq
    Sq = Aq(Iq)
    # Tradução da saída da resolução do problema
    # da 3-coloração para uma saída do problema 3-SAT
    Sp = f2(Sq)
class Vertex:
    """
    Classe que abstrai a representação de um vértice que
    possui um nome associado e uma cor.

    Parâmetros
    ----------
        - name (str | int): Nome do vértice;
        - color (Any): Cor do vértice (default = "").
    """

    def __init__(self, name, color=""):
        # Inicializa o vértice com seu nome e sua cor
        # ou inicializa-o sem uma cor associada
        self.__name = name
        self.__color = color

    def __str__(self) -> str:
        # Utilizado para exibição das informações do vértice
        return f"Vértice {self.__name} de cor {self.__color}"

    def set_color(self, new_color):
        """
        Atualiza a cor do vértice.

        Parâmetros
        ----------
            - new_color (Any): Nova cor do vértice.
        """

        self.__color = new_color
    
    def get_color(self):
        """
        Retorna a cor atual do vértice.

        Retorno
        -------
            - color (Any): Cor atual do vértice.
        """

        return self.__color
    
    def set_name(self, new_name):
        """
        Atualiza o nome do vértice.

        Parâmetros
        ----------
            - new_name (Any): Novo nome do vértice.
        """

        self.__name = new_name
    
    def get_name(self):
        """
        Retorna o nome atual do vértice.

        Retorno
        -------
            - name (str | int): Nome atual do vértice.
        """
        
        return self.__name
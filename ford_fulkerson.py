# Daniel Luiz Araújo Marques - Algoritmo Ford-Fulkerson em Python

# Criação e plotagem de grafos
import networkx as nx 
import matplotlib.pyplot as plt

# Implementação do algoritmo Ford-Fulkerson para encontrar o fluxo máximo em um grafo
def ford_fulkerson(grafo, raiz, destino):
    
    # Função para atualizar o fluxo ao longo de um caminho
    def update_fluxo(v, fluxo):
        u = adjacente[v]
        if v != raiz:
            
            # Encontra a aresta com a menor capacidade no caminho
            if grafo[u][v] < fluxo:
                fluxo = grafo[u][v]
            
            # Recursivamente atualiza o fluxo ao longo do caminho
            if u != raiz:
                fluxo = update_fluxo(u, fluxo)
            
            # Atualiza as capacidades das arestas no caminho
            grafo[u][v] -= fluxo
            grafo[v][u] += fluxo
        
        return fluxo

    # Função para encontrar um caminho da raiz ao destino com capacidade residual
    def bfs():
        
        # Inicializa todos os nós como não visitados
        for i in range(len(grafo)):
            adjacente[i] = -1
        
        # Começa na raiz
        fila = [raiz]
        adjacente[raiz] = raiz
        
        # Busca em largura para encontrar um caminho
        while fila:
            u = fila.pop(0)
            
            # Visita todos os vizinhos de u
            for v in range(len(grafo)):
                
                # Se o nó v não foi visitado e a aresta u-v tem capacidade residual
                if adjacente[v] == -1 and grafo[u][v] > 0:
                    # Marca v como visitado e adiciona à fila
                    adjacente[v] = u
                    fila.append(v)
                    
                    # Se v é o destino, encontramos um caminho
                    if v == destino:
                        return True
    
        return False

    # Inicializa o fluxo máximo como 0
    max_fluxo = 0
    adjacente = [-1] * len(grafo)
    
    # Enquanto houver um caminho da raiz ao destino
    while bfs():
        # Aumenta o fluxo máximo pelo fluxo encontrado
        max_fluxo += update_fluxo(destino, float('inf'))
    # Retorna o fluxo máximo
    return max_fluxo

# Lê as arestas do grafo de um arquivo
aresta = []

with open('input.txt', 'r') as file:
    lines = file.readlines()
    
    for line in lines:
        u, v, c = line.strip().split()
        aresta.append((u, v, int(c)))

# Cria um conjunto de todos os vértices no grafo
vertices = set([u for u, v, c in aresta] + [v for u, v, c in aresta])

# Mapeia cada vértice para um inteiro único
vertice_to_int = {node: i for i, node in enumerate(vertices)}

# Mapeia cada inteiro de volta para o vértice correspondente
int_to_vertice = {i: node for node, i in vertice_to_int.items()}

# Inicializa o grafo como uma matriz de adjacência
grafo = [[0 for _ in vertices] for _ in vertices]

# Preenche a matriz de adjacência com as capacidades das arestas
for u, v, c in aresta:
    grafo[vertice_to_int[u]][vertice_to_int[v]] = c

# Define a raiz e o destino do grafo
raiz = vertice_to_int['S']
destino = vertice_to_int['T']

# Faz uma cópia do grafo original para calcular os fluxos depois
original_grafo = [linha[:] for linha in grafo]

# Calcula o fluxo máximo usando o algoritmo Ford-Fulkerson
max_fluxo = ford_fulkerson(grafo, raiz, destino)

# Imprime o fluxo máximo
print(f'O fluxo máximo do grafo é {max_fluxo}')

# Imprime o fluxo em cada aresta
print('O fluxo em cada aresta é:')
for u, v, c in aresta:
    fluxo = original_grafo[vertice_to_int[u]][vertice_to_int[v]] - grafo[vertice_to_int[u]][vertice_to_int[v]]
    print(f'{u} -> {v}: {fluxo}')

# Cria um grafo direcionado usando 
G = nx.DiGraph()

# Adiciona as arestas ao grafo 
for u, v, c in aresta:
    G.add_edge(u, v, capacity = c, fluxo = original_grafo[vertice_to_int[u]][vertice_to_int[v]] - grafo[vertice_to_int[u]][vertice_to_int[v]])

# Desenha o grafo 
pos = nx.spring_layout(G)  
nx.draw(G, pos, with_labels = True, node_color = 'skyblue', node_size = 1500, edge_cmap = plt.cm.Blues, width = 2)
edge_labels = nx.get_edge_attributes(G, 'fluxo')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)

# Mostra o grafo
plt.show()

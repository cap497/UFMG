import sys
from queue import PriorityQueue

# --------------------------------
# FUNCOES AUXILIARES
# --------------------------------

# Função para obter vizinhos do estado atual
def get_neighbors(node):
    neighbors = []
    state = list(node)
    empty_tile_index = state.index(0)
    row, col = empty_tile_index // 3, empty_tile_index % 3
    
    # Movimento para cima
    if row > 0:
        new_state = state[:]
        new_state[empty_tile_index], new_state[empty_tile_index - 3] = new_state[empty_tile_index - 3], new_state[empty_tile_index]
        neighbors.append(tuple(new_state))
    
    # Movimento para baixo
    if row < 2:
        new_state = state[:]
        new_state[empty_tile_index], new_state[empty_tile_index + 3] = new_state[empty_tile_index + 3], new_state[empty_tile_index]
        neighbors.append(tuple(new_state))
    
    # Movimento para a esquerda
    if col > 0:
        new_state = state[:]
        new_state[empty_tile_index], new_state[empty_tile_index - 1] = new_state[empty_tile_index - 1], new_state[empty_tile_index]
        neighbors.append(tuple(new_state))
    
    # Movimento para a direita
    if col < 2:
        new_state = state[:]
        new_state[empty_tile_index], new_state[empty_tile_index + 1] = new_state[empty_tile_index + 1], new_state[empty_tile_index]
        neighbors.append(tuple(new_state))
    
    return neighbors

# Funcao para imprimir o tabuleiro
def print_board(state):
    for i in range(3):
        for j in range(3):
            s = state[3*i + j]
            if s != 0:
                print(s, end=' ')
            else:
                print(" ", end=' ')
        print()
    print()

# Funcao para imprimir os passos
def print_step(print_steps, result):
    print(len(result) - 1)
    if print_steps and result:
        print()
        for state in result:
            print_board(state)

# --------------------------------
# BUSCA SEM INFORMACAO
# --------------------------------

# Algoritmo Breadth-first search (BFS)
def bfs(start, goal):
    queue = [(start, [])]
    explored = set()
    while queue:
        node, path = queue.pop(0)
        if node == goal:
            return path + [node]  # Retorna o caminho completo da solução
        explored.add(node)
        neighbors = get_neighbors(node)
        for neighbor in neighbors:
            if neighbor not in explored:
                queue.append((neighbor, path + [node]))  # Adiciona o nó atual ao caminho
    return []

# Algoritmo Iterative deepening search (IDS)
def ids(start, goal, max_depth=30):
    depth = 0
    while depth <= max_depth:
        result = dls(start, goal, depth)
        if result:
            return result
        depth += 1
    return None

def dls(node, goal, depth):
    if node == goal:
        return [node]
    if depth <= 0:
        return None
    neighbors = get_neighbors(node)
    for neighbor in neighbors:
        result = dls(neighbor, goal, depth - 1)
        if result:
            return [node] + result
    return None

# Algoritmo Uniform-cost search (UCS)
def ucs(start, goal):
    priority_queue = PriorityQueue()
    priority_queue.put((0, start, []))
    explored = set()
    while not priority_queue.empty():
        cost, node, path = priority_queue.get()
        if node == goal:
            return path + [node]  # Retorna o vetor de estados
        explored.add(node)
        neighbors = get_neighbors(node)
        for neighbor in neighbors:
            if neighbor not in explored:
                priority_queue.put((cost + 1, neighbor, path + [node]))  # Adiciona o nó atual ao caminho
    return []

# --------------------------------
# BUSCA COM INFORMACAO
# --------------------------------

# Heuristica Fora do Lugar
def heuristic_out_of_place(node, goal):
    misplaced_tiles = 0
    for i, j in zip(node, goal):
        if i != j and i != 0:
            misplaced_tiles += 1
    return misplaced_tiles

# Algoritmo A* Search
def astar(start, goal):
    priority_queue = PriorityQueue()
    priority_queue.put((0, start, []))
    explored = set()
    while not priority_queue.empty():
        f, node, path = priority_queue.get()
        if node == goal:
            return path + [node]
        explored.add(node)
        neighbors = get_neighbors(node)
        for neighbor in neighbors:
            if neighbor not in explored:
                new_path = path + [node]
                priority_queue.put((len(new_path) + heuristic_out_of_place(neighbor, goal), neighbor, new_path))
    return []

# Heuristica Distancia de Manhattan
def heuristic_manhattan_distance(node, goal):
    total_distance = 0
    for i in range(3):
        for j in range(3):
            current_tile = node[i * 3 + j]
            if current_tile != 0:
                correct_position = goal.index(current_tile)
                goal_row, goal_col = correct_position // 3, correct_position % 3
                total_distance += abs(i - goal_row) + abs(j - goal_col)
    return total_distance

# Algoritmo Greedy Best-first Search
def greedy_best_first(start, goal):
    priority_queue = PriorityQueue()
    priority_queue.put((heuristic_manhattan_distance(start, goal), start, []))
    explored = set()
    while not priority_queue.empty():
        item = priority_queue.get()
        h, node, path = item[0], item[1], item[2]
        if node == goal:
            return path + [node]
        explored.add(node)
        neighbors = get_neighbors(node)
        if not neighbors:
            return None
        for neighbor in neighbors:
            if neighbor not in explored:
                priority_queue.put((heuristic_manhattan_distance(neighbor, goal), neighbor, path + [node]))
    return None

# --------------------------------
# BUSCA LOCAL
# --------------------------------

# Algoritmo Hill Climbing
def hill_climbing(start, goal, k):
    current_state = start
    current_cost = calculate_cost(start, goal)
    steps = 0
    visited_states = [current_state]

    while steps < k and current_state != goal:
        neighbors = get_neighbors(current_state)
        neighbors.sort(key=lambda x: calculate_cost(x, goal))

        if neighbors and calculate_cost(neighbors[0], goal) < current_cost:
            current_state = neighbors[0]
            current_cost = calculate_cost(current_state, goal)
            visited_states.append(current_state)
        else:
            break

        steps += 1

    return visited_states

# Calcula o custo do estado
def calculate_cost(state, goal):
    misplaced_tiles = 0
    for i in range(9):
        if state[i] != goal[i] and state[i] != 0:
            misplaced_tiles += 1
    return misplaced_tiles

# --------------------------------
# FUNÇÃO MAIN
# --------------------------------

if __name__ == "__main__":
    # Leitura da linha de comando
    algorithm = sys.argv[1]
    puzzle_input = list(map(int, sys.argv[2:11]))
    print_steps = False
    if len(sys.argv) > 11 and sys.argv[11] == "PRINT":
        print_steps = True

    # Estados inicial e final
    start_state = tuple(puzzle_input)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    # Execucao dos algoritmos
    if algorithm == "B":
        result = bfs(start_state, goal_state)
        print_step(print_steps, result)
    elif algorithm == "I":
        result = ids(start_state, goal_state)
        print_step(print_steps, result)
    elif algorithm == "U":
        result = ucs(start_state, goal_state)
        print_step(print_steps, result)
    elif algorithm == "A":
        result = astar(start_state, goal_state)
        print_step(print_steps, result)
    elif algorithm == "G":
        result = greedy_best_first(start_state, goal_state)
        print_step(print_steps, result)
    elif algorithm == "H":
        k = 100
        result = hill_climbing(start_state, goal_state, k)
        print_step(print_steps, result)

    
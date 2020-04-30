perfectSquares = {x*x: x for x in range(2, 50)}

def createGraph(vertices):
    graph = {}
    for origin in range(1, vertices+1):
            for goal in range(1, vertices+1):
                if origin != goal:
                    if perfectSquares.get(origin+goal):
                        if graph.get(origin) is None:
                            graph[origin] = [goal]
                        else:
                            graph[origin].append(goal)
    return graph

def hamiltonPath(graph, start_point, vertices, path = []):
    if start_point not in path:
            path.append(start_point)
            if len(path) == vertices:
                return path
            for next_pt in graph.get(start_point, []):
                res_path = [i for i in path]
                candidate = hamiltonPath(graph, next_pt, vertices, res_path)
                if candidate is not None:
                    return candidate

    

def square_sums(num):
    graph = createGraph(num)
    for i in range(1, num+1):
        graph1 = hamiltonPath(graph, i, num, [])
        if graph1 is not None:
            return graph1
    return False
    
print(perfectSquares)
print(square_sums(5))
print(square_sums(15))
print(square_sums(23))
print(square_sums(37))
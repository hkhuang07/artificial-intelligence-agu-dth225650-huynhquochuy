# This code is contributed by Anđela Niketić
def dfs(adj_list, start, target, path, visited = set()):
    path.append(start)
    visited.add(start)
    if start == target:
        return path
    for neighbour in adj_list[start]:
        if neighbour not in visited:
            result = dfs(adj_list, neighbour, target, path, visited)
            if result is not None:
                return result
            path.pop()
    return None
graph = {
  1 : [2, 3, 4, 5],
  2 : [1, 3],
  3 : [1, 2, 4, 6],
  4 : [1, 3, 5, 6],
  5 : [1, 4, 6],
  6 : [3, 4, 5]
}

traversal_path = []
traversal_path = dfs(graph, 1, 6, traversal_path)
print(traversal_path)
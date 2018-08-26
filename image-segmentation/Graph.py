import Edge

class Graph:
    def __init__(self, vertices: int):
        self._adj = []
        for _ in range(vertices):
            self._adj.append([])
        self._vertices = vertices
    
    def add_edge(self, edge: Edge.Edge):
        v = edge.start()
        w = edge.end()
        self._adj[v].append(edge)
        self._adj[w].append(edge)

    def adj(self, vertex: int):
        return iter(self._adj[vertex])
    
    def vertices(self):
        return self._vertices
    
    def edges(self):
        for edges in self._adj:
            for e in edges:
                yield e

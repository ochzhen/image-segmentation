import queue
import Graph


class BorderFinder:
    def __init__(self, graph: Graph.Graph, s: int):
        self._graph = graph
        self._reached = [False] * graph.vertices()
        self._explore_reachable_vertices(s)

    def _explore_reachable_vertices(self, s: int):
        q = queue.Queue()
        q.put(s)
        self._reached[s] = True
        while not q.empty():
            v = q.get()
            for edge in self._graph.adj(v):
                w = edge.other(v)
                if not self._reached[w] and edge.residual_capacity_to(w) > 0:
                    self._reached[w] = True
                    q.put(w)

    def border_vertices(self, excluded):
        vertices = set()
        for e in self._graph.edges():
            if ((self._reached[e.start()] and not self._reached[e.end()] or
                 not self._reached[e.start()] and self._reached[e.end()]) and
                    e.start() not in excluded and e.end() not in excluded):
                vertices.add(e.start())
                vertices.add(e.end())
        return iter(vertices)

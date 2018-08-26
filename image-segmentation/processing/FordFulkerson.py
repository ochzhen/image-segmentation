import queue
import Graph

class FordFulkerson:
    def __init__(self, graph: Graph.Graph, s: int, t: int):
        self.graph = graph
        self._marked = None
        self._edge_to = None
        self._flow = 0
        while self._has_augmenting_path(graph, s, t):
            bottleneck = float('inf')
            v = t
            while v != s:
                bottleneck = min(bottleneck, self._edge_to[v].residual_capacity_to(v))
                v = self._edge_to[v].other(v)
            v = t
            while v != s:
                self._edge_to[v].add_residual_flow_to(v, bottleneck)
                v = self._edge_to[v].other(v)
            self._flow += bottleneck
            print('flow: {0}'.format(self._flow))
    
    def _has_augmenting_path(self, graph: Graph.Graph, s: int, t: int):
        self._edge_to = [None] * graph.vertices()
        self._marked = [False] * graph.vertices()
        q = queue.Queue()
        q.put(s)
        self._marked[s] = True
        while not q.empty():
            v = q.get()
            for edge in graph.adj(v):
                w = edge.other(v)
                if edge.residual_capacity_to(w) > 0 and not self._marked[w]:
                    self._edge_to[w] = edge
                    self._marked[w] = True
                    q.put(w)
        return self._marked[t]

    def flow(self):
        return self._flow

    def in_cut(self, vertex: int):
        return self._marked[vertex]

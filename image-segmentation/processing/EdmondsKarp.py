import queue
import Graph
import common


class EdmondsKarp:
    def __init__(self, graph: Graph.Graph, s: int, t: int):
        self._graph = graph
        self._marked = [False] * graph.vertices()
        self._edge_to = [None] * graph.vertices()
        self._source = s
        self._sink = t
        self._flow = 0

    def flow(self):
        return self._flow

    def process(self):
        while self._has_augmenting_path(self._source, self._sink):
            bottleneck = float('inf')
            v = self._sink
            while v != self._source:
                bottleneck = min(bottleneck, self._edge_to[v].residual_capacity_to(v))
                v = self._edge_to[v].other(v)
            v = self._sink
            while v != self._source:
                self._edge_to[v].add_residual_flow_to(v, bottleneck)
                v = self._edge_to[v].other(v)
            self._flow += bottleneck
            print('flow: {0}'.format(self._flow))

    def _has_augmenting_path(self, s: int, t: int):
        common.fill_with_value(self._edge_to, None)
        common.fill_with_value(self._marked, False)
        q = queue.Queue()
        q.put(s)
        self._marked[s] = True
        while not q.empty():
            v = q.get()
            for edge in self._graph.adj(v):
                w = edge.other(v)
                if edge.residual_capacity_to(w) > 0 and not self._marked[w]:
                    self._edge_to[w] = edge
                    self._marked[w] = True
                    q.put(w)
        return self._marked[t]

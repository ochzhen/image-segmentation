import queue
import Graph


class PushRelabel:
    def __init__(self, graph: Graph.Graph, s: int, t: int):
        self._graph = graph
        self._source = s
        self._sink = t
        self._initialize()

    def _initialize(self):
        self._queue = queue.Queue()
        self._overflows = [0] * self._graph.vertices()
        self._heights = [0] * self._graph.vertices()
        self._heights[self._source] = self._graph.vertices()
        self._currents = [0] * self._graph.vertices()

        for edge in self._graph.adj(self._source):
            w = edge.other(self._source)
            flow = edge.residual_capacity_to(w)
            if flow == 0:
                continue
            edge.add_residual_flow_to(w, flow)
            self._overflows[w] += flow
            if self._is_regular(w):
                self._queue.put(w)

    def flow(self):
        return self._overflows[self._sink]

    def process(self):
        while not self._queue.empty():
            v = self._queue.get()
            self._discharge(v)

    def _discharge(self, v: int):
        counter = 0
        while self._overflows[v] > 0:
            counter += 1
            adj_edges = self._graph.adj(v)
            if self._currents[v] < len(adj_edges):
                edge = adj_edges[self._currents[v]]
                w = edge.other(v)
                if edge.residual_capacity_to(w) > 0 and self._heights[v] == self._heights[w] + 1:
                    flow = min(edge.residual_capacity_to(w), self._overflows[v])
                    edge.add_residual_flow_to(w, flow)
                    self._overflows[v] -= flow
                    self._overflows[w] += flow
                    if 0 < flow == self._overflows[w] and self._is_regular(w):
                        self._queue.put(w)
                else:
                    self._currents[v] += 1
            else:
                self._relabel(v)
                self._currents[v] = 0

    def _is_regular(self, v: int):
        return v != self._source and v != self._sink

    def _relabel(self, v: int):
        min_height = float('inf')
        for edge in self._graph.adj(v):
            w = edge.other(v)
            if edge.residual_capacity_to(w) > 0 and self._heights[w] < min_height:
                min_height = self._heights[w]
        self._heights[v] = min_height + 1
        print('relabel {0}'.format(self._heights[v]))

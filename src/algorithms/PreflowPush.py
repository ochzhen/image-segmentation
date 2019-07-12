import Graph


class PreflowPush:
    def __init__(self, graph: Graph.Graph, s: int, t: int):
        self._graph = graph
        self._source = s
        self._sink = t
        self._initialize()

    def _initialize(self):
        self._overflows = [0] * self._graph.vertices()
        self._heights = [0] * self._graph.vertices()
        self._heights[self._source] = self._graph.vertices()

        for edge in self._graph.adj(self._source):
            w = edge.other(self._source)
            flow = edge.residual_capacity_to(w)
            edge.add_residual_flow_to(w, flow)
            self._overflows[w] += flow

    def flow(self):
        return self._overflows[self._sink]

    def process(self):
        while True:
            print('source:{0} sink:{1}'.format(self._overflows[self._source], self._overflows[self._sink]))
            v = self._overflow_vertex_with_max_height()
            if v == -1:
                break
            if not self._try_push(v):
                self._relabel(v)

    def _try_push(self, v: int):
        for edge in self._graph.adj(v):
            w = edge.other(v)
            if edge.residual_capacity_to(w) > 0 and self._heights[v] == self._heights[w] + 1:
                flow = min(edge.residual_capacity_to(w), self._overflows[v])
                edge.add_residual_flow_to(w, flow)
                self._overflows[v] -= flow
                self._overflows[w] += flow
                return True
        return False

    def _relabel(self, v: int):
        min_height = float('inf')
        for edge in self._graph.adj(v):
            w = edge.other(v)
            if edge.residual_capacity_to(w) > 0 and self._heights[w] < min_height:
                min_height = self._heights[w]
        self._heights[v] = min_height + 1

    def _overflow_vertex_with_max_height(self):
        vertex = -1
        max_height = -1
        for v in range(self._graph.vertices()):
            if self._overflows[v] == 0 or v == self._source or v == self._sink:
                continue
            if self._heights[v] > max_height:
                vertex = v
                max_height = self._heights[v]
        return vertex

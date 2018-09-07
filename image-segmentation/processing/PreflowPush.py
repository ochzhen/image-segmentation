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
            edge.add_residual_flow_to(w, edge.capacity())
            self._overflows[w] += edge.capacity()


    def flow(self):
        return self._overflows[self._sink]


    def process(self):
        while True:
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
                print('add_residual_flow_to({0}, {1})'.format(w, flow))
                return True
        return False
    

    def _relabel(self, v: int):
        min_height = float('inf')
        for edge in self._graph.adj(v):
            w = edge.other(v)
            if edge.residual_capacity_to(w) > 0 and self._heights[w] < min_height:
                min_height = self._heights[w]
        if min_height < float('inf'):
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

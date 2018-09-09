import queue
import Graph
import common


class PushRelabelRecompute:
    def __init__(self, graph: Graph.Graph, s: int, t: int):
        self._graph = graph
        self._source = s
        self._sink = t
        self._initialize()

    def _initialize(self):
        self._queue = queue.Queue()
        self._overflows = [0] * self._graph.vertices()
        self._heights = [0] * self._graph.vertices()
        self._currents = [0] * self._graph.vertices()
        self._relabel_counter = 0
        self._visited = [False] * self._graph.vertices()

        for edge in self._graph.adj(self._source):
            w = edge.other(self._source)
            flow = edge.residual_capacity_to(w)
            if flow == 0:
                continue
            edge.add_residual_flow_to(w, flow)
            self._overflows[w] += flow
            if self._is_regular(w):
                self._queue.put(w)

        self._recompute_heights()

    def flow(self):
        return self._overflows[self._sink]

    def process(self):
        while not self._queue.empty():
            print('qsize: {0}'.format(self._queue.qsize()))
            v = self._queue.get()
            self._discharge(v)

    def _discharge(self, v: int):
        while self._overflows[v] > 0:
            adj_edges = self._graph.adj(v)
            if self._currents[v] < len(adj_edges):
                edge = adj_edges[self._currents[v]]
                w = edge.other(v)
                if edge.residual_capacity_to(w) > 0 and self._heights[v] == self._heights[w] + 1:
                    flow = min(edge.residual_capacity_to(w), self._overflows[v])
                    edge.add_residual_flow_to(w, flow)
                    self._overflows[v] -= flow
                    self._overflows[w] += flow
                    if flow == self._overflows[w] and self._is_regular(w):
                        self._queue.put(w)
                else:
                    self._currents[v] += 1
            else:
                self._relabel(v)
                if self._relabel_counter == self._graph.vertices():
                    self._recompute_heights()
                    for i in range(self._graph.vertices()):
                        self._currents[i] = 0
                self._currents[v] = 0

    def _is_regular(self, v: int):
        return v != self._source and v != self._sink

    def _relabel(self, v: int):
        self._relabel_counter += 1
        min_height = float('inf')
        for edge in self._graph.adj(v):
            w = edge.other(v)
            if edge.residual_capacity_to(w) > 0 and self._heights[w] < min_height:
                min_height = self._heights[w]
        self._heights[v] = min_height + 1

    def _recompute_heights(self):
        print('recompute_heights')
        common.fill_with_value(self._visited, False)
        common.fill_with_value(self._heights, 2 * self._graph.vertices())

        self._heights[self._sink] = 0
        self._heights[self._source] = self._graph.vertices()
        self._visited[self._sink] = True
        self._visited[self._source] = True

        q = queue.Queue()
        q.put(self._sink)
        self._process_queue_till_empty(q)
        q.put(self._source)
        self._process_queue_till_empty(q)

        self._relabel_counter = 0

    def _process_queue_till_empty(self, q: queue.Queue):
        while not q.empty():
            v = q.get()
            for edge in self._graph.adj(v):
                w = edge.other(v)
                if not self._visited[w] and edge.residual_capacity_to(v) > 0:
                    self._heights[w] = self._heights[v] + 1
                    q.put(w)
                    self._visited[w] = True

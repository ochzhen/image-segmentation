import queue
import Graph
import common


class DinicV2:
    def __init__(self, graph: Graph.Graph, s: int, t: int):
        self._graph = graph
        self._levels = [-1] * graph.vertices()
        self._blocked = [False] * graph.vertices()
        self._source = s
        self._sink = t
        self._flow = 0

    def flow(self):
        return self._flow

    def process(self):
        while self._has_augmenting_path(self._source, self._sink):
            while True:
                common.fill_with_value(self._blocked, False)
                delta = self._send_flow(float('inf'), self._source, self._sink, self._blocked)
                self._flow += delta
                if delta == 0:
                    break
                print('flow: {0}'.format(self._flow))

    def _has_augmenting_path(self, s: int, t: int):
        common.fill_with_value(self._levels, -1)
        q = queue.Queue()
        q.put(s)
        self._levels[s] = 0
        while not q.empty():
            v = q.get()
            for edge in self._graph.adj(v):
                w = edge.other(v)
                if self._levels[w] < 0 and edge.residual_capacity_to(w) > 0:
                    self._levels[w] = self._levels[v] + 1
                    q.put(w)
        return self._levels[t] >= 0

    def _send_flow(self, requested, v: int, t: int, blocked):
        if v == t:
            return requested
        flow = 0
        for edge in self._graph.adj(v):
            w = edge.other(v)
            if not blocked[w] and self._levels[w] == self._levels[v] + 1 and edge.residual_capacity_to(w) > 0:
                temp_flow = self._send_flow(min(requested - flow, edge.residual_capacity_to(w)), w, t, blocked)
                edge.add_residual_flow_to(w, temp_flow)
                flow += temp_flow
            if flow == requested:
                break
        blocked[v] = flow != requested
        return flow

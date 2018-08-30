import queue
import Graph

class Dinic:
    def __init__(self, graph: Graph.Graph, s: int, t: int):
        self._graph = graph
        self._levels = [-1] * graph.vertices()
        self._source = s
        self._sink = t
        self._flow = 0

    
    def flow(self):
        return self._flow


    def process(self):
        while self._has_augmenting_path(self._source, self._sink):
            starts = [0] * self._graph.vertices()
            while True:
                delta = self._send_flow(float('inf'), self._source, self._sink, starts)
                self._flow += delta
                if delta == 0:
                    break
                print('flow: {0}'.format(self._flow))
                
    

    def _has_augmenting_path(self, s: int, t: int):
        for i in range(len(self._levels)):
            self._levels[i] = -1
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

    
    def _send_flow(self, flow, v: int, t: int, starts):
        if v == t:
            return flow
        adj_edges = self._graph.adj(v)
        for i in range(starts[v], len(adj_edges)):
            starts[v] = i
            edge = adj_edges[i]
            w = edge.other(v)
            if self._levels[w] == self._levels[v] + 1 and edge.residual_capacity_to(w) > 0:
                flow = min(flow, edge.residual_capacity_to(w))
                temp_flow = self._send_flow(flow, w, t, starts)
                if temp_flow > 0:
                    edge.add_residual_flow_to(w, temp_flow)
                    return temp_flow
        return 0
    
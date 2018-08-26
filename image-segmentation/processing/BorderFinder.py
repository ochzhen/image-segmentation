import Graph

class BorderFinder:
    def __init__(self, flow_finder):
        self._flow_finder = flow_finder
        self._graph: Graph.Graph = flow_finder.graph

    def border_vertices(self, excluded):
        vertices = set()
        for e in self._graph.edges():
            if ((self._in_cut(e.start()) and not self._in_cut(e.end()) or 
                    not self._in_cut(e.start()) and self._in_cut(e.end())) and 
                    e.start() not in excluded and e.end() not in excluded):
                vertices.add(e.start())
                vertices.add(e.end())
        return iter(vertices)
    
    def _in_cut(self, v):
        return self._flow_finder.in_cut(v)

import Graph
import Edge
import ImageRegion as image


class GraphBuilder:
    def __init__(self, img: image.ImageRegion):
        self.img = img
        self.deltas = [(0, 1), (1, -1), (1, 0), (1, 1)]

    def build(self):
        size = self.img.size()
        s = size
        t = size + 1

        graph = Graph.Graph(size + 2)

        r0 = self.img.r0()
        c0 = self.img.c0()
        r_end = r0 + self.img.height()
        c_end = c0 + self.img.width()
        for r in range(r0, r_end):
            for c in range(c0, c_end):
                print('r:{0} c:{1}'.format(r, c))
                graph.add_edge(Edge.Edge(s, self.img.get_id(r, c), self.img.unary_background(r, c)))
                print('Unary background: {0}'.format(self.img.unary_background(r, c)))
                graph.add_edge(Edge.Edge(self.img.get_id(r, c), t, self.img.unary_foreground(r, c)))
                print('Unary foreground: {0}'.format(self.img.unary_foreground(r, c)))

                for dr, dc in self.deltas:
                    if r + dr >= r_end or c + dc >= c_end:
                        continue
                    graph.add_edge(
                        Edge.Edge(
                            self.img.get_id(r, c),
                            self.img.get_id(r + dr, c + dc),
                            self.img.binary_cost(r, c, r + dr, c + dc)
                        )
                    )
                    graph.add_edge(
                        Edge.Edge(
                            self.img.get_id(r + dr, c + dc),
                            self.img.get_id(r, c),
                            self.img.binary_cost(r, c, r + dr, c + dc)
                        )
                    )
                    print('Binary: {0}'.format(self.img.binary_cost(r, c, r + dr, c + dc)))

        return graph, s, t

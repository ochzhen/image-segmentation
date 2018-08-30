class Edge:
    def __init__(self, v: int, w: int, capacity: float):
        self._source = v
        self._sink = w
        self._capacity = capacity
        self._flow = 0

    
    def start(self):
        return self._source

    
    def end(self):
        return self._sink
    
    
    def capacity(self):
        return self._capacity
    
    
    def flow(self):
        return self._flow

    
    def other(self, u: int):
        if self.start() == u:
            return self.end()
        elif self.end() == u:
            return self.start()
        else:
            raise ValueError('Invalid input vertex')
    
    
    def residual_capacity_to(self, vertex: int):
        if vertex == self.start():
            return self.flow()
        elif vertex == self.end():
            return self.capacity() - self.flow()
        else:
            raise ValueError('Invalid input vertex')

    
    def add_residual_flow_to(self, vertex: int, delta: float):
        if vertex == self.start():
            self._flow -= delta
        elif vertex == self.end():
            self._flow += delta
        else:
            raise ValueError('Invalid input vertex')

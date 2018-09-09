import math
import cv2


def _distance(r1, c1, r2, c2):
    return math.sqrt((r2 - r1) ** 2 + (c2 - c1) ** 2)


class ImageRegion:
    def __init__(self, path: str, r0: int, c0: int, r1: int, c1: int):
        self.img = cv2.imread(path)
        self._r0 = r0
        self._c0 = c0
        self._r1 = r1
        self._c1 = c1
        self._cr = (r0 + r1) / 2
        self._cc = (c0 + c1) / 2
        self.deltas = [(0, 1), (1, -1), (1, 0), (1, 1)]
        self._alpha = 8
        rgb_distance = self.max_rgb_distance()
        self._beta = 80 / rgb_distance if rgb_distance > 0 else 1
        self._binary_coef = 100000000
        self._unary_coef = 1000
    
    def max_rgb_distance(self):
        max_distance = float('-inf')
        r0 = self.r0()
        c0 = self.c0()
        r_end = r0 + self.height()
        c_end = c0 + self.width()
        for r in range(r0, r_end):
            for c in range(c0, c_end):
                for dr, dc in self.deltas:
                    if r + dr >= r_end or c + dc >= c_end:
                        continue
                    max_distance = max(max_distance, self._rgb_distance(r, c, r + dr, c + dc))
        return max_distance

    def r0(self):
        return self._r0
    
    def c0(self):
        return self._c0

    def width(self):
        return self._c1 - self._c0 + 1

    def height(self):
        return self._r1 - self._r0 + 1

    def size(self):
        return self.width() * self.height()

    def get_id(self, r, c):
        r -= self._r0
        c -= self._c0
        return r * self.width() + c
    
    def get_coordinate(self, id):
        r = id // self.width()
        c = id % self.width()
        return r + self._r0, c + self._c0

    def unary_foreground(self, r, c):
        if self._is_border_pixel(r, c):
            return 0
        return math.ceil(self._unary_coef * (1 - self._unary_background(r, c)))

    def unary_background(self, r, c):
        if self._is_border_pixel(r, c):
            return 1000000000000
        return math.ceil(self._unary_coef * self._unary_background(r, c))

    def _is_border_pixel(self, r, c):
        return r == self._r0 or r == self._r1 or c == self._c0 or c == self._c1

    def _unary_background(self, r, c):
        return 0.4
        # return self.distance_to_center(r, c) / self.distance_to_center(self.r0(), self.c0())

    def distance_to_center(self, r, c):
        return _distance(self._cr, self._cc, r, c)

    def binary_cost(self, r0, c0, r1, c1):
        return math.ceil(self._binary_coef * ((1 / _distance(r0, c0, r1, c1)) *
            math.exp(-8 - self._beta * self._rgb_distance(r0, c0, r1, c1))))

    def _rgb_distance(self, r1, c1, r2, c2):
        B1, G1, R1 = map(int, self.img[r1, c1])
        B2, G2, R2 = map(int, self.img[r2, c2])
        return math.sqrt((B2 - B1) ** 2 + (G2 - G1) ** 2 + (R2 - R1) ** 2)
    
    def set_yellow(self, v_id):
        r, c = self.get_coordinate(v_id)
        self.img[r, c] = [0, 255, 255]
    
    def save(self, path: str):
        cv2.imwrite(path, self.img)
    
    def show(self, title):
        cv2.imshow(title, self.img)

    def close(self):
        cv2.destroyAllWindows()

    def wait_key(self):
        return cv2.waitKey(0)

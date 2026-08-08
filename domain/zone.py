class Zone:
    def __init__(self, left, right, top, bottom, cx=None, cy=None):
        self.cx = cx if cx is not None else (left + right) / 2
        self.cy = cy if cy is not None else (top + bottom) / 2
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


class Vector:

    def __init__(self, data):
        self.dims = len(data)
        self.data = data.copy()

    @property
    def x(self): return self.data[0]

    @property
    def y(self): return self.data[1]

    @property
    def z(self): return self.data[2]

    @property
    def w(self): return self.data[3]

    def __mul__(self, other):
        vector = Vector(self.data)
        for i in range(vector.dims):
            vector[i] *= other
        return vector

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

class Matrix:

    def __init__(self, data):
        self.rows = len(data)
        self.cols = len(data[0])
        self.data = data.copy()

    def __mul__(self, other):
        if type(other) == Matrix:
            matrix = Matrix([[0 for i in range(other.cols)] for j in range(self.rows)])
            for i in range(matrix.rows):
                for j in range(matrix.cols):
                    for k in range(self.cols):
                        matrix[i, j] += self.__getitem__((i, k)) * other[k, j]
            return matrix
        
        vector = Vector([0 for i in range(self.rows)])
        for i in range(self.rows):
            for j in range(self.cols):
                vector[i] += self.__getitem__((i, j)) * other[j]

        return vector

    def __setitem__(self, key, value):
        row, col = key
        self.data[row][col] = value

    def __getitem__(self, key):
        row, col = key
        return self.data[row][col]

    def __str__(self):
        return '\n'.join(', '.join(map(str, row)) for row in self.data)

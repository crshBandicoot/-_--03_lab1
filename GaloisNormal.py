from mul_matrix import matrix


class GaloisFieldPolynom:
    deg = 431
    matrix = matrix

    def __init__(self, vector: str) -> None:
        vector = vector.lstrip('0')
        vector = vector[-431:]
        for bit in vector:
            if bit not in '01':
                raise ValueError('Invalid polynom format')
        self.vector = '0' * (self.deg - len(vector)) + vector

    def __add__(self, other: 'GaloisFieldPolynom') -> 'GaloisFieldPolynom':
        result = ''
        for x, y in zip(self.vector, other.vector):
            if x == y:
                result += '0'
            else:
                result += '1'
        return GaloisFieldPolynom(result)

    def __mul__(self, other):
        result = ''
        for i in range(self.deg):
            result += self.mul_mtr(self << i, other << i)
        return GaloisFieldPolynom(result)

    def mul_mtr(self, left, right):
        first = ''
        for i in range(self.deg):
            cell = 0
            for j in range(self.deg):
                a = int(left.vector[j])
                b = int(self.matrix[i][j])
                cell += a*b
            first += str(cell % 2)
        result = 0
        for i in range(self.deg):
            result += int(first[i]) * int(right.vector[i])
        return str(result % 2)

    def trace(self):
        result = GaloisFieldPolynom('0')
        prev = self
        for _ in range(self.deg):
            val = prev*prev
            result += val
            prev = val
        return result

    def inverse(self):
        return self**((2**self.deg) - 2)

    def __pow__(self, pow):
        result = GaloisFieldPolynom('1'*431)
        for _ in range(pow):
            result *= self
        return result

    def __lshift__(self, value):
        vector = self.vector[value:] + self.vector[:value]
        return GaloisFieldPolynom(vector)

    def __rshift__(self, value):
        vector = self.vector[-value:] + self.vector[:-value]
        return GaloisFieldPolynom(vector)

    def __eq__(self, other):
        return self.vector == other.vector

    def __ne__(self, other):
        return self.vector != other.vector

    def __repr__(self) -> str:
        repr = self.vector.lstrip('0')
        if repr:
            return repr
        return '0'




class GaloisFieldPolynom:
    deg = 431
    gen = '101011'

    def __init__(self, vector: str) -> None:
        vector = vector.lstrip('0')
        for bit in vector:
            if bit not in '01':
                raise ValueError('Invalid polynom format')
        if len(vector) > self.deg:
            result = GaloisFieldPolynom(vector[-431:])
            for i in range(self.deg, len(vector)):
                if vector[::-1][i] == '1':
                    result += GaloisFieldPolynom(self.gen) << (i - self.deg)
            self.vector = result.vector
        else:
            self.vector = '0' * (self.deg - len(vector)) + vector

    def __add__(self, other: 'GaloisFieldPolynom') -> 'GaloisFieldPolynom':
        result = ''
        for x, y in zip(self.vector, other.vector):
            if x == y:
                result += '0'
            else:
                result += '1'
        return GaloisFieldPolynom(result)

    def __lshift__(self, value) -> 'GaloisFieldPolynom':
        return GaloisFieldPolynom(self.vector + '0' * value)

    def __eq__(self, other):
        return self.vector == other.vector

    def __ne__(self, other):
        return self.vector != other.vector

    def __mul__(self, other: 'GaloisFieldPolynom') -> 'GaloisFieldPolynom':
        result = GaloisFieldPolynom('0')
        for i in range(len(other.vector)):
            if other.vector[i] == '1':
                result += (self << (len(other.vector) - i - 1))
        return result

    def __pow__(self, pow: int) -> 'GaloisFieldPolynom':
        result = GaloisFieldPolynom('1')
        pow = bin(pow)[2:]
        for bit in pow:
            result = result * result
            if bit == '1':
                result = result * self
        return result

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

    def __len__(self):
        return len(self.vector.lstrip('0'))

    def __repr__(self) -> str:
        repr = self.vector.lstrip('0')
        if repr:
            return repr
        return '0'


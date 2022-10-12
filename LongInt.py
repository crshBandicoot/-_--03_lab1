from textwrap import wrap
from random import randint


class LongInt:
    hex_charset = '0123456789abcdef'
    numeral_system = 16
    length = 512

    def __init__(self, number):
        match number:
            case True:
                number = '1'
            case False:
                number = '0'
            case _:
                number = number[-self.length:]
                for char in number.lower():
                    if char not in self.hex_charset:
                        print('Invalid number format!')
                        number = ''
                        break
        self.number = '0' * (self.length - len(number)) + number.lower()

    def to_binary(self):
        result = ''
        number = self.number.lstrip('0')
        for i in number:
            if i == '0':
                result = result + '0000'
            elif i == '1':
                result = result + '0001'
            elif i == '2':
                result = result + '0010'
            elif i == '3':
                result = result + '0011'
            elif i == '4':
                result = result + '0100'
            elif i == '5':
                result = result + '0101'
            elif i == '6':
                result = result + '0110'
            elif i == '7':
                result = result + '0111'
            elif i == '8':
                result = result + '1000'
            elif i == '9':
                result = result + '1001'
            elif i == 'a':
                result = result + '1010'
            elif i == 'b':
                result = result + '1011'
            elif i == 'c':
                result = result + '1100'
            elif i == 'd':
                result = result + '1101'
            elif i == 'e':
                result = result + '1110'
            elif i == 'f':
                result = result + '1111'
        return '0' * (self.length * 4 - len(result)) + result

    def from_binary(self, binary):
        result = ''
        result_arr = tuple(wrap(binary, 4))
        for binary in result_arr:
            if binary == '0000':
                result = result + '0'
            elif binary == '0001':
                result = result + '1'
            elif binary == '0010':
                result = result + '2'
            elif binary == '0011':
                result = result + '3'
            elif binary == '0100':
                result = result + '4'
            elif binary == '0101':
                result = result + '5'
            elif binary == '0110':
                result = result + '6'
            elif binary == '0111':
                result = result + '7'
            elif binary == '1000':
                result = result + '8'
            elif binary == '1001':
                result = result + '9'
            elif binary == '1010':
                result = result + 'a'
            elif binary == '1011':
                result = result + 'b'
            elif binary == '1100':
                result = result + 'c'
            elif binary == '1101':
                result = result + 'd'
            elif binary == '1110':
                result = result + 'e'
            elif binary == '1111':
                result = result + 'f'
        return result

    def __lshift__(self, value):
        binary = self.to_binary()
        return LongInt(self.from_binary(binary[value:] + '0' * value))

    def __rshift__(self, value):
        if value == 0:
            return self
        binary = self.to_binary()
        return LongInt(self.from_binary('0' * value + binary[:-value]))

    def elder_bit(self):
        binary = self.to_binary().lstrip('0')
        return len(binary) - 1

    def __add__(self, value):
        result = ''
        next_add = False
        for x, y in zip(self.number[::-1], value.number[::-1]):
            single_add = self.hex_charset.index(x) + self.hex_charset.index(y) + next_add
            if single_add >= self.numeral_system:
                next_add = True
                single_add = single_add % self.numeral_system
            else:
                next_add = False
            result = self.hex_charset[single_add] + result
        return LongInt(result)

    def __sub__(self, value):
        if self < value:
            return LongInt('0')
        result = ''
        next_sub = False
        for x, y in zip(self.number[::-1], value.number[::-1]):
            single_sub = self.hex_charset.index(x) - self.hex_charset.index(y) - next_sub
            if single_sub < 0:
                next_sub = True
                single_sub = single_sub + self.numeral_system
            else:
                next_sub = False
            result = self.hex_charset[single_sub] + result
        return LongInt(result)

    def __mul__(self, value):
        binary = value.to_binary()
        result = LongInt('0')
        for i in range(len(binary)):
            if binary[i] == '1':
                result = result + (self << (len(binary) - i - 1))
        return result

    def __truediv__(self, value):
        if str(value) == '0':
            return None
        if self < value:
            return LongInt('0'), self
        shifts = self.elder_bit() - value.elder_bit()
        rem = LongInt(self.number)
        divider = value << (shifts)
        result = ''
        for _ in range(shifts + 1):
            if rem < divider:
                result = result + '0'
            else:
                result = result + '1'
                rem = rem - divider
            divider = divider >> 1
        result = LongInt(self.from_binary('0' * (self.length * 4 - len(result)) + result))
        return result, rem

    def __pow__(self, value):
        if str(value) == '0':
            return LongInt('1')
        if str(value) == '1':
            return self
        result = LongInt('1')
        binary = value.to_binary().lstrip('0')
        for i in binary:
            result = result * result
            if i == '1':
                result = result * self
        return result

    # lab 2
    def is_even(self):

        if self.hex_charset.index(self.number[-1]) % 2 == 0:
            return True
        return False

    def is_2_pow(self):
        if self.to_binary().count('1') == 1:
            return True
        return False

    def __mod__(self, value):
        if str(value) == '0' or value > self:
            return self
        if value.is_2_pow():
            result = self.to_binary()[-value.elder_bit():]
            return LongInt(self.from_binary('0' * (self.length * 4 - len(result)) + result))
        if self.elder_bit() < value.elder_bit()*2:
            k = value.elder_bit() + 1
            r = ((LongInt('1') << (2*k))/value)[0]
            t = self - (((self*r) >> (2*k))*value)
            if t < value:
                return t
            return t - value
        else:
            return self - (self/value)[0]*value

    def gcd(self, value):
        if str(self) == '0' or str(value) == '0':
            return max(self, value)
        a = self
        b = value
        d = 0
        while a.is_even() and b.is_even():
            a = a >> 1
            b = b >> 1
            d += 1
        while a.is_even():
            a = a >> 1
        while str(b) != '0':
            while b.is_even():
                b = b >> 1
            if a > b:
                a, b = b, a
            b = b-a
        return a << d

    def lcm(self, value):
        return ((self * value) / (self.gcd(value)))[0]

    def add_mod(self, value, mod):
        return (self+value) % mod

    def sub_mod(self, value, mod):
        return (self-value) % mod

    def mul_mod(self, value, mod):
        return ((self % mod)*(value % mod)) % mod

    def pow_barrett(self, value, mod):
        if str(value) == '0':
            return LongInt('1')
        if str(value) == '1':
            return self
        result = LongInt('1')
        binary = value.to_binary().lstrip('0')
        k = mod.elder_bit() + 1
        r = ((LongInt('1') << (2*k))/mod)[0]
        for i in binary:
            result = result * result
            if result > mod:
                if mod.is_2_pow():
                    result = result.to_binary()[-mod.elder_bit():]
                    result = LongInt(self.from_binary('0' * (len(result) * 4 - len(result)) + result))
                elif result.elder_bit() < mod.elder_bit()*2:
                    k = mod.elder_bit() + 1
                    r = ((LongInt('1') << (2*k))/mod)[0]
                    t = result - (((result*r) >> (2*k))*mod)
                    if t < mod:
                        result = t
                    else:
                        result = t - mod
                else:
                    result = result - (result/mod)[0]*mod
            if i == '1':
                result = result*self
                if result > mod:
                    if mod.is_2_pow():
                        result = result.to_binary()[-mod.elder_bit():]
                        result = LongInt(self.from_binary('0' * (len(result) * 4 - len(result)) + result))
                    elif result.elder_bit() < mod.elder_bit()*2:
                        k = mod.elder_bit() + 1
                        r = ((LongInt('1') << (2*k))/mod)[0]
                        t = result - (((result*r) >> (2*k))*mod)
                        if t < mod:
                            result = t
                        else:
                            result = t - mod
                    else:
                        result = result - (result/mod)[0]*mod
        return result

    def randrange(self, start, stop):
        start = int(str(start), base=16)
        stop = int(str(stop), base=16)
        return LongInt(hex(randint(start, stop))[2:])

    def miller_rabin(self, tries):
        if str(self) == '2':
            return True
        if self.is_even():
            return False
        r = 0
        d = self - LongInt('1')
        while d.is_even():
            r += 1
            d = d >> 1
        for _ in range(tries):
            a = self.randrange(LongInt('2'), self-LongInt('1'))
            if str(a.pow_barrett(d, self)) == '1':
                continue
            for i in range(r):
                if a.pow_barrett(d << (2*i), self) == self - LongInt('1'):
                    break
            else:
                return False
        return True

    def __eq__(self, other):
        if self.number == other.number:
            return True
        return False

    def __lt__(self, other):
        if self.number < other.number:
            return True
        return False

    def __le__(self, other):
        if self.number <= other.number:
            return True
        return False

    def __gt__(self, other):
        if self.number > other.number:
            return True
        return False

    def __ge__(self, other):
        if self.number >= other.number:
            return True
        return False

    def __ne__(self, other):
        if self.number != other.number:
            return True
        return False

    def __repr__(self):
        repr = self.number.lstrip('0')
        if not repr:
            repr = '0'
        return repr



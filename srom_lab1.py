from time import time
from random import choices
from textwrap import wrap
from matplotlib import pyplot


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
        return '0' * (self.length*4 - len(result)) + result

    def from_binary(self, binary):
        result = ''
        result_arr = tuple(wrap(binary, 4))
        for binary in result_arr:
            if binary == '0000':
                result = result + '0'
            elif binary == '0001':
                result = result+'1'
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

    def lshift(self, value=1):
        binary = self.to_binary()
        return LongInt(self.from_binary(binary[value:] + '0' * value))

    def rshift(self, value=1):
        binary = self.to_binary()
        return LongInt(self.from_binary('0' * value + binary[:-value]))

    def elder_bit(self):
        binary = self.to_binary().lstrip('0')
        return len(binary)-1

    def add(self, value):
        result = ''
        next_add = False
        for i in range(self.length - 1, -1, -1):
            single_add = self.hex_charset.index(self.number[i]) + self.hex_charset.index(value.number[i]) + next_add
            if single_add >= self.numeral_system:
                next_add = True
                single_add = single_add % self.numeral_system
            else:
                next_add = False
            result = self.hex_charset[single_add] + result
        return LongInt(result)

    def lt(self, value):
        for i in range(self.length):
            if self.hex_charset.index(self.number[i]) > self.hex_charset.index(value.number[i]):
                return False
            elif self.hex_charset.index(self.number[i]) < self.hex_charset.index(value.number[i]):
                return True
        return False

    def sub(self, value):
        if self.lt(value):
            return LongInt('')
        result = ''
        next_sub = False
        for i in range(self.length - 1, -1, -1):
            single_sub = self.hex_charset.index(self.number[i]) - self.hex_charset.index(value.number[i]) - next_sub
            if single_sub < 0:
                next_sub = True
                single_sub = single_sub + self.numeral_system
            else:
                next_sub = False
            result = self.hex_charset[single_sub] + result
        return LongInt(result)

    def mul(self, value):
        binary = value.to_binary()
        result = LongInt('')
        for i in range(len(binary)):
            if binary[i] == '1':
                result = result.add(self.lshift(len(binary)-i-1))
        return result

    def div(self, value):
        if str(value) == '0':
            return None
        if self.lt(value):
            return LongInt(''), self
        shifts = self.elder_bit() - value.elder_bit()
        rem = LongInt(self.number)
        divider = value.lshift(shifts)
        result = ''
        for _ in range(shifts+1):
            if rem.lt(divider):
                result = result + '0'
            else:
                result = result + '1'
                rem = rem.sub(divider)
            divider = divider.rshift()
        result = LongInt(self.from_binary('0'*(self.length*4-len(result)) + result))
        return result, rem

    def pow(self, value):
        value = int(value.number, base=16)
        if value < 0:
            return None
        if value == 0:
            return LongInt('1')
        if value == 1:
            return self
        result = LongInt('1')
        binary = bin(value)[2:]
        for i in range(len(binary)):
            result = result.mul(result)
            if binary[i] == '1':
                result = result.mul(self)
        return result

    def __repr__(self):
        repr = self.number.lstrip('0')
        if not repr:
            repr = '0'
        return repr


x = LongInt(''.join(choices('0123456789abcdef', k=512)))
result = x
for i in range(300):
    result = result.add(x)
if str(result) != str(x.mul(LongInt('12d'))):
    print('ERROR!')

for i in range(10):
    print(i)
    a = LongInt(''.join(choices('0123456789abcdef', k=512)))
    b = LongInt(''.join(choices('0123456789abcdef', k=512)))
    c = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1 = a.add(b).mul(c)  # (a+b)*c
    num2 = c.mul(a.add(b))  # c*(a+b)
    num3 = a.mul(c).add(b.mul(c))  # a*c+b*c
    if str(num1) != str(num2) != str(num3):
        print('ERROR!')
        break


start_init = time()
for _ in range(1000):
    num = LongInt(''.join(choices('0123456789abcdef', k=512)))
end_init = time()
start_to_binary = time()
for _ in range(1000):
    num = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num.to_binary()
end_to_binary = time()

start_from_binary = time()
for _ in range(1000):
    num = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num.from_binary(num.to_binary())
end_from_binary = time()

start_lshift = time()
for _ in range(1000):
    num = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num.lshift()
end_lshift = time()

start_rshift = time()
for _ in range(1000):
    num = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num.rshift()
end_rshift = time()

start_elder_bit = time()
for _ in range(1000):
    num = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num.elder_bit()
end_elder_bit = time()

start_add = time()
for _ in range(1000):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1.add(num2)
end_add = time()

start_sub = time()
for _ in range(1000):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1.sub(num2)
end_sub = time()

start_lt = time()
for _ in range(1000):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1.lt(num2)
end_lt = time()

start_mul = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1.mul(num2)
end_mul = time()

start_div = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1.div(num2)
end_div = time()

start_pow = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=3)))
    num1.pow(num2)
end_pow = time()

init = end_init-start_init
to_bin = end_to_binary - start_to_binary - init
from_bin = end_from_binary - start_from_binary - init - to_bin
lshift = end_lshift - start_lshift - init
rshift = end_rshift - start_rshift - init
elder_bit = end_elder_bit - start_elder_bit - init
add = end_add - start_add-init*2
sub = end_sub - start_sub - init*2
lt = end_lt - start_lt - init*2
mul = (end_mul-start_mul-init*2)*100
div = (end_div-start_div-init*2)*100
pow = (end_pow-start_pow-init*2)*100
print(pow)
pyplot.bar(['init', 'to_bin', 'from_bin', 'lshift', 'rshift', 'elder_bit', 'add', 'sub', 'lt'], [init, to_bin, from_bin, lshift, rshift, elder_bit, add, sub, lt])
pyplot.figure()
pyplot.bar(['mul', 'div'], [mul, div])
pyplot.show()

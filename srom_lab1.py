import time
import random
from textwrap import wrap


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
        return True

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
        result = LongInt(self.from_binary('0'*(2048-len(result)) + result))
        return result, self.sub(result.mul(value))

    def pow(self, value):
        value = int(value.number, base=16)
        if value < 0:
            return None
        if value == 0:
            return LongInt('1')
        if value == 1:
            return value
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


start = time.time()

num1 = LongInt(''.join(random.choices('0123456789abcdef', k=512)))
num2 = LongInt('d12')
# num3 = LongInt('D4D2110984907B5625309D956521BAB4157B8B1ECE04043249A3D379AC112E5B9AF44E721E148D88A942744CF56A06B92D28A0DB950FE4CED2B41A0BD38BCE7D0BE1055CF5DE38F2A588C2C9A79A75011058C320A7B661C6CE1C36C7D870758307E5D2CF07D9B6E8D529779B6B2910DD17B6766A7EFEE215A98CAC300F2827DB')
# num4 = LongInt('3A7EF2554E8940FA9B93B2A5E822CC7BB262F4A14159E4318CAE3ABF5AEB1022EC6D01DEFAB48B528868679D649B445A753684C13F6C3ADBAB059D635A2882090FC166EA9F0AAACD16A062149E4A0952F7FAAB14A0E9D3CB0BE9200DBD3B0342496421826919148E617AF1DB66978B1FCD28F8408506B79979CCBCC7F7E5FDE7')
# print(num3.mul(num4).div(num4))
num1.pow(num2)
end = time.time()
print(end-start)

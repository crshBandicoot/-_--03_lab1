from time import time
from random import choices
from matplotlib import pyplot
from LongInt import LongInt

x = LongInt('D4D2110984907B5625309D956521BAB4157B8B1ECE04043249A3D379AC112E5B9AF44E721E148D88A942744CF56A06B92D28A0DB950FE4CED2B41A0BD38BCE7D0BE1055CF5DE38F2A588C2C9A79A75011058C320A7B661C6CE1C36C7D870758307E5D2CF07D9B6E8D529779B6B2910DD17B6766A7EFEE215A98CAC300F2827DB')
y = LongInt('3A7EF2554E8940FA9B93B2A5E822CC7BB262F4A14159E4318CAE3ABF5AEB1022EC6D01DEFAB48B528868679D649B445A753684C13F6C3ADBAB059D635A2882090FC166EA9F0AAACD16A062149E4A0952F7FAAB14A0E9D3CB0BE9200DBD3B0342496421826919148E617AF1DB66978B1FCD28F8408506B79979CCBCC7F7E5FDE7')
print(x*y/y)

x = LongInt(''.join(choices('0123456789abcdef', k=512)))
result = x
for i in range(300):
    result = result + x
if result != x * LongInt('12d'):
    print('ERROR!')

for i in range(10):
    a = LongInt(''.join(choices('0123456789abcdef', k=512)))
    b = LongInt(''.join(choices('0123456789abcdef', k=512)))
    c = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1 = (a + b) * c
    num2 = c*(a+b)
    num3 = a*c + b*c  # a*c+b*c
    if num1 != num2 != num3:
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
    num << 1
end_lshift = time()

start_rshift = time()
for _ in range(1000):
    num = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num >> 1
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
    num1 + num2
end_add = time()


start_sub = time()
for _ in range(1000):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1 - num2
end_sub = time()


start_mul = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1 * num2
end_mul = time()

start_div = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num1/num2
end_div = time()

start_pow = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=512)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=3)))
    num1 ** num2
end_pow = time()

init = end_init-start_init
to_bin = end_to_binary - start_to_binary - init
from_bin = end_from_binary - start_from_binary - init - to_bin
lshift = end_lshift - start_lshift - init
rshift = end_rshift - start_rshift - init
elder_bit = end_elder_bit - start_elder_bit - init
add = end_add - start_add-init*2
sub = end_sub - start_sub - init*2
mul = (end_mul-start_mul-init*2/100)*100
div = (end_div-start_div-init*2/100)*100
pow = (end_pow-start_pow-init*2/100)*100
print(pow)
pyplot.bar(['init', 'to_bin', 'from_bin', 'lshift', 'rshift', 'elder_bit', 'add', 'sub'], [init, to_bin, from_bin, lshift, rshift, elder_bit, add, sub])
pyplot.figure()
pyplot.bar(['mul', 'div'], [mul, div])
pyplot.show()


from time import time
from random import choices, randint
from matplotlib import pyplot
from LongInt import LongInt


for i in range(10):
    print(i)
    a = LongInt(''.join(choices('0123456789abcdef', k=128)))
    b = LongInt(''.join(choices('0123456789abcdef', k=128)))
    c = LongInt(''.join(choices('0123456789abcdef', k=3)))
    mod = LongInt(''.join(choices('0123456789abcdef', k=randint(2, 64))))
    if (a % mod) != (a - ((a/mod)[0]*mod)):
        print('ERROR1')
    if (a.add_mod(b, mod)) != ((a+b) - ((a+b)/mod)[0]*mod):
        print('ERROR2')
    if (a.sub_mod(b, mod)) != ((a-b) - ((a-b)/mod)[0]*mod):
        print('ERROR3')
    if (a*b % mod) != (a.mul_mod(b, mod)):
        print('ERROR4')


start_init = time()
for _ in range(1000):
    num = LongInt(''.join(choices('0123456789abcdef', k=128)))
end_init = time()
init = end_init-start_init


start_gcd = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num1.gcd(num2)
end_gcd = time()

start_lcm = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num1.lcm(num2)
end_lcm = time()

start_add_mod = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    mod = LongInt(''.join(choices('0123456789abcdef', k=randint(2, 64))))
    num1.add_mod(num2, mod)
end_add_mod = time()

start_sub_mod = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    mod = LongInt(''.join(choices('0123456789abcdef', k=randint(2, 64))))
    num1.sub_mod(num2, mod)
end_sub_mod = time()

start_add_mod = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    mod = LongInt(''.join(choices('0123456789abcdef', k=randint(2, 64))))
    num1.add_mod(num2, mod)
end_add_mod = time()

start_mul_mod = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    mod = LongInt(''.join(choices('0123456789abcdef', k=randint(2, 64))))
    num1.mul_mod(num2, mod)
end_mul_mod = time()

start_pow_barrett = time()
for _ in range(10):
    num1 = LongInt(''.join(choices('0123456789abcdef', k=128)))
    num2 = LongInt(''.join(choices('0123456789abcdef', k=3)))
    mod = LongInt(''.join(choices('0123456789abcdef', k=randint(2, 64))))
    num1.pow_barrett(num2, mod)
end_pow_barrett = time()

start_miller_rabin = time()
for i in range(10):
    a = LongInt(''.join(choices('0123456789abcdef', k=16)))
    a.miller_rabin(1)
end_miller_rabin = time()

init = end_init - start_init
gcd = (end_gcd - start_gcd - init*2/100) / 10
lcm = (end_lcm - start_lcm - init*2/100) / 10
add_mod = (end_add_mod - start_add_mod - init*2/100)/10
sub_mod = (end_sub_mod - start_sub_mod-init*2/100)/10
mul_mod = (end_mul_mod - start_mul_mod-init*2/100)/10
pow_barrett = (end_pow_barrett - start_pow_barrett-init*2/100)/10
miller_rabin = (end_miller_rabin-start_miller_rabin-init/100)/10
pyplot.bar(['gcd', 'lcm', 'add_mod', 'sub_mod', 'mul_mod', 'pow_barrett'], [gcd, lcm, add_mod, sub_mod, mul_mod, pow_barrett])
pyplot.show()
print(miller_rabin)

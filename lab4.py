from time import time
from random import choices
from matplotlib import pyplot
from GaloisNormal import GaloisFieldPolynom


for i in range(1):
    a = GaloisFieldPolynom(''.join(choices('01', k=128)))
    b = GaloisFieldPolynom(''.join(choices('01', k=128)))
    c = GaloisFieldPolynom(''.join(choices('01', k=3)))
    if (a+b)*c != (a*c + b*c):
        raise Exception
    if a**(2**a.deg - 1) != GaloisFieldPolynom('1'*431):
        raise Exception
    result = GaloisFieldPolynom('1'*431)
    for _ in range(100):
        result *= c
    if result != c**100:
        raise Exception
    if c.inverse() * c != GaloisFieldPolynom('1'*431):
        raise Exception
print('passed')

start_init = time()
for _ in range(1000):
    num = GaloisFieldPolynom(''.join(choices('01', k=128)))
end_init = time()
init = end_init-start_init


start_inverse = time()
num = GaloisFieldPolynom(''.join(choices('01', k=128)))
num.inverse()
end_inverse = time()

start_trace = time()
num = GaloisFieldPolynom(''.join(choices('01', k=128)))
num.trace()
end_trace = time()

start_add = time()
for _ in range(10):
    num1 = GaloisFieldPolynom(''.join(choices('01', k=128)))
    num2 = GaloisFieldPolynom(''.join(choices('01', k=128)))
    num1+num2
end_add = time()

start_mul = time()
for _ in range(10):
    num1 = GaloisFieldPolynom(''.join(choices('01', k=128)))
    num2 = GaloisFieldPolynom(''.join(choices('01', k=128)))
    num1*num2
end_mul = time()

start_pow = time()
for _ in range(10):
    num1 = GaloisFieldPolynom(''.join(choices('01', k=128)))
    num1**128
end_pow = time()


init = end_init - start_init
inverse = (end_inverse - start_inverse - init/1000)
trace = (end_trace - start_trace - init/1000)
add = (end_add - start_add - init*2/1000)/10
mul = (end_mul - start_mul - init*2/1000)/10
pow = (end_pow - start_pow - init/1000)/10
print(f'{trace=}')
print(f'{inverse=}')
pyplot.bar(['add', 'mul', 'pow'], [addz, mul, pow])
pyplot.show()

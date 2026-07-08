# Yield from

def gen1():
    yield 1
    yield 2
    yield 3
    print('Acabou GEN 1')

def gen3():
    yield 10
    yield 20
    yield 30
    print('Acabou GEN 3')


def gen2(gen):
    yield from gen()
    yield 4
    yield 5
    yield 6
    print('Acabou GEN 2')

g1 = gen2(gen1)
g2 = gen2(gen3)
for numero in g1:
    print(numero)
for numero in g2:
    print(numero)
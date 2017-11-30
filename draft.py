from numpy.random import RandomState

random = RandomState()
res = random.multinomial(1, [1.0/6.0] * 6, size=None)
print(res)

from copy import copy, deepcopy


class AIPlayer:
    temp = []


test = AIPlayer()
print(test)

x = deepcopy(test)
print(x)
x.temp = [2]
print(x.temp)
print(test.temp)
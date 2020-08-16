def mymap(func, *iterables):
    for t in zip(*iterables):
        yield func(*t)


def plus(a):
    return a + 1


def add(a, b):
    return a + b


print(list(mymap(plus, [1, 2, 3])))
print(list(mymap(add, [1, 2, 3], [1, 2, 3])))

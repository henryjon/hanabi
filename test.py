class a(object):
    def __init__(self, n):
        self.l = n * [None]


class A(object):
    def __init__(self, a):
        print("init A")
        self.a = a


a1 = a(5)
A1 = A(a1)
A2 = A(a1)

print(A1.a.l)
print(A2.a.l)

A2.a.l[0] = 1

print(A1.a.l)
print(A2.a.l)

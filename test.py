class A:

    def __init__(self, num):
        self.field = num


arr = []
a = A(1)
arr.append(a)
del a

print(arr)
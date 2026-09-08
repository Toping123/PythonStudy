"""
|运算符其实就是类中的__or__方法，重写即可
"""
class Test(object):

    def __init__(self, name):
        self.name = name

    def __or__(self, other):
        return Temp(self, other)

    def __str__(self) -> str:
        return self.name


class Temp(object):
    def __init__(self, *args):
        self.char_list = []
        for arg in args:
            self.char_list.append(arg)

    def __or__(self, other):
        self.char_list.append(other)
        return self

    def run(self):
        for char in self.char_list:
            print(char)


if __name__ == '__main__':
    a = Test("a")
    b = Test("b")
    c = Test("c")
    d = Test("d")
    result = a | b | c | d
    result.run()

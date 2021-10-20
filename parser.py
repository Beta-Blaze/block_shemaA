class Parser:
    def __init__(self, data=''):
        self.data = data
        self.defines = []
        self.parse_defines_with_brackets = []
        self.parse_defines_without_brackets = []

    def read(self, name):
        with open(name) as f:
            self.data = f.readlines()

    def normalize(self):
        ...

    def prepare(self):
        emp = []
        rubbish = ['#include', 'namespace']
        for i in self.data:
            if not any([r in i for r in rubbish]) and i != '\n':
                emp.append(i[:-1])
            if 'define' in i:
                self.defines.append(i)
        self.data = emp

    def define(self):
        for i in self.defines:
            i = ' '.join(i.split()[1:])
            try:  # TODO define без скобок(переменных)
                perem = i[i.index('(') + 1: i.index(')')]
            except Exception:
                name = i.split()[0]
                temp = ' '.join(i.split()[1:])
                self.parse_defines_without_brackets.append([name, temp])
                continue
            name = i[: i.index('(')]
            i = i[i.index(')') + 1:]
            symb = '+ - * / % ^ & | ~ ! = < >  = < > , ( ) [ ]'.split(' ') + [' ']
            ids = []
            for b in range(0, len(i) - len(perem)):
                if i[b: b + len(perem)] == perem:
                    if i[b - 1] in symb:
                        if b + len(perem) + 1 in range(0, len(i) - len(perem)):
                            if i[b + len(perem) + 1]:
                                ids.append([b, b + len(perem)])
                        else:
                            ids.append([b, b + len(perem)])
            temp = []
            i2 = i
            for id_ in ids[::-1]:
                temp.insert(0, i2[id_[1]:])
                i2 = i2[:id_[0]]
            temp.insert(0, i2)
            self.parse_defines_with_brackets.append([name, perem, temp])


p = Parser()
p.read('primer.cpp')
p.prepare()
# print(*p.data, sep='\n')
p.define()
print(p.parse_defines_with_brackets)
print(p.parse_defines_without_brackets)
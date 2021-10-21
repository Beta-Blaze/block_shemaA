import subprocess
import re


class Parser:
    def __init__(self, data=''):
        self.data = data
        self.defines = []
        self.funcs = {}
        self.parse_defines_with_brackets = {}
        self.parse_defines_without_brackets = {}

    def read(self, name):
        subprocess.Popen(f".\\helpers\\formatter.exe --i --style=Google {name}")
        with open(name) as f:
            self.data = f.readlines()

    def prepare(self):
        emp = []
        rubbish = ['#include', 'namespace']
        for i in self.data:
            if not any([r in i for r in rubbish]) and i != '\n':
                emp.append(i[:-1])
            if 'define' in i:
                self.defines.append(i[:-1])
        self.data = emp

    def define(self):
        for i in self.defines:
            i: str = i[8:]
            if i[i.index(' ') - 1] != ')':
                name = i.split()[0]
                temp = ' '.join(i.split()[1:])
                self.parse_defines_without_brackets[name] = temp
                continue
            perem = i[i.index('(') + 1: i.index(')')]
            name = i[: i.index('(')]
            i = i[i.index(')') + 2:]
            symb = '+ - * / % ^ & | ~ ! = < >  = < > , ( ) [ ]'.split(' ') + [' ']
            ids = []
            for b in range(0, len(i) - len(perem) + 1):
                if i[b: b + len(perem)] == perem:
                    if i[b - 1] in symb:
                        if b + len(perem) + 1 in range(0, len(i) - len(perem)):
                            if i[b + len(perem) + 1]:
                                ids.append([b, b + len(perem)])
                        else:
                            ids.append([b, b + len(perem)])
            temp = []
            for i2 in ids[::-1]:
                temp.insert(0, i[i2[1]:])
                i = i[:i2[0]]
            temp.insert(0, i)
            self.parse_defines_with_brackets[name] = [temp]

    def parse_variables(self, string: str) -> list[str, str | None] | None:
        keywords = "bool char wchar_t char8_t char16_t char32_t int short long signed unsigned float double".split()
        if any([string.startswith(i) for i in keywords]):
            for keyword in keywords:
                string = string.replace(keyword, "").lstrip()
            if re.match(r"[A-z]*?;", string):
                return [string.rstrip(";"), None]
            initialization = re.search(r'[{].*?[}]', string)
            if initialization:
                return [string[0:initialization.start()], string[initialization.start()+1:initialization.end()-1] if string[initialization.start()+1:initialization.end()-1] else None]
            if re.search(r"[A-z]*? = .*?", string):
                var = string.split(" = ")
                return [var[0], var[1].rstrip(";")]

    def find_func(self):  #TODO typedef void F(); F  fv;
        keywords = "bool char wchar_t char8_t char16_t char32_t int float double void".split()
        for s in range(len(self.data)):
            if any([self.data[s].startswith(i) for i in keywords]) and '{' in self.data[s] and '}' not in self.data[s]:
                index = s
                name = self.data[s][self.data[s].index(' ') + 1: self.data[s].index('(')]
            elif self.data[s] == '}':
                self.funcs[name] = self.data[index: s + 1]


p = Parser()
p.read('primer.cpp')
p.prepare()
# print(*p.data, sep='\n')
p.define()
# print(p.parse_defines_with_brackets)
# print(p.parse_defines_without_brackets)
# print(p.parse_variables("int a;"))
p.find_func()
print(p.funcs)

import os
import re


class Parser:
    def __init__(self, data=''):
        self.data = data
        self.defines = []
        self.funcs = {}
        self.parse_defines_with_brackets = {}
        self.parse_defines_without_brackets = {}

    def read(self, name):
        os.system(f".\\helpers\\formatter.exe --i --style=file {name}")
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

    def parse_variable_initializations(self, string: str) -> list:
        parsed_variables = []
        keywords = "bool char wchar_t char8_t char16_t char32_t int short long signed unsigned float double const".split()
        if any([string.lstrip().startswith(i) for i in keywords]):
            parsed = []
            found_breaks = list(re.finditer(r"(, [A-z])[A-z]", string))
            first_variable_end = found_breaks[0].span()[0] if len(found_breaks) else len(string)
            first_variable = string[:first_variable_end] + ";"
            parsed.append(first_variable)
            type_hint = first_variable.split()[0]
            for index, semicolon in enumerate(found_breaks):
                if index + 1 < len(found_breaks):
                    print(found_breaks[index + 1])
                    parsed.append(type_hint + " " + string[semicolon.span()[0] + 2:found_breaks[index + 1].span()[0]] + ";")
                else:
                    parsed.append(string[semicolon.span()[0] + 2:len(string) - 1] + ";")

            for variable in parsed:
                for keyword in keywords:
                    variable = variable.replace(keyword, "").lstrip()
                if re.match(r"\w*?;", variable):
                    parsed_variables.append([variable.rstrip(";"), None])
                initialization = re.search(r'[{].*?[}]', variable)
                if initialization:
                    parsed_variables.append([variable[0:initialization.start()], variable[initialization.start() + 1:initialization.end() - 1] if variable[initialization.start() + 1:initialization.end() - 1] else 0])
                if re.search(r"\w*? = .*?", variable):
                    var_info = variable.split(" = ")
                    parsed_variables.append([var_info[0], var_info[1].rstrip(";")])

            return parsed_variables


    def parse_io(self, string: str):
        if 'cout' in string:
            string = string[string[:string.index('c')].count(' '):]
            string = string[:-1].replace(' << ', ' ').replace('cout', '').replace('endl', ' \\n')
            return 'Вывод ' + string[1:].replace('"', '').replace('  ', ' ')

        if 'cin' in string:
            string = string[:-1].split(' >> ')[1:]
            return 'Ввод ' + ' '.join(string)
        return None

    def find_func(self):  # TODO typedef void F(); F  fv;
        keywords = "bool char wchar_t char8_t char16_t char32_t int float double void".split()
        for s in range(len(self.data)):
            if any([self.data[s].startswith(i) for i in keywords]) and '{' in self.data[s] and '}' not in self.data[s]:
                index = s
                name = self.data[s][self.data[s].index(' ') + 1: self.data[s].index('(')]
            elif self.data[s] == '}':
                self.funcs[name] = self.data[index + 1: s]

    def replace_modification(self):
        for i in range(len(self.data)):
            if re.match(r"[A-z 0-9]*?(\+{2}|-{2});", self.data[i]):
                n = self.data[i][:-3].count(' ')
                name = self.data[i][n:-3]
                self.data[i] = n * ' ' + name + ' = ' + name + (' - 1' if '--' in self.data[i] else ' + 1') + ';'
            if re.match(r" *?(\+{2}|-{2})", self.data[i]):
                n = self.data[i][:-1].count(' ')
                name = self.data[i][n + 2:-1]
                self.data[i] = n * ' ' + name + ' = ' + name + (' - 1' if '--' in self.data[i] else ' + 1') + ';'

            init = re.match(r"(?:\w|\s)*? (\+=|-=|\*=|/=|%=) .*", self.data[i])
            if init:
                n = self.data[i].split(' ' + init.group(1) + ' ')[0].count(' ')
                emp = self.data[i][n:-1].split(' ' + init.group(1) + ' ')
                self.data[i] = ' ' * n + emp[0] + ' = ' + emp[0] + ' ' + init.group(1)[0] + ' ' + emp[1] + ';'


p = Parser()
p.read('primer.cpp')
p.prepare()
# print(*p.data, sep='\n')
p.define()
# print(p.parse_defines_with_brackets)
# print(p.parse_defines_without_brackets)
print(p.parse_variable_initializations("double ada{};"))
p.replace_modification()
p.find_func()
# print(*p.funcs['main'], sep='\n')
print(p.parse_io('  cin >> a >> b >> c >> d;'))
print(p.parse_io('  cout << "sum " << summ << endl;'))
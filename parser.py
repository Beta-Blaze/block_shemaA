import os
import re


# noinspection PyMethodMayBeStatic
class Parser:
    def __init__(self, data=''):
        self.data = data
        self.defines = []
        self.funcs = {}
        self.parse_defines_with_brackets = {}
        self.parse_defines_without_brackets = {}

    def read(self, name):
        os.system(f".\\helpers\\formatter.exe --i {name}")
        with open(name) as f:
            self.data = f.readlines()

    def prepare(self):
        emp = []
        rubbish = ['#include', 'namespace']
        for i in self.data:
            if not any([r in i for r in rubbish]):
                emp.append(i.rstrip('\n'))
            if 'define' in i:
                self.defines.append(i.rstrip('\n'))
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
            self.parse_defines_with_brackets[name] = temp

    def parse_variable_initializations(self, string: str) -> list:
        parsed_variables = []
        keywords = "vector bool char wchar_t char8_t char16_t char32_t int short long signed unsigned float double const".split()
        if any([string.lstrip().startswith(i) for i in keywords]):
            parsed = []
            found_breaks = list(re.finditer(r"(, [A-z])", string))
            first_variable_end = found_breaks[0].span()[0] if len(found_breaks) else len(string)
            first_variable = string[:first_variable_end] + ";"
            parsed.append(first_variable)
            type_hint = first_variable.split()[0]
            for index, semicolon in enumerate(found_breaks):
                if index + 1 < len(found_breaks):
                    # print(found_breaks[index + 1])
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
            string = string[:-1].replace(' << ', ' ').replace('cout', '').replace('endl', '')
            return 'Вывод ' + string[1:].replace('  ', ' ')

        if 'cin' in string:
            string = string[:-1].split(' >> ')[1:]
            return 'Ввод ' + ' '.join(string)
        return None

    def find_func(self):  # TODO typedef void F(); F  fv;
        keywords = "vector bool char wchar_t char8_t char16_t char32_t int float double void".split()
        for s in range(len(self.data)):
            if any([self.data[s].startswith(i) for i in keywords]) and '{' in self.data[s] and '}' not in self.data[s]:
                index = s
                name = self.data[s][self.data[s].index(' ') + 1: self.data[s].index('(')]
            elif self.data[s] == '}':
                self.funcs[name] = self.data[index + 1: s]

    def parse_while(self, string):
        string = string.replace('}', '')
        if re.match(r" *?while ", string):
            string = string.replace(' {', '').replace(';', ' ').split(' (')
            return string[1]

    def parse_match_func(self, string: str):
        double = {'pow': '^'}
        single = {'abs': '|'}
        for d in double:
            init = re.finditer(r".*?({}\(.+?,.+?\))".format(d), string)
            for i in init:
                i = i.group(1)
                if i.count('(') != i.count(')'):
                    i = i + ')'
                gr = i
                i = i.replace(f'{d}(', '')[:-1].split(', ')
                string = string.replace(gr, f' {double[d]} '.join(i))
        for s in single:
            init = re.finditer(r".*?({}\(.+?\))".format(s), string)
            for i in init:
                i = i.group(1)
                if i.count('(') != i.count(')'):
                    i = i + ')'
                gr = i
                i = i.replace(f'{s}(', '')[:-1]
                string = string.replace(gr, f'{single[s]} {i} {single[s]}')
        return string.replace(' % ', ' ост ').replace(' == ', ' = ').replace('&', '&#38;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '&#xA;')

    def parse_for(self, string):
        if re.match(r" *?for ", string):
            string = string[:-3].lstrip(' ')[5:]
            if ':' in string:
                return f"{string.split(' ')[1]} ({string.split(' ')[-1]})"
            else:
                string = string.split('; ')
                pars = self.parse_variable_initializations(string[0])
                if not string[2]:
                    value = ''
                elif '--' in string[2]:
                    value = -1
                    perem = pars[0] if pars else [string[2].replace('--', ''), '']
                elif '++' in string[2]:
                    value = 1
                    perem = pars[0] if pars else [string[2].replace('++', ''), '']
                else:
                    s = string[2].split()
                    perem = pars[0] if pars else [s[0], '']
                    if s[1] != '=':
                        value = s[1][0] + s[2]
                        value.replace('+', '')
                    else:
                        value = s[3] + s[4]
                        value.replace('+', '')
                return f'{perem[0]}{"=" if perem[1] else ""}{perem[1]} ({str(value).replace("+", "")}) {string[1]}'
        return None

    def parse_if(self, start_string, strings):
        opened_brackets = 0
        counter = start_string + 1
        data = {True: [], False: [], "Depth": 0}
        if counter >= len(strings):
            return data, counter
        condition = re.search(r"^(?!else)\s*if \((.*?)\) {", strings[start_string])
        if condition:
            opened_brackets += 1
            data['Condition'] = condition.group(1)
            while counter < len(strings):
                if re.match(r"\s*?if \((.*?)\) {", strings[counter]):
                    inner_block = self.parse_if(counter, strings)
                    counter = inner_block[1]
                    data[True].append(inner_block[0])
                    data["Depth"] += inner_block[0]['Depth'] + 1
                    continue
                if '{' in strings[counter]:
                    opened_brackets += 1
                if '}' in strings[counter]:
                    if opened_brackets:
                        opened_brackets -= 1
                    if not opened_brackets:
                        break
                data[True].append(strings[counter])
                data["Depth"] += 1
                counter += 1
        if "else" in strings[counter]:
            false_depth = 0
            opened_brackets -= 1
            else_if_condition = re.search(r"if \((.*?)\) {", strings[counter])
            if not else_if_condition:
                counter += 1
            while counter < len(strings):
                if re.search(r"if \((.*?)\) {", strings[counter]):
                    strings[counter] = strings[counter].replace("} else ", "")
                    inner_block = self.parse_if(counter, strings)
                    counter = inner_block[1]
                    data[False].append(inner_block[0])
                    data["Depth"] += inner_block[0]['Depth'] + 1
                    if else_if_condition:
                        break
                    continue
                if '{' in strings[counter]:
                    opened_brackets += 1
                if '}' in strings[counter]:
                    if opened_brackets:
                        opened_brackets -= 1
                    if not opened_brackets:
                        break
                data[False].append(strings[counter])
                counter += 1
                false_depth += 1
            data["Depth"] = max(data["Depth"], false_depth)
        return data, counter + 1

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


# p = Parser()
# p.read('primer.cpp')
# p.prepare()
# print(*p.data, sep='\n')
# p.define()
# print(p.parse_defines_with_brackets)
# print(p.parse_defines_without_brackets)
# print(p.parse_variable_initializations("double ada{};"))
# p.replace_modification()
# p.find_func()
# print(*p.funcs['main'], sep='\n')
# print(p.parse_io('  cin >> a >> b >> c >> d;'))
# print(p.parse_io('  cout << "sum " << summ << endl;'))
# print(p.parse_for('  for (int i : arr) {'))
# print(p.parse_if(1, p.funcs['main']))

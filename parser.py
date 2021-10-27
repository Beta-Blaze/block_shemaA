import os
import re


# noinspection PyMethodMayBeStatic
class Parser:
    def __init__(self, data: str = ''):
        self.data = data
        self.defines = []
        self.funcs = {}
        self.parse_defines_with_brackets = {}
        self.parse_defines_without_brackets = {}

    def read(self, name: str):
        os.system('.\\helpers\\formatter.exe --i --style="{BasedOnStyle: Google, ColumnLimit: 9999, MaxEmptyLinesToKeep: 0}" ' + name)
        with open(name, encoding='utf-8') as f:
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
        for string in self.defines:
            string: str = string[8:]
            if '(' not in string.split(' ')[0]:
                name = string.split()[0]
                temp = ' '.join(string.split()[1:])
                self.parse_defines_without_brackets[name] = temp.rstrip(';')
                continue
            perem = string[string.index('(') + 1: string.index(')')].split(', ')
            name = string[: string.index('(')]
            string = string[string.index(')') + 2:]
            symb = '+ - * / % ^ & | ~ ! = < >  = < > , ( ) [ ] ;'.split(' ') + [' ']
            ids = []
            for p in perem:
                for b in range(0, len(string) - len(p) + 1):
                    if string[b: b + len(p)] == p:
                        if string[b - 1] in symb:
                            if b + len(p) + 1 in range(0, len(string) - len(p)):
                                if string[b + len(p) + 1]:
                                    ids.append([b, b + len(p), p + '_SUPPER_PUPER_DEF'])
                            else:
                                ids.append([b, b + len(p), p + '_SUPPER_PUPER_DEF'])
            temp = ''
            for _id in sorted(ids, key=lambda x: x[0], reverse=True):
                temp = _id[2] + string[_id[1]:] + temp
                string = string[:_id[0]]
            temp = string + temp
            self.parse_defines_with_brackets[name] = [list(map(lambda x: x + '_SUPPER_PUPER_DEF', perem)), temp]

    def find_define_in_string(self, string: str, name: str, shift=0) -> list:
        res = re.search(r".*?{}\((.+)\)+".format(name), string)
        if res:
            pos = string.index(res.group(1))
            pos = [pos + shift, pos + len(res.group(1)) + shift]
            shift = pos[0]
            return [pos] + self.find_define_in_string(res.group(1), name, shift)
        return []

    def replace_define(self, string: str) -> str:
        for define in self.parse_defines_with_brackets:
            pos = self.find_define_in_string(string, define)
            if pos:
                while pos:
                    pos = pos[-1]
                    perem = string[pos[0]: pos[1]].split(', ')
                    new = self.parse_defines_with_brackets[define][1]
                    for p in range(len(self.parse_defines_with_brackets[define][0])):
                        new = new.replace(self.parse_defines_with_brackets[define][0][p], perem[p])
                    string = string.replace(f'{define}({string[pos[0]: pos[1]]})', new)
                    pos = self.find_define_in_string(string, define)

        symb = '+ - * / % ^ & | ~ ! = < >  = < > , ( ) [ ] ;'.split(' ') + [' ']
        for define in self.parse_defines_without_brackets:
            cord = []
            for s in range(0, len(string) - len(define) + 1):
                if string[s:s + len(define)] == define:
                    if s == 0:
                        if s == len(string) - len(define):
                            cord.append([s, s + len(define)])
                        elif string[s + len(define)] in symb:
                            cord.append([s, s + len(define)])
                    elif s == len(string) - len(define):
                        if string[s - 1] in symb:
                            cord.append([s, s + len(define)])
                    elif string[s + len(define)] in symb and string[s - 1] in symb:
                        cord.append([s, s + len(define)])
            for c in cord[::-1]:
                string = string[:c[0]] + self.parse_defines_without_brackets[define] + string[c[1]:]

        return string

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

    def parse_io(self, string: str) -> str:
        if 'cout' in string:
            string = string[string[:string.index('c')].count(' '):]
            string = string[:-1].replace(' << ', ' ').replace('cout', '').replace('endl', '')
            return 'Вывод ' + string[1:].replace('  ', ' ')

        if 'cin' in string:
            string = string[:-1].split(' >> ')[1:]
            return 'Ввод ' + ' '.join(string)
        return None

    def find_func(self, f_type: str = None):  # TODO typedef void F(); F  fv;
        keywords = "vector bool char wchar_t char8_t char16_t char32_t int float double void".split()
        if f_type:
            keywords.append(f_type)
        for s in range(len(self.data)):
            if any([self.data[s].startswith(i) for i in keywords]) and '{' in self.data[s] and '}' not in self.data[s]:
                index = s
                name = self.data[s][self.data[s].index(' ') + 1: self.data[s].index('(')]
            elif self.data[s] == '}':
                self.funcs[name] = self.data[index + 1: s]

    def parse_while(self, string: str) -> str:
        string = string.replace('}', '')
        if re.match(r" *?while ", string):
            string = string.replace(' {', '').replace(';', ' ').split(' (')
            return string[1]

    def replace_xml_special_symbols(self, string: str) -> str:
        return string.replace(' % ', ' ост ').replace(' == ', ' = ').replace('&', '&#38;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '&#xA;').replace('\\n', ' ')

    def parse_match_funk(self, string: str) -> str:
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
                string = string.replace(gr, ' (' + f' {double[d]} '.join(i) + ') ')
        for s in single:
            init = re.finditer(r".*?({}\(.+?\))".format(s), string)
            for i in init:
                i = i.group(1)
                if i.count('(') != i.count(')'):
                    i = i + ')'
                gr = i
                i = i.replace(f'{s}(', '')[:-1]
                string = string.replace(gr, f'{single[s]} {i} {single[s]}')
        return string

    def final_transformation(self, string: str) -> str:
        string = self.parse_match_funk(string)
        string = self.replace_define(string)

        string = self.replace_xml_special_symbols(string)
        return string

    def parse_for(self, string: str) -> str | None:
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

    def parse_if(self, counter, strings, else_if=False) -> ({True: [], False: [], str: int | str}, int):
        opened_brackets = 0
        state = "NO_CONDITION"
        data = {True: [], False: []}
        while counter < len(strings):
            else_regex = re.search(r"else\s*(if)?", strings[counter])
            if else_regex:
                state = "PARSING_ELSE_BLOCK"
                if else_regex.group(1):
                    state = "PARSING_ELSE_IF_BLOCK"
                else:
                    counter += 1
                    continue
            condition = re.search(r"\s*if \((.*?)\) {", strings[counter])
            if condition:
                if state == "NO_CONDITION":
                    state = "PARSING_IF_BLOCK"
                    data["Condition"] = condition.group(1)
                    opened_brackets += 1
                    counter += 1
                else:
                    cnt = counter + 1
                    if state == "PARSING_IF_BLOCK":
                        cnt -= 1
                    inner_block = self.parse_if(cnt, strings, else_if=(state in ["PARSING_ELSE_BLOCK", "PARSING_ELSE_IF_BLOCK"]))
                    counter = inner_block[1]
                    inner_block[0]["Condition"] = condition.group(1)
                    data[True if state == "PARSING_IF_BLOCK" else False].append(inner_block[0])
                    if state == "PARSING_ELSE_IF_BLOCK":
                        break
                continue
            if else_if:
                state = "PARSING_IF_BLOCK"
                opened_brackets += 1
                else_if = False
            if state != "NO_CONDITION":
                if "{" in strings[counter]:
                    opened_brackets += 1
                if "}" in strings[counter]:
                    opened_brackets -= 1
                if not opened_brackets:
                    counter += 1
                    break
                data[True if state == "PARSING_IF_BLOCK" else False].append(strings[counter])
                counter += 1
            else:
                break
        return data, counter

    def parse_switch(self, counter: int, strings: list[str]) -> tuple[dict[str, dict], int] | None:
        switch_regex = re.match(r"\s*switch \((.*?)\)", strings[counter])
        if switch_regex:
            result = {"condition": switch_regex.group(1),
                      "cases": {}}
            case = True  # False means default branch
            while counter + 1< len(strings):
                counter += 1
                stripped_string = strings[counter].strip()
                case_regex = re.match(r"\s*case (.*?):$", strings[counter])
                if stripped_string == "break;":
                    if case == "default":
                        break
                    continue
                if case == "default" and stripped_string == "}" and len(result["cases"]["default"]):  # Handle unclosed default block
                    number_of_whitespaces = len(strings[counter]) - len(strings[counter].lstrip(' '))
                    number_of_whitespaces_first_str = len(result["cases"]["default"][0]) - len(result["cases"]["default"][0].lstrip(' '))
                    if number_of_whitespaces < number_of_whitespaces_first_str:
                        break
                if case_regex:
                    case = (case_regex.group(1)).lstrip("(").rstrip(")")
                    result["cases"][case] = []
                    continue
                if stripped_string == "default:":
                    case = "default"
                    result["cases"][case] = []
                    continue
                result["cases"][case].append(strings[counter])
            return result, counter + 1
        return None

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

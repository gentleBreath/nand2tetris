import os
import sys
from typing import Optional


class Terminal:  # Terminal: 关键字、符号、整数常量、字符串常量、标识符
    def __init__(self, _type: str, value: str) -> None:
        assert _type in ['keyword', 'symbol', 'integerConstant', 'stringConstant', 'identifier'], '请传入终结符类型'
        self._type = _type
        self.value = value
        self.special_type = {
            '<': "&lt;",
            '>': "&gt;",
            '&': "&amp;",
        }
        if value in self.special_type:
            self.form = '<' + _type + '>' + self.special_type[value] + '</' + _type + '>'
        else:
            self.form = '<' + _type + '>' + value + '</' + _type + '>'


class NonTerminal:
    def __init__(self, value: str, isbeign: bool) -> None:
        assert value in [
            'class', 'classVarDec', 'subroutineDec', 'parameterList', 'subroutineBody', 'varDec',
            'statements', 'whileStatement', 'ifStatement', 'returnStatement', 'letStatement', 'doStatement',
            'expression', 'term', 'expressionList',
        ], '请传入非终结符类型'
        self.value = value
        self.is_terminal = False
        if isbeign:
            self.form = '<' + value + '>'
        else:
            self.form = '</' + value + '>'


class FileReader:
    def __init__(self, filename: str) -> None:
        self.file_object = open(filename, 'r', encoding='utf-8')
        self.buffer = ''
        self.buffer_size = 100
        self.next = 0

    def next_char(self):
        if self.next < len(self.buffer):
            res = self.buffer[self.next]
            self.next += 1
            return res

        self.buffer = self.file_object.read(self.buffer_size)
        self.next = 0

        if self.next < len(self.buffer):
            res = self.buffer[self.next]
            self.next += 1
            return res
        return None

    def lookahead(self, num=1):
        if self.next + num - 1 < len(self.buffer):
            return self.buffer[self.next + num - 1]

        remain = self.buffer[self.next:]
        self.buffer = remain + self.file_object.read(self.buffer_size)
        self.next = 0

        if self.next + num - 1 < len(self.buffer):
            return self.buffer[self.next + num - 1]

        return None

    def close(self):
        if not self.file_object.closed:
            self.file_object.close()


class JackLexer:
    def __init__(self, filename: str) -> None:
        '''
        Jack 词法分析器
        '''
        self.filename = filename
        self.xml_filename = filename[:-5] + '_tokens.xml'
        self.basename = os.path.basename(input)[:-5]  # .jack
        self.tokens = []
        self.codes = []

        self.keywords = [
            'class', 'constructor', 'function', 'method', 'field', 'static',
            'int', 'char', 'boolean', 'void',
            'true', 'false', 'null',
            'this',
            'let', 'var', 'do',
            'if', 'else', 'while', 'return',
        ]
        self.symbols = [
            '{', '}', '[', ']', '(', ')',
            '.', ',', ';',
            '+', '-', '*', '/',
            '&', '|', '~',
            '>', '<', '=',
        ]

        self.reader = FileReader(filename)

    def next_token(self):
        while True:
            char = self.reader.next_char()
            if char is None:
                return None
            # 跳过空白符和换行符
            if char == ' ' or char == '\n' or char == '\t':
                next_char = self.reader.lookahead()
                while next_char == ' ' or next_char == '\n' or next_char == '\t':
                    self.reader.next_char()
                    next_char = self.reader.lookahead()
                continue

            # 跳过单行注释
            if char == '/' and self.reader.lookahead() == '/':
                self.reader.next_char()  # 跳过 //
                next_char = self.reader.lookahead()
                comment = ''
                while next_char != '\n':
                    comment += self.reader.next_char()
                    next_char = self.reader.lookahead()
                self.reader.next_char()  # 跳过\n
                continue

            # 跳过多行注释
            if char == '/' and self.reader.lookahead() == '*':
                self.reader.next_char()  # 跳过/*
                next_char = self.reader.lookahead()
                comment = ''
                while True:
                    if next_char == '*':
                        if self.reader.lookahead(2) == '/':
                            self.reader.next_char()  # 跳过*/
                            self.reader.next_char()  # 跳过*/
                            break
                    comment += self.reader.next_char()
                    next_char = self.reader.lookahead()
                continue

            # keyword/symbol/integerConstant/stringConstant/identifier
            if char.isnumeric():  # 数字
                token = char
                next_char = self.reader.lookahead()
                while next_char.isnumeric():
                    token += self.reader.next_char()
                    next_char = self.reader.lookahead()
                return Terminal('integerConstant', token)

            if char == '"':  # 字符串常量
                token = ''
                next_char = self.reader.lookahead()
                while next_char != '"':
                    token += self.reader.next_char()
                    next_char = self.reader.lookahead()
                self.reader.next_char()  # 跳过结尾双引号
                return Terminal('stringConstant', token)

            if char in self.symbols:
                return Terminal('symbol', char)

            # 分隔符
            token = char
            next_char = self.reader.lookahead()
            while next_char != ' ' and next_char != '\n' and char != '\t' and next_char not in self.symbols:
                token += self.reader.next_char()
                next_char = self.reader.lookahead()

            if token in self.keywords:
                return Terminal('keyword', token)

            return Terminal('identifier', token)

    def tokenize(self):
        token = self.next_token()
        while token is not None:
            self.tokens.append(token)
            token = self.next_token()

    def save_tokens(self):
        with open(self.xml_filename, 'w') as f:
            f.write('<tokens>\n')
            for token in self.tokens:
                f.write(token.form + '\n')
            f.write('</tokens>')

    def close(self):
        if self.reader is not None:
            self.reader.close()


class Symbol:
    def __init__(self, name, _type, kind, index):
        self.name = name
        self._type = _type
        self.kind = kind
        self.index = index


class SymbolTable:
    def __init__(self, prev):
        self.prev = prev
        self.symbols = {}

        self.indexes = {
            "static": 0,
            "field": 0,
            "argument": 0,
            "var": 0
        }


class JackCompiler:
    def __init__(self, source_filenames: list) -> None:
        for _filename in source_filenames:
            assert os.path.basename(_filename)[-4:] == 'jack'
        self.source_filenames = source_filenames

        self.tokens = []
        self.index = -1
        self.current_token = None

        self.output_file_for_xml_obj = None
        self.output_file_obj = None

        # for xml
        self.indent_content = '\t'
        self.indent_level = 0
        self.output_xml = False

        # for vm code
        self.binary_op = {
            '-': 'sub',
            '+': 'add',
            '&': 'and',
            '|': 'or',
            '>': 'gt',
            '<': 'lt',
            '=': 'eq',
            '*': 'mul',
            '/': 'div',
        }
        self.unary_op = {
            '~': 'not',
            '-': 'neg',
        }
        # current scope
        self.scope = SymbolTable(None)
        self.current_class_name = ''
        self.current_function_name = ''
        self.nest_while_statement_level = 0
        self.nest_if_statement_level = 0

        # 标识符属性：名称、数据类型、种类、编号
        # 标准映射：
        # 1. xxx.jack -> xxx.vm
        #
        # 2. 类yyy的子程序xxx -> yyy.xxx
        #
        # 3. k个参数的函数或构造函数 -> k个参数vm函数
        #
        # 4. k个参数的方法 -> k+1个参数vm函数，第一个参数总是指针this
        #
        # 5. 子程序局部变量 -> local段
        #
        # 6. 子程序参数变量 -> argument段
        #
        # 7. xxx.jack文件内的静态变量 -> 对应xxx.vm中的static段
        #
        # 8. 方法或构造函数对this对象字段：通过pointer0将this指针指向的虚拟内存段（this段）映射为存储当前对象的内存段即基地址，
        #    通过this index访问成员，检查index为非负数
        #
        # 9. 数组的成员的访问类似于对象字段：通过pointer1将that指针指向的虚拟内存段（that段）映射为数组的第一个元素的内存段即基地址，
        #    通过that index访问成员，检查index为非负数
        #
        # 10. 子程序调用：调用vm函数前，由调用者压入被调用函数的参数，对于方法，首先压入的参数是操作对象的引用；方法编译为vm函数时，
        #     插入适当的VM代码设置this虚拟段的基地址；构造函数编译时查入VM代码分配内存段并将this指向这个内存段的基地址

    def run(self):
        try:
            for source_filename in self.source_filenames:
                print("===")
                print("当前解析文件为：", source_filename)

                output_filename = source_filename[:-5] + '_my.vm'
                print("输出vm文件名为：", output_filename)
                self.output_file_obj = open(output_filename, 'w')

                if self.output_xml:
                    output_xml_filename = source_filename[:-5] + '_my.xml'
                    print("输出xml文件名为：", output_xml_filename)
                    self.output_file_for_xml_obj = open(output_xml_filename, 'w')

                lexer = JackLexer(source_filename)
                lexer.tokenize()
                self.tokens = lexer.tokens
                self.index = 0
                self.current_token = None
                # 入口
                while self.index < len(self.tokens):
                    self.compile_class()
                print("===")

                if self.output_xml:
                    if self.output_file_for_xml_obj is not None:
                        self.output_file_for_xml_obj.close()
                    self.output_file_for_xml_obj = None

                if self.output_file_obj is not None:
                    self.output_file_obj.close()
                self.output_file_obj = None
        finally:
            if self.output_xml:
                if self.output_file_for_xml_obj is not None:
                    self.output_file_for_xml_obj.close()

            if self.output_file_obj is not None:
                self.output_file_obj.close()

    def next_token(self):
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]

    def advance(self):
        self.current_token = self.tokens[self.index]
        self.index += 1

    def expect(self, _type, values):
        next_token = self.next_token()
        if next_token is None:
            self.error("expect (" + _type + "," + '|'.join(values) + "), but no token left")
        if next_token._type == _type and next_token.value in values:
            self.advance()
            return next_token
        self.error("expect (" + _type + ",[" + '|'.join(
            values) + "]), but got (" + next_token._type + "," + next_token.value + ")")

    def expect_type(self, _type):
        next_token = self.next_token()
        if self.index < len(self.tokens):
            next_token = self.tokens[self.index]
        if next_token is None:
            self.error("expect (" + _type + ", *), but no token left")
        if next_token._type == _type:
            self.advance()
            return next_token
        self.error("expect token type:" + _type + ", but got " + next_token._type)
        return None

    def error(self, msg: str):
        print(msg)
        exit(1)

    def write_to_xml(self, content: str):
        if not self.output_xml:
            return
        indent_level = self.indent_level
        while indent_level > 0:
            self.output_file_for_xml_obj.write(self.indent_content)
            indent_level -= 1
        self.output_file_for_xml_obj.write(content)
        self.output_file_for_xml_obj.write('\n')

    def define(self, name, _type, kind):
        self.scope.symbols[name] = Symbol(name, _type, kind, self.scope.indexes[kind])
        self.scope.indexes[kind] += 1

    def find(self, name) -> Optional[Symbol]:
        scope = self.scope
        while scope is not None:
            if name not in scope.symbols:
                scope = scope.prev
            else:
                return scope.symbols[name]
        return None

    def print_scope(self):
        print('\n----')
        print('|\tname\t|\ttype\t|\tkind\t|\tindex\t|')
        for key in self.scope.symbols:
            symbol = self.scope.symbols[key]
            print('|\t', symbol.name, '\t|\t', symbol._type, '\t|\t', symbol.kind, '\t|\t', symbol.index, '\t|')
        print('----\n')

    def code_write(self, content):
        self.output_file_obj.write(content)
        self.output_file_obj.write('\n')

    def write_push(self, segment, index):
        if segment == 'var':
            segment = 'local'
        elif segment == 'field':
            segment = 'this'
        assert segment in ['constant', 'local', 'argument', 'this', 'that', 'temp', 'pointer', 'static'], print(
            '不支持 %s', segment)
        self.code_write('push' + ' ' + segment + ' ' + str(index))
        return

    def write_pop(self, segment, index):
        if segment == 'var':
            segment = 'local'
        elif segment == 'field':
            segment = 'this'
        assert segment in ['constant', 'local', 'argument', 'this', 'that', 'temp', 'pointer', 'static'], segment
        self.code_write('pop' + ' ' + segment + ' ' + str(index))
        return

    def write_arithmetic(self, command):
        assert command in ('not', 'neg', 'add', 'sub', 'and', 'or', 'eq', 'lt', 'gt', 'mul', 'div')
        if command == 'mul':
            self.code_write('call Math.multiply 2')
        elif command == 'div':
            self.code_write('call Math.divide 2')
        else:
            self.code_write(command)
        return

    def write_label(self, label):
        self.code_write('label' + ' ' + label)
        return

    def write_goto(self, label):
        self.code_write('goto' + ' ' + label)
        return

    def write_if(self, label):
        self.code_write('if-goto' + ' ' + label)
        return

    def write_call(self, name, num_args):
        self.code_write('call' + ' ' + name + ' ' + str(num_args))
        return

    def write_function(self, name, num_args):
        self.code_write('function' + ' ' + name + ' ' + str(num_args))
        return

    def write_return(self):
        self.code_write('return')
        return

    def write_constructor_header(self, num_fields):
        # 分配内存
        self.write_push('constant', num_fields)
        self.write_call('Memory.alloc', 1)
        self.write_pop('pointer', 0)

    def write_method_header(self, num_fields):
        # 设置 this
        self.write_push('argument', 0)
        self.write_pop('pointer', 0)

    # classDec -> 'class' identifier '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        token = self.expect('keyword', ['class'])

        self.write_to_xml(NonTerminal('class', True).form)
        self.indent_level += 1

        self.write_to_xml(token.form)

        token = self.expect_type('identifier')
        self.write_to_xml(token.form)

        # 获取类名称，并初始化一个新的作用域
        current_class_name = token.value
        self.scope = SymbolTable(self.scope)
        self.current_class_name = current_class_name

        token = self.expect('symbol', ['{'])
        self.write_to_xml(token.form)

        num_fields = 0
        while self.next_token() is not None and self.next_token().value in ['static', 'field']:
            num_fields += self.compile_class_var_desc()
        # 打印作用域
        print("类 ", self.current_class_name, " 作用域:")
        self.print_scope()

        while self.next_token() is not None and self.next_token().value in ['constructor', 'function', 'method']:
            # 方法作用域
            self.scope = SymbolTable(self.scope)

            self.compile_subroutine_desc(num_fields)

            # 打印方法作用域内容
            print("方法 ", self.current_function_name, " 作用域:")
            self.print_scope()
            # 复原作用域
            self.scope = self.scope.prev
            self.current_function_name = ''

        token = self.expect('symbol', ['}'])
        self.write_to_xml(token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('class', False).form)

        # 复原作用域
        self.scope = self.scope.prev
        self.current_class_name = ''

    # classVarDec -> ('static'|'filed') type identifier (',' identifier)* ';'
    def compile_class_var_desc(self) -> int:
        num_field = 0
        token = self.expect('keyword', ['static', 'field'])
        kind = token.value

        self.write_to_xml(NonTerminal('classVarDec', True).form)
        self.indent_level += 1

        self.write_to_xml(token.form)

        # type -> 'int' | 'char' | 'boolean' | identifier
        next_token = self.next_token()
        if next_token._type == 'keyword' and next_token.value in ['int', 'char', 'boolean']:
            self.write_to_xml(next_token.form)
            self.advance()
        elif next_token._type == 'identifier':
            self.write_to_xml(next_token.form)
            self.advance()
        else:
            self.error('expect a token("type") but got ' + next_token._type)

        _type = next_token.value

        token = self.expect_type('identifier')
        self.write_to_xml(token.form)

        if kind == 'field':
            num_field += 1

        # 写入符号表
        self.define(token.value, _type, kind)

        next_token = self.next_token()
        while next_token._type == 'symbol' and next_token.value in [',']:
            self.write_to_xml(next_token.form)
            self.advance()

            token = self.expect_type('identifier')
            self.write_to_xml(token.form)

            if kind == 'field':
                num_field += 1
            # 写入符号表
            self.define(token.value, _type, kind)

            next_token = self.next_token()

        token = self.expect('symbol', [';'])
        self.write_to_xml(token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('classVarDec', False).form)
        return num_field

    # subroutineDec -> ('constructor'|'function'|'method') ('void'|type) identifier '(' parameterList ')' subroutineBody
    def compile_subroutine_desc(self, num_fields):
        # 初始化
        self.nest_while_statement_level = 0
        self.nest_if_statement_level = 0

        token = self.expect('keyword', ['constructor', 'function', 'method'])
        function_type = token.value

        self.write_to_xml(NonTerminal('subroutineDec', True).form)
        self.indent_level += 1

        self.write_to_xml(token.form)

        next_token = self.next_token()
        return_type = next_token.value
        if next_token._type == 'keyword' and next_token.value in ['void']:
            self.write_to_xml(next_token.form)
            self.advance()
        elif next_token._type == 'keyword' and next_token.value in ['int', 'char', 'boolean']:
            self.write_to_xml(next_token.form)
            self.advance()
        elif next_token._type == 'identifier':
            self.write_to_xml(next_token.form)
            self.advance()
        else:
            self.error('expect a token(type|"void") but got ' + next_token._type)

        token = self.expect_type('identifier')
        self.write_to_xml(token.form)
        self.current_function_name = token.value

        if function_type in ['method']:
            self.define("this", self.current_class_name, "argument")

        token = self.expect('symbol', ['('])
        self.write_to_xml(token.form)

        self.compile_parameter_list()

        token = self.expect('symbol', [')'])
        self.write_to_xml(token.form)

        self.compile_subroutine_body(return_type, function_type, num_fields)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('subroutineDec', False).form)

    # parameterList -> ((type identifier) (',' type identifier)*)?
    def compile_parameter_list(self) -> int:
        num_args = 0
        parsed = False
        while True:
            next_token = self.next_token()
            if next_token._type == 'keyword' and next_token.value in ['int', 'char', 'boolean']:
                if not parsed:
                    self.write_to_xml(NonTerminal('parameterList', True).form)
                    self.indent_level += 1
                    parsed = True

                self.write_to_xml(next_token.form)
                self.advance()
            elif next_token._type == 'identifier':
                if not parsed:
                    self.write_to_xml(NonTerminal('parameterList', True).form)
                    self.indent_level += 1
                    parsed = True

                self.write_to_xml(next_token.form)
                self.advance()
            elif next_token._type == 'symbol' and next_token.value == ')':
                self.write_to_xml(NonTerminal('parameterList', True).form)
                self.write_to_xml(NonTerminal('parameterList', False).form)
                return num_args
            else:
                self.error("error" + __name__)

            _type = next_token.value

            token = self.expect_type('identifier')
            self.write_to_xml(token.form)

            # 添加到符号表
            self.define(token.value, _type, "argument")
            num_args += 1

            next_token = self.next_token()
            if next_token._type == 'symbol' and next_token.value == ')':
                break
            elif next_token._type == 'symbol' and next_token.value == ',':
                self.write_to_xml(next_token.form)
                self.advance()
            else:
                self.error(
                    'expect a token ("symbol",","|")") but got (' + next_token._type + ' , ' + next_token.value + ' )')
        if parsed:
            self.indent_level -= 1
            self.write_to_xml(NonTerminal('parameterList', False).form)

        return num_args

    # subroutineBody -> '{' varDec* statements '}'
    def compile_subroutine_body(self, return_type, function_type, num_fields):
        num_locals = 0
        token = self.expect('symbol', ['{'])

        self.write_to_xml(NonTerminal('subroutineBody', True).form)
        self.indent_level += 1

        self.write_to_xml(token.form)

        next_token = self.next_token()
        while next_token._type == 'keyword' and next_token.value in ['var']:
            num_locals += self.compile_var_desc()
            next_token = self.next_token()

        self.write_function(self.current_class_name + '.' + self.current_function_name, num_locals)

        if function_type == 'constructor':
            self.write_constructor_header(num_fields)
        elif function_type == 'method':
            self.write_method_header(num_fields)
        else:  # 'function'
            pass
        self.compile_statements(return_type)

        token = self.expect('symbol', ['}'])
        self.write_to_xml(token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('subroutineBody', False).form)
        return num_locals

    # varDec -> 'var' type identifier (',' identifier)* ';'
    def compile_var_desc(self) -> int:
        num_desc = 0
        token = self.expect('keyword', ['var'])

        self.write_to_xml(NonTerminal('varDec', True).form)
        self.indent_level += 1

        self.write_to_xml(token.form)

        # type -> 'int' | 'char' | 'boolean' | identifier
        next_token = self.next_token()
        if next_token._type == 'keyword' and next_token.value in ['int', 'char', 'boolean']:
            self.write_to_xml(next_token.form)
            self.advance()
        elif next_token._type == 'identifier':
            self.write_to_xml(next_token.form)
            self.advance()
        else:
            self.error('expect a token("type") but got ' + next_token._type)
        _type = next_token.value

        token = self.expect_type('identifier')
        self.write_to_xml(token.form)
        num_desc += 1

        self.define(token.value, _type, "var")

        while True:
            next_token = self.next_token()
            if next_token._type == 'symbol' and next_token.value in [',']:
                self.write_to_xml(next_token.form)
                self.advance()

                token = self.expect_type('identifier')
                self.write_to_xml(token.form)
                num_desc += 1

                self.define(token.value, _type, "var")

                continue
            elif next_token._type == 'symbol' and next_token.value in [';']:
                self.write_to_xml(next_token.form)
                self.advance()
                break
            else:
                self.error(
                    'expect a token ("symbol",",";")") but got (' + next_token._type + ' , ' + next_token.value + ' )')

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('varDec', False).form)
        return num_desc

    # statements -> statement*
    def compile_statements(self, return_type='void'):
        next_token = self.next_token()

        self.write_to_xml(NonTerminal('statements', True).form)
        self.indent_level += 1

        while next_token._type == 'keyword' and next_token.value in ['let', 'if', 'while', 'do', 'return']:
            self.compile_statement(return_type)
            next_token = self.next_token()

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('statements', False).form)

    # statement -> letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compile_statement(self, return_type):
        next_token = self.next_token()

        if next_token.value == 'let':
            self.compile_let_statement()
        elif next_token.value == 'if':
            self.compile_if_statement(return_type)
        elif next_token.value == 'while':
            self.compile_while_statement(return_type)
        elif next_token.value == 'do':
            self.compile_do_statement()
        elif next_token.value == 'return':
            self.compile_return_statement(return_type)
        else:
            self.error("expect token ('keyword',') but got ")

    # letStatement -> 'let' identifier ('[' expression ']')? '=' expression ';'
    def compile_let_statement(self):
        next_token = self.expect('keyword', ['let'])

        self.write_to_xml(NonTerminal('letStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        next_token = self.expect_type('identifier')
        self.write_to_xml(next_token.form)

        variable_name = next_token.value

        access_array = False
        while True:
            next_token = self.next_token()
            if next_token._type == 'symbol' and next_token.value == '[':
                self.write_to_xml(next_token.form)
                self.advance()

                self.compile_expression()
                symbol = self.find(variable_name)
                if symbol is None:
                    self.error('non-exist variable')
                self.write_push(symbol.kind, symbol.index)
                self.write_arithmetic("add")
                access_array = True

                next_token = self.expect('symbol', [']'])
                self.write_to_xml(next_token.form)
            elif next_token._type == 'symbol' and next_token.value == '=':
                break
            else:
                self.error(
                    'expect a token ("symbol","["|"=") but got (' + next_token._type + ' , ' + next_token.value + ' )')

        next_token = self.expect('symbol', ['='])
        self.write_to_xml(next_token.form)

        self.compile_expression()

        if access_array:
            self.write_pop('temp', 0)  # 临时存放结果
            self.write_pop('pointer', 1)  # 目标地址存放 that
            self.write_push('temp', 0)  # 结果重新入栈
            self.write_pop('that', 0)  # 放入目标地址
        else:
            symbol = self.find(variable_name)
            if symbol is None:
                self.error('non-exist variable')
            self.write_pop(symbol.kind, symbol.index)

        next_token = self.expect('symbol', [';'])
        self.write_to_xml(next_token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('letStatement', False).form)

    # ifStatement -> 'if' '(' expression ')' '{' statements '}'
    def compile_if_statement(self, return_type):
        current_if_cnt = self.nest_if_statement_level
        self.nest_if_statement_level += 1
        label_for_true = 'IF_TRUE' + str(current_if_cnt)
        label_for_false = 'IF_FALSE' + str(current_if_cnt)
        label_for_end = 'IF_END' + str(current_if_cnt)

        next_token = self.expect('keyword', ['if'])

        self.write_to_xml(NonTerminal('ifStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        next_token = self.expect('symbol', ['('])
        self.write_to_xml(next_token.form)

        self.compile_expression()

        next_token = self.expect('symbol', [')'])
        self.write_to_xml(next_token.form)

        self.write_if(label_for_true)
        self.write_goto(label_for_false)

        self.write_label(label_for_true)
        next_token = self.expect('symbol', ['{'])
        self.write_to_xml(next_token.form)

        self.compile_statements(return_type)

        next_token = self.expect('symbol', ['}'])
        self.write_to_xml(next_token.form)

        exist_else = False

        next_token = self.next_token()
        if next_token._type == 'keyword' and next_token.value == 'else':
            self.write_to_xml(next_token.form)
            self.advance()

            self.write_goto(label_for_end)
            exist_else = True
            self.write_label(label_for_false)

            next_token = self.expect('symbol', ['{'])
            self.write_to_xml(next_token.form)

            self.compile_statements(return_type)

            next_token = self.expect('symbol', ['}'])
            self.write_to_xml(next_token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('ifStatement', False).form)

        if not exist_else:
            self.write_label(label_for_false)
        else:
            self.write_label(label_for_end)

    # whileStatement -> 'while' '(' expression ')' '{' statements '}'
    def compile_while_statement(self, return_type):
        current_while_cnt = self.nest_while_statement_level
        self.nest_while_statement_level += 1
        label_for_exp = 'WHILE_EXP' + str(current_while_cnt)
        label_for_end = 'WHILE_END' + str(current_while_cnt)

        next_token = self.expect('keyword', ['while'])

        self.write_to_xml(NonTerminal('whileStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        self.write_label(label_for_exp)

        token = self.expect('symbol', ['('])
        self.write_to_xml(token.form)

        self.compile_expression()

        token = self.expect('symbol', [')'])
        self.write_to_xml(token.form)

        self.write_arithmetic('not')
        self.write_if(label_for_end)

        token = self.expect('symbol', ['{'])
        self.write_to_xml(token.form)

        self.compile_statements(return_type)

        token = self.expect('symbol', ['}'])
        self.write_to_xml(token.form)

        self.write_goto(label_for_exp)
        self.write_label(label_for_end)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('whileStatement', False).form)

    # doStatement -> 'do' subroutineCall ';'
    def compile_do_statement(self):
        next_token = self.expect('keyword', ['do'])

        self.write_to_xml(NonTerminal('doStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        num_args = 0
        # subroutineCall -> identifier ('.' subroutineName)? '(' expressionList ')'
        token = self.expect_type('identifier')
        self.write_to_xml(token.form)
        called_name = token.value

        next_token = self.next_token()
        if next_token.value == '.':
            self.write_to_xml(next_token.form)
            self.advance()

            next_token = self.expect_type('identifier')
            self.write_to_xml(next_token.form)

            symbol = self.find(called_name)
            if symbol is None:
                called_name += '.' + next_token.value
            else:
                num_args = 1
                self.write_push(symbol.kind, symbol.index)
                called_name = symbol._type + '.' + next_token.value
        else:
            self.write_push('pointer', 0)
            num_args = 1
            called_name = self.current_class_name + '.' + called_name

        next_token = self.expect('symbol', '(')
        self.write_to_xml(next_token.form)

        num_args += self.compile_expression_list()

        next_token = self.expect('symbol', ')')
        self.write_to_xml(next_token.form)

        next_token = self.expect('symbol', [';'])
        self.write_to_xml(next_token.form)

        self.write_call(called_name, num_args)

        # 丢弃结果
        self.write_pop('temp', 0)
        self.indent_level -= 1
        self.write_to_xml(NonTerminal('doStatement', False).form)

    # returnStatement -> 'return' expression? ';'
    def compile_return_statement(self, return_type):
        next_token = self.expect('keyword', ['return'])

        self.write_to_xml(NonTerminal('returnStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        while True:
            next_token = self.next_token()
            if next_token._type == 'symbol' and next_token.value == ';':
                if return_type == 'void':
                    self.write_push('constant', 0)
                break
            elif next_token._type == 'keyword' and next_token.value == 'this':
                self.write_push('pointer', 0)
                self.advance()
            else:
                self.compile_expression()

        next_token = self.expect('symbol', [';'])
        self.write_to_xml(next_token.form)

        self.write_return()

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('returnStatement', False).form)

    # expression -> term ( op term )*
    def compile_expression(self):
        parsed = False
        next_token = self.next_token()
        if next_token._type in ['integerConstant', 'stringConstant'] or (
                next_token._type == 'keyword' and next_token.value in ['true', 'false', 'null', 'this']) or (
                next_token._type == 'identifier') or (
                next_token._type == 'symbol' and next_token.value in ['(', '~', '-']):
            if not parsed:
                self.write_to_xml(NonTerminal('expression', True).form)
                self.indent_level += 1
                parsed = True
            self.compile_term()

        # op ->  '+' | '-' | '*' | '/' | '&' | '|' | '>' | '<' | '='
        next_token = self.next_token()
        while next_token._type == 'symbol' and next_token.value in ['+', '-', '*', '/', '&', '|', '>', '<', '=']:
            self.write_to_xml(next_token.form)
            self.advance()

            op = next_token.value

            self.compile_term()
            next_token = self.next_token()

            self.write_arithmetic(self.binary_op[op])

        if parsed:
            self.indent_level -= 1
            self.write_to_xml(NonTerminal('expression', False).form)

    # term -> integerConstant | stringConstant | keywordConstant |
    #         identifier | identifier '['expression ']' | subroutineCall |
    #         '(' expression ')' | unaryOp term
    def compile_term(self):
        next_token = self.next_token()
        if next_token._type in ['integerConstant', 'stringConstant']:
            self.write_to_xml(NonTerminal('term', True).form)
            self.indent_level += 1

            self.write_to_xml(next_token.form)
            self.advance()

            if next_token._type == 'integerConstant':
                self.write_push("constant", next_token.value)
            else:
                self.write_push('constant', len(next_token.value))
                self.code_write('call String.new 1')
                for char in next_token.value:
                    self.write_push('constant', ord(char))
                    self.code_write('call String.appendChar 2')

        elif next_token._type == 'keyword' and next_token.value in ['true', 'false', 'null',
                                                                    'this']:  # keywordConstant -> 'true' | 'false' | 'null' | 'this'
            self.write_to_xml(NonTerminal('term', True).form)
            self.indent_level += 1

            self.write_to_xml(next_token.form)
            self.advance()

            if next_token.value == 'true':
                self.write_push("constant", 0)
                self.write_arithmetic("not")
            elif next_token.value in ('false', 'null'):
                self.write_push("constant", 0)
            else:  # next_token.value in ('this')
                self.write_push("pointer", 0)

        elif next_token._type == 'identifier':
            self.write_to_xml(NonTerminal('term', True).form)
            self.indent_level += 1

            self.write_to_xml(next_token.form)
            self.advance()

            variable_name = next_token.value

            next_token = self.next_token()
            if next_token._type == 'symbol':
                access_array = False
                if next_token.value == '[':  # identifier '['expression ']'
                    self.write_to_xml(next_token.form)
                    self.advance()

                    access_array = True

                    self.compile_expression()
                    symbol = self.find(variable_name)
                    if symbol is not None:
                        self.write_push(symbol.kind, symbol.index)
                    self.write_arithmetic('add')

                    token = self.expect('symbol', ']')
                    self.write_to_xml(token.form)

                    self.write_pop('pointer', 1)
                    self.write_push('that', 0)
                elif next_token.value == '.':  # identifier '.' subroutineName '(' expressionList ')'
                    self.write_to_xml(next_token.form)
                    self.advance()

                    next_token = self.expect_type('identifier')
                    self.write_to_xml(next_token.form)

                    subroutine_name = next_token.value

                    next_token = self.expect('symbol', '(')
                    self.write_to_xml(next_token.form)

                    num_args = self.compile_expression_list()

                    next_token = self.expect('symbol', ')')
                    self.write_to_xml(next_token.form)

                    symbol = self.find(variable_name)
                    if symbol is not None:
                        self.write_push(symbol.kind, symbol.index)
                        variable_name = symbol._type
                        num_args += 1
                    variable_name += '.' + subroutine_name

                    self.write_call(variable_name, num_args)
                elif next_token.value == '(':  # identifier                    '(' expressionList ')'
                    self.write_to_xml(next_token.form)
                    self.advance()

                    num_args = self.compile_expression_list()

                    next_token = self.expect('symbol', ')')
                    self.write_to_xml(next_token.form)

                    self.write_call(variable_name, num_args)
                else:
                    symbol = self.find(variable_name)
                    if symbol is not None:
                        self.write_push(symbol.kind, symbol.index)

        elif next_token._type == 'symbol' and next_token.value == '(':
            self.write_to_xml(NonTerminal('term', True).form)
            self.indent_level += 1

            self.write_to_xml(next_token.form)
            self.advance()

            self.compile_expression()

            next_token = self.expect('symbol', [')'])
            self.write_to_xml(next_token.form)
        elif next_token._type == 'symbol' and next_token.value in ['~', '-']:  # unaryOp -> '~' |  '-'
            self.write_to_xml(NonTerminal('term', True).form)
            self.indent_level += 1

            op = next_token.value

            self.write_to_xml(next_token.form)
            self.advance()

            self.compile_term()

            self.write_arithmetic(self.unary_op[op])

        else:
            self.error("expect a term production but got ...")

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('term', False).form)

    # expressionList -> (expression (',' expression)*)?
    def compile_expression_list(self) -> int:
        num_args = 0
        parsed = False
        next_token = self.next_token()
        if next_token._type in ['integerConstant', 'stringConstant'] or (
                next_token._type == 'keyword' and next_token.value in ['true', 'false', 'null', 'this']) or (
                next_token._type == 'identifier') or (
                next_token._type == 'symbol' and next_token.value in ['(', '~', '-']):
            if not parsed:
                self.write_to_xml(NonTerminal('expressionList', True).form)
                self.indent_level += 1
                parsed = True

            self.compile_expression()
            num_args += 1

            # op ->  '+' | '-' | '*' | '/' | '&' | '|' | '>' | '<' | '='
            next_token = self.next_token()
            while True:
                if next_token._type == 'symbol' and next_token.value in [',']:
                    self.write_to_xml(next_token.form)
                    self.advance()

                    self.compile_expression()
                    num_args += 1

                elif next_token._type == 'symbol' and next_token.value == ')':
                    break
                next_token = self.next_token()
            if parsed:
                self.indent_level -= 1
                self.write_to_xml(NonTerminal('expressionList', False).form)
        elif next_token._type == 'symbol' and next_token.value == ')':
            self.write_to_xml(NonTerminal('expressionList', True).form)
            self.write_to_xml(NonTerminal('expressionList', False).form)

        else:
            self.error("expect a expression_list production but got ...")

        return num_args


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("请输入要解析的文件名或目录")
        exit(1)
    print('当前工作目录为：', os.getcwd())

    input = os.getcwd() + '/' + sys.argv[1]
    source_filenames = []
    # output_filename = ''
    # 判断是否是目录，获取到所有后缀名为.jack的文件
    if os.path.isdir(input):
        if input.endswith('/'):
            input = input[:-1]
        for filename in os.listdir(input):
            if os.path.isfile(input + '/' + filename) and filename[-4:] == 'jack':
                source_filenames.append(input + '/' + filename)
        if len(source_filenames) == 0:
            print('请输入正确的.jack文件名或目录')
            exit(1)
        # output_filename = input + '/' + os.path.basename(input) + ".vm"
    elif os.path.isfile(input) and input[-4:] == 'jack':
        source_filenames.append(input)
        # output_filename = os.path.dirname(input) + '/' + os.path.basename(input)[:-4] + 'vm'
    else:
        print('请输入正确的.jack文件名或目录')
        exit(1)
    # print("输出文件名为：", output_filename)

    compiler = JackCompiler(source_filenames)
    compiler.run()

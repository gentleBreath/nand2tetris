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


class JackCompiler:
    def __init__(self, source_filenames: list) -> None:
        for _filename in source_filenames:
            assert os.path.basename(_filename)[-4:] == 'jack'
        self.source_filenames = source_filenames

        self.tokens = []
        self.index = -1
        self.current_token = None

        self.output_file_obj = None

        self.indent_content = '\t'
        self.indent_level = 0

    def run(self):
        try:
            for _filename in self.source_filenames:
                print("===")
                print("当前解析文件为：", _filename)

                output_filename = _filename[:-4]+'vm'
                print("输出文件名为：", output_filename)

                self.output_file_obj = open(output_filename, 'w')
                lexer = JackLexer(_filename)
                lexer.tokenize()
                self.tokens = lexer.tokens
                self.index = 0
                self.current_token = None
                # 入口
                while self.index < len(self.tokens):
                    self.compile_class()
                print("===")

                if self.output_file_obj is not None:
                    self.output_file_obj.close()
                self.output_file_obj = None
        finally:
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
        indent_level = self.indent_level
        while indent_level > 0:
            self.output_file_obj.write(self.indent_content)
            indent_level -= 1
        self.output_file_obj.write(content)
        self.output_file_obj.write('\n')

    # classDec -> 'class' identifier '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        token = self.expect('keyword', ['class'])

        self.write_to_xml(NonTerminal('class', True).form)
        self.indent_level += 1

        self.write_to_xml(token.form)

        token = self.expect_type('identifier')
        self.write_to_xml(token.form)

        token = self.expect('symbol', ['{'])
        self.write_to_xml(token.form)

        while self.next_token() is not None and self.next_token().value in ['static', 'field']:
            self.compile_class_var_desc()

        while self.next_token() is not None and self.next_token().value in ['constructor', 'function', 'method']:
            self.compile_subroutine_desc()

        token = self.expect('symbol', ['}'])
        self.write_to_xml(token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('class', False).form)

    # classVarDec -> ('static'|'filed') type identifier (',' identifier)* ';'
    def compile_class_var_desc(self):
        token = self.expect('keyword', ['static', 'field'])

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

        token = self.expect_type('identifier')
        self.write_to_xml(token.form)

        next_token = self.next_token()
        while next_token._type == 'symbol' and next_token.value in [',']:
            self.write_to_xml(next_token.form)
            self.advance()

            token = self.expect_type('identifier')
            self.write_to_xml(token.form)

            next_token = self.next_token()

        token = self.expect('symbol', [';'])
        self.write_to_xml(token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('classVarDec', False).form)

    # subroutineDec -> ('constructor'|'function'|'method') ('void'|type) identifier '(' parameterList ')' subroutineBody
    def compile_subroutine_desc(self):
        token = self.expect('keyword', ['constructor', 'function', 'method'])

        self.write_to_xml(NonTerminal('subroutineDec', True).form)
        self.indent_level += 1

        self.write_to_xml(token.form)

        next_token = self.next_token()
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

        token = self.expect('symbol', ['('])
        self.write_to_xml(token.form)

        self.compile_parameter_list()

        token = self.expect('symbol', [')'])
        self.write_to_xml(token.form)

        self.compile_subroutine_body()

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('subroutineDec', False).form)

    # parameterList -> ((type identifier) (',' type identifier)*)?
    def compile_parameter_list(self):
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
                return
            else:
                self.error("error" + __name__)

            token = self.expect_type('identifier')
            self.write_to_xml(token.form)

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

    # subroutineBody -> '{' varDec* statements '}'
    def compile_subroutine_body(self):
        token = self.expect('symbol', ['{'])

        self.write_to_xml(NonTerminal('subroutineBody', True).form)
        self.indent_level += 1

        self.write_to_xml(token.form)

        next_token = self.next_token()
        while next_token._type == 'keyword' and next_token.value in ['var']:
            self.compile_var_desc()
            next_token = self.next_token()

        self.compile_statements()

        token = self.expect('symbol', ['}'])
        self.write_to_xml(token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('subroutineBody', False).form)

    # varDec -> 'var' type identifier (',' identifier)* ';'
    def compile_var_desc(self):
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

        token = self.expect_type('identifier')
        self.write_to_xml(token.form)

        while True:
            next_token = self.next_token()
            if next_token._type == 'symbol' and next_token.value in [',']:
                self.write_to_xml(next_token.form)
                self.advance()

                token = self.expect_type('identifier')
                self.write_to_xml(token.form)
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

    # statements -> statement*
    def compile_statements(self):
        next_token = self.next_token()

        self.write_to_xml(NonTerminal('statements', True).form)
        self.indent_level += 1

        while next_token._type == 'keyword' and next_token.value in ['let', 'if', 'while', 'do', 'return']:
            self.compile_statement()
            next_token = self.next_token()

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('statements', False).form)

    # statement -> letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compile_statement(self):
        next_token = self.next_token()

        if next_token.value == 'let':
            self.compile_let_statement()
        elif next_token.value == 'if':
            self.compile_if_statement()
        elif next_token.value == 'while':
            self.compile_while_statement()
        elif next_token.value == 'do':
            self.compile_do_statement()
        elif next_token.value == 'return':
            self.compile_return_statement()
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

        while True:
            next_token = self.next_token()
            if next_token._type == 'symbol' and next_token.value == '[':
                self.write_to_xml(next_token.form)
                self.advance()

                self.compile_expression()

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

        next_token = self.expect('symbol', [';'])
        self.write_to_xml(next_token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('letStatement', False).form)

    # ifStatement -> 'if' '(' expression ')' '{' statements '}'
    def compile_if_statement(self):
        next_token = self.expect('keyword', ['if'])

        self.write_to_xml(NonTerminal('ifStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        next_token = self.expect('symbol', ['('])
        self.write_to_xml(next_token.form)

        self.compile_expression()

        next_token = self.expect('symbol', [')'])
        self.write_to_xml(next_token.form)

        next_token = self.expect('symbol', ['{'])
        self.write_to_xml(next_token.form)

        self.compile_statements()

        next_token = self.expect('symbol', ['}'])
        self.write_to_xml(next_token.form)

        next_token = self.next_token()
        if next_token._type == 'keyword' and next_token.value == 'else':
            self.write_to_xml(next_token.form)
            self.advance()

            next_token = self.expect('symbol', ['{'])
            self.write_to_xml(next_token.form)

            self.compile_statements()

            next_token = self.expect('symbol', ['}'])
            self.write_to_xml(next_token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('ifStatement', False).form)

    # whileStatement -> 'while' '(' expression ')' '{' statements '}'
    def compile_while_statement(self):
        next_token = self.expect('keyword', ['while'])

        self.write_to_xml(NonTerminal('whileStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        token = self.expect('symbol', ['('])
        self.write_to_xml(token.form)

        self.compile_expression()

        token = self.expect('symbol', [')'])
        self.write_to_xml(token.form)

        token = self.expect('symbol', ['{'])
        self.write_to_xml(token.form)

        self.compile_statements()

        token = self.expect('symbol', ['}'])
        self.write_to_xml(token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('whileStatement', False).form)

    # doStatement -> 'do' subroutineCall ';'
    def compile_do_statement(self):
        next_token = self.expect('keyword', ['do'])

        self.write_to_xml(NonTerminal('doStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        # subroutineCall -> identifier ('.' subroutineName)? '(' expressionList ')'
        token = self.expect_type('identifier')
        self.write_to_xml(token.form)

        next_token = self.next_token()
        if next_token.value == '.':
            self.write_to_xml(next_token.form)
            self.advance()

            next_token = self.expect_type('identifier')
            self.write_to_xml(next_token.form)

        next_token = self.expect('symbol', '(')
        self.write_to_xml(next_token.form)

        self.compile_expression_list()

        next_token = self.expect('symbol', ')')
        self.write_to_xml(next_token.form)

        next_token = self.expect('symbol', [';'])
        self.write_to_xml(next_token.form)

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('doStatement', False).form)

    # returnStatement -> 'return' expression? ';'
    def compile_return_statement(self):
        next_token = self.expect('keyword', ['return'])

        self.write_to_xml(NonTerminal('returnStatement', True).form)
        self.indent_level += 1

        self.write_to_xml(next_token.form)

        next_token = self.next_token()
        while True:
            if next_token._type == 'symbol' and next_token.value == ';':
                break
            else:
                self.compile_expression()
                next_token = self.next_token()

        next_token = self.expect('symbol', [';'])
        self.write_to_xml(next_token.form)

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

            self.compile_term()
            next_token = self.next_token()

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

        elif next_token._type == 'keyword' and next_token.value in ['true', 'false', 'null',
                                                                    'this']:  # keywordConstant -> 'true' | 'false' | 'null' | 'this'
            self.write_to_xml(NonTerminal('term', True).form)
            self.indent_level += 1

            self.write_to_xml(next_token.form)
            self.advance()
            pass
        elif next_token._type == 'identifier':
            self.write_to_xml(NonTerminal('term', True).form)
            self.indent_level += 1

            self.write_to_xml(next_token.form)
            self.advance()

            next_token = self.next_token()
            if next_token._type == 'symbol':
                if next_token.value == '[':  # identifier '['expression ']'
                    self.write_to_xml(next_token.form)
                    self.advance()

                    self.compile_expression()

                    token = self.expect('symbol', ']')
                    self.write_to_xml(token.form)
                elif next_token.value == '.':  # identifier '.' subroutineName '(' expressionList ')'
                    self.write_to_xml(next_token.form)
                    self.advance()

                    next_token = self.expect_type('identifier')
                    self.write_to_xml(next_token.form)

                    next_token = self.expect('symbol', '(')
                    self.write_to_xml(next_token.form)

                    self.compile_expression_list()

                    next_token = self.expect('symbol', ')')
                    self.write_to_xml(next_token.form)
                elif next_token.value == '(':  # identifier                    '(' expressionList ')'
                    self.write_to_xml(next_token.form)
                    self.advance()

                    self.compile_expression_list()

                    next_token = self.expect('symbol', ')')
                    self.write_to_xml(next_token.form)

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

            self.write_to_xml(next_token.form)
            self.advance()

            self.compile_term()
        else:
            self.error("expect a term production but got ...")

        self.indent_level -= 1
        self.write_to_xml(NonTerminal('term', False).form)

    # expressionList -> (expression (',' expression)*)?
    def compile_expression_list(self):
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

            # op ->  '+' | '-' | '*' | '/' | '&' | '|' | '>' | '<' | '='
            next_token = self.next_token()
            while True:
                if next_token._type == 'symbol' and next_token.value in [',']:
                    self.write_to_xml(next_token.form)
                    self.advance()

                    self.compile_expression()

                elif next_token._type == 'symbol' and next_token.value == ')':
                    break
                next_token = self.next_token()
            if parsed:
                self.indent_level -= 1
                self.write_to_xml(NonTerminal('expressionList', False).form)
        elif next_token._type == 'symbol' and next_token.value == ')':
            self.write_to_xml(NonTerminal('expressionList', True).form)
            self.write_to_xml(NonTerminal('expressionList', False).form)

            return
        else:
            self.error("expect a expression_list production but got ...")


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

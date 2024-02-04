from enum import Enum
import sys
import os


class SymbolTable:
    def  __init__(self) -> None:
        self.table={
            "SP":0,
            "LCL":1,
            "ARG":2,
            "THIS":3,
            "THAT":4,
            
            "R0":0,
            "R1":1,
            "R2":2,
            "R3":3,
            "R4":4,
            "R5":5,
            "R6":6,
            "R7":7,
            "R8":8,
            "R9":9,
            "R10":10,
            "R11":11,
            "R12":12,
            "R13":13,
            "R14":14,
            "R15":15,

            "SCREEN":16384,
            "KBD":24576,
        }
        self.alloc_address=16
    def addLabel(self,symbol:str,address:int):
        self.table[symbol]=address
    def addEntry(self,symbol:str)->int:
        self.table[symbol]=self.alloc_address
        self.alloc_address+=1
        return self.alloc_address - 1 
    def contains(self,symbol:str):
        return self.table.get(symbol)
    def getAddress(self,symbol:str)->int:
        return self.table.get(symbol)

class CodeTranslator:
    '''
    Translate Hash assembler code to machine code
    '''
    def __init__(self,symbol_table:SymbolTable) -> None:
        self.dest_map={
            'NULL':'000',
            'M':'001',
            'D':'010',
            'MD':'011',
            'A':'100',
            'AM':'101',
            'AD':'110',
            'AMD':'111',
        }
        self.jump_map={
            'NULL':'000',
            'JGT':'001',
            'JEQ':'010',
            'JGE':'011',
            'JLT':'100',
            'JNE':'101',
            'JLE':'110',
            'JMP':'111',
        }
        self.comp_map={
            '0':'0101010',
            '1':'0111111',
            '-1':'0111010',

            'D':'0001100',
            'A':'0110000',
            'M':'1110000',

            '!D':'0001101',
            '!A':'0110001',
            '!M':'1110001',

            '-D':'0001111',
            '-A':'0110011',
            '-M':'1110011',

            'D+1':'0011111',
            'A+1':'0110111',
            'M+1':'1110111',

            'D-1':'0001110',
            'A-1':'0110010',
            'M-1':'1110010',
        
            'D+A':'0000010',
            'D+M':'1000010',

            'D-A':'0010011',
            'D-M':'1010011',

            'A-D':'0000111',
            'M-D':'1000111',

            'D&A':'0000000',
            'D&M':'1000000',

            'D|A':'0010101',
            'D|M':'1010101',
        }
        self.symbol_table=symbol_table
    def dest(self,dest:str)->str:
        return self.dest_map[dest]
    def comp(self,comp:str)->str:
        return self.comp_map[comp]
    def jump(self,jump:str)->str:
        return self.jump_map[jump]
    def translate(self,code:str)->str:
        if code.startswith('('): # L Command
            return
        elif code.startswith('@'): # A Command
            print('ACommand:',code)
            code=code[1:].strip()
            if code.isdecimal():
                binary=bin(int(code))[2:]
                binary="0"*(16-len(binary))+binary
                print('->Machine Code:',binary)
                return binary
            elif self.symbol_table.contains(code) == None:
                print('add ' + code + ' to symbol table')
                address =self.symbol_table.addEntry(code)
                binary=bin(int(address))[2:]
                binary="0"*(16-len(binary))+binary
                print('->Machine Code:',binary)
                return binary
            else:
                assert self.symbol_table.contains(code) != None
                address = self.symbol_table.getAddress(code)
                binary=bin(int(address))[2:]
                binary = "0"*(16-len(binary))+binary
                print('->Machine Code:',binary)
                return binary
        else: # C Command
            print('CCommand:',code)
            equal_loc = code.find('=')
            semicolon_loc = code.find(';')
            dest=''
            comp=''
            jump=''
            if equal_loc == -1:
                dest='NULL'
            if semicolon_loc == -1:
                jump='NULL'
                semicolon_loc=len(code)
            if len(dest) == 0:
                dest = code[:equal_loc]
            if len(jump) == 0:
                jump = code[semicolon_loc+1:]
            comp = code[equal_loc+1:semicolon_loc]
            binary = '111'+self.comp_map[comp]+self.dest_map[dest]+self.jump_map[jump]
            print('->Machine Code:',binary)
            return binary


class Parser:
    '''
    A simple parser for Hach assembler
    '''
    def __init__(self,file_path:str) -> None:
        self.file_name=os.path.basename(file_path)
        suffix=self.file_name[-3:]
        assert suffix=='asm','please input an file named like Xxx.asm'

        self.assembler_codes=[]
        self.cursor=-1
        with open(file_path,'r') as f:
            for assembler_code in f:
                # 去掉首尾空格
                assembler_code=assembler_code.strip()
                # 去掉空行
                if assembler_code.strip() == '':
                    continue
                # 去掉注释
                if assembler_code.startswith('/'):
                    continue
                # 去掉行注释
                if assembler_code.find('/') !=-1:
                    assembler_code=assembler_code[:assembler_code.find('/')]
                self.assembler_codes.append(assembler_code.strip())    
        self.symbol_table=SymbolTable()
        
    def hasMoreCommands(self)->bool:
        return self.cursor < len(self.assembler_codes)
    
    def advance(self)->str:
        self.cursor+=1
        if self.hasMoreCommands():
            return self.assembler_codes[self.cursor]
        return ''
    def pre_process(self):
        filted_codes=[]
        cursor = -1
        for code in self.assembler_codes:
            if code.startswith('('): # L Command
                self.symbol_table.addLabel(code[1:-1],cursor+1)
            else:
                filted_codes.append(code)
                cursor+=1
        self.assembler_codes=filted_codes
class Assembler:
    def __init__(self,file_path:str) -> None:
        '''
        A simple assembler for Hack machine
        '''
        self.parser = Parser(file_path)
        self.machine_codes=[]
        self.save_file_path = file_path[:-4]+'.hack'        
    def run(self):
        translator=CodeTranslator(self.parser.symbol_table)
        self.parser.pre_process()
        while True:
            code = self.parser.advance()
            print(code)
            if code == '':
                break
            machine_code = translator.translate(code)
            assert machine_code  !=None,'翻译错误'+code
            self.machine_codes.append(machine_code)
    def save(self):
        with open(self.save_file_path,'w') as f:
            for line in self.machine_codes:
                f.write(line)
                f.write('\n')
        
if __name__== '__main__':
    file_path = sys.argv[1]
    assembler = Assembler(file_path)
    assembler.run()
    # print(assembler.machine_codes)
    assembler.save()
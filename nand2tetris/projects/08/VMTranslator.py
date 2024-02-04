import sys
import os


class CodeWriter:
    def __init__(self,filename:str,write_init_code:bool) -> None:
        self.arith_dict = {
            'not':'!',
            'neg':'-',
            'add':'+',
            'sub':'-',
            'and':'&',
            'or':'|',
            'eq':'JNE',
            'lt':'JGE',
            'gt':'JLE',
        }
        self.segment_dict = {
            'local':"LCL",
            'argument':'ARG',
            'this':'THIS',
            'that':'THAT',
            'temp':'5',
            'pointer':'3',
        }
        self.output_filename=filename
        self.base_filename=os.path.basename(filename)[:-4] # .asm
        self.asm_codes=[]
        self.symbol_index=0
        self.ret_index=0
        self.write_init_code=write_init_code
        self.current_source_filename=''
        pass
    def set_current_vm_source(self,source_filename:str):
        self.current_source_filename=source_filename
    def function_symbol(self,function_name:str):
        return self.base_filename+'$func$'+function_name
    def function_return_address_symbol(self,function_name:str):
        return self.base_filename+'$func$'+function_name+'_return_address'
    def label_symbol(self,label:str):
        return self.base_filename+'$label$'+label
    def static_variable_name(self,index):
        # 每个vm文件下的静态变量应当是不与其他vm文件下的发生冲突，故引入当前文件名
        assert self.current_source_filename !=''
        return self.base_filename+'$'+self.current_source_filename+'$static$'+index
    def writeArithmetic(self,command:str):
        assert command in ['not','neg','add','sub','and','or','eq','lt','gt'],'不支持的指令'
        res = []
        if command in ['not','neg']: # 单参数
            res.extend([
                '@SP',
                'A=M-1',
                'M='+self.arith_dict[command]+'M'
            ])
        elif command in ['add','sub','and','or']: # 双参数
            res.extend([
                '@SP',
                'AM=M-1', # 同时完成SP=SP-1并存入SP
                'D=M', # 取得第二个参数 D = M[SP-1]
                'A=A-1', 
                'M=M'+self.arith_dict[command]+'D' # M[SP-2]=M[SP-2] op D
            ])
        else: # command in ['eq','gt','lt']
            # 创建一个符号
            symbol = self.base_filename[:-4]+'_'+command+'_'+str(self.symbol_index)
            self.symbol_index+=1
            res.extend([
                '@SP',
                'AM=M-1', # 同时完成SP=SP-1
                'D=M',# 获取第二个操作数
                'A=A-1',
                'D=M-D', # D = M[SP-2] - M[SP-1]
                'M=0', # M[SP-2] = False
                '@'+symbol,
                'D;'+self.arith_dict[command],
                '@SP',
                'A=M-1',
                'M=-1', # M[SP-2] = True
                '('+symbol+')',
            ])
        print(res)
        self.asm_codes.append(res)
    def writePush(self,segment:str,index:int):
            assert segment in ['constant','local','argument','this','that','temp','pointer','static'],'不支持的段名'
            res=[]
            # 使用D寄存器存放将要压栈的数据
            if segment == 'constant': # 立即数
                res.extend([
                    '@'+index,
                    'D=A',  
                ])
            elif segment in ['local','argument','this','that']: # 变址寻址——从寄存器指向内存中获取基址，加上索引获取数据所在内存地址，然后获取值
                res.extend([
                    '@'+index,
                    'D=A',
                    '@'+self.segment_dict[segment],
                    'A=M+D',
                    'D=M'
                ])
            elif segment in ['temp','pointer']: # 变址寻址——从寄存器中获取基址，加上索引获取数据所在地址，然后获取值
                res.extend([
                    '@'+index,
                    'D=A',
                    '@'+self.segment_dict[segment],
                    'A=A+D',
                    'D=M'
                ])
            else:  #segment == 'static' # 静态变量，文件名和静态变量数量作为静态变量名，获取其值
                res.extend([
                    '@'+self.static_variable_name(index),
                    'D=M'
                ])
            # 将数据压入栈，并增加栈指针SP
            res.extend([
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M+1'
            ])
            print(res)
            self.asm_codes.append(res)

    def writePop(self,segment:str,index:int):
            assert segment in ['local','argument','this','that','temp','pointer','static'],'不支持的段名'
            res=[]
            if segment in ['local','argument','this','that']: # 变址寻址——从寄存器指向内存中获取基址，加上索引获取数据所在内存地址，然后获取值
                res.extend([
                    '@'+index,
                    'D=A',
                    '@'+self.segment_dict[segment],
                    'D=M+D',
                ])
            elif segment in ['temp','pointer']: # 变址寻址——从寄存器中获取基址，加上索引获取数据所在地址，然后获取值
                res.extend([
                    '@'+index,
                    'D=A',
                    '@'+self.segment_dict[segment],
                    'D=A+D',
                    
                ])
            else:  #segment == 'static' # 静态变量，文件名和静态变量数量作为静态变量名，获取其值
                res.extend([
                    '@'+self.static_variable_name(index),
                    'D=A',
                ])
            res.extend([
                # 使用R15存放目标地址
                '@R15',
                'M=D',
                # 获取栈数据
                '@SP',
                'AM=M-1',# A=M[SP]-1
                'D=M', # D=M[M[SP]-1]]
                # 存放值
                '@R15',
                'A=M',
                'M=D'
            ])
            print(res)
            self.asm_codes.append(res)
    def InitCode(self)->list:
        res=[]
        # 初始化寄存器 SP
        res.extend([
            # SP = 256
            '@256',
            'D=A',
            '@SP',
            'M=D',
        ])
            
        # 初始化寄存器 LCL，ARG,THIS,THAT
        for k,v in zip([1,2,3,4],['LCL','ARG','THIS','THAT']):
            res.extend([
                '@'+str(k),
                'D=A',
                '@'+v,
                'M=D',
            ])
        
        # 准备Sys.init执行环境
        # 压入返回地址
        res.extend([
            '@'+self.label_symbol('bootstrap'),
            'D=A',

            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
        ])
        
        # 为Sys.init初始化帧布局
        for segment_name in ['LCL','ARG','THIS','THAT']:
            res.extend([
                '@'+segment_name,
                'D=M',
                
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1',
            ])
        
        # ARG = SP - 5 
        res.extend([
            '@5',
            'D=A',
            '@SP',
            'D=M-D',
            '@ARG',
            'M=D',
        ])
        # LCL = SP
        res.extend([
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
        ])
        # goto Sys.init
        res.extend([
            '@'+self.function_symbol('Sys.init'),
            '0;JMP',
            '('+self.label_symbol('bootstrap')+')',
            '@'+self.label_symbol('bootstrap'),
            '0;JMP',
        ]) 
        return res
            
    def writeLabel(self,label:str):
        # TODO 检查label有效性
        res=[]
        res.extend([
            '('+self.label_symbol(label)+')',
        ])
        print(res)
        self.asm_codes.append(res)
    def writeGoto(self,label:str):
        res=[]
        res.extend([
            '@'+self.label_symbol(label),
            '0;JMP'
        ])
        print(res)
        self.asm_codes.append(res)
    def writeIf(self,label:str):
        res=[]
        res.extend([
            # 获取栈顶数据
            '@SP',
            'AM=M-1',
            'D=M',
            # -1 表示 True
            # 0 表示 False
            # 设置跳转地址
            '@'+self.label_symbol(label),
            'D;JNE'
        ])
        print(res)
        self.asm_codes.append(res)
    def writeCall(self,function_name:str,numArgs:int):
        res=[]
        current_return_address = self.function_return_address_symbol(function_name)+str(self.ret_index)
        self.ret_index+=1
        res.extend([
            # 获取返回值地址，并压入栈中
            '@'+current_return_address,
            'D=A',

            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
        ])

        for segment_name in ['LCL','ARG','THIS','THAT']:
            res.extend([
            '@'+segment_name,
            'D=M',
            
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            ])
        
        res.extend([
            # ARG = SP - n - 5 
            '@'+str(numArgs+5),
            'D=A',
            '@SP',
            'D=M-D',
            '@ARG',
            'M=D',

            # LCL=SP
            '@SP',
            'D=M',
            '@LCL',
            'M=D',

            # goto f
            '@'+self.function_symbol(function_name),
            '0;JMP',

            # (return_address)
            '('+current_return_address+')',
        ])
        print(res)
        self.asm_codes.append(res)
    def writeReturn(self):
        res=[]
        res.extend([
            # R15 = LCL
            '@LCL',
            'D=M',
            '@R15',
            'M=D',
            
            # return address
            '@5',
            'D=A',
            '@R15',
            'A=M-D', # LCL - 5
            'D=M',
            '@R14',
            'M=D',

            # ARG = pop()
            '@SP',
            'AM=M-1', # A = SP - 1
            'D=M', # D = M[SP-1]
            '@ARG', 
            'A=M',
            'M=D',
            
            # SP = ARG + 1
            '@ARG',
            'D=M+1',
            '@SP',
            'M=D',
        ])
        for segment_name in ['THAT','THIS','ARG','LCL']:
             res.extend([
                '@R15',
                'AM=M-1',
                'D=M',
                '@'+segment_name,
                'M=D',
            ])

        res.extend([    
            # goto ret
            '@R14',
            'A=M',
            '0;JMP',
        ])
        print(res)
        self.asm_codes.append(res)
    def writeFunction(self,function_name:str,numLocals:int):
        res=[]
        res.extend([    
            # (f)
            '('+self.function_symbol(function_name) + ')',
        ])
        for i in range(0,numLocals):
            res.extend([    
                '@SP',
                'A=M',
                'M=0',
                '@SP',
                'M=M+1',
            ])
        print(res)
        self.asm_codes.append(res)

    
    def save(self,commands):
        current = 0
        with open(self.output_filename,'w') as f:
            idx=0
            if self.write_init_code:
                for code in self.InitCode():
                    if code.startswith('('):
                        f.write(code)
                    else:
                        f.write(code+'      //'+str(idx))
                        idx+=1
                    f.write('\n')
            for codes in self.asm_codes:
                f.write('//-start '+ commands[current]+'\n')
                for code in codes:
                    if code.startswith('('):
                        f.write(code)
                    else:
                        f.write(code+'      //'+str(idx))
                        idx+=1
                    f.write('\n')
                f.write('//-end '+ commands[current]+'\n')
                current+=1
        return

    
if __name__ == '__main__':
    print('当前工作目录为：',os.getcwd())
    input=os.getcwd() + '/'+sys.argv[1]
    source_filenames=[]
    output_filename=''
    # 判断是否是目录，获取到所有后缀名为.vm的文件
    if os.path.isdir(input):
        if input.endswith('/'):
            input=input[:-1]
        for filename in os.listdir(input):
            if os.path.isfile(input+'/'+filename) and filename[-2:] == 'vm' :
                    source_filenames.append(input+'/'+filename)
        if len(source_filenames) == 0:
            print('请输入正确的vm文件名或目录')
            exit(1)
        output_filename= input+'/'+os.path.basename(input)+".asm"
    elif os.path.isfile(input) and input[-2:] == 'vm' :
        source_filenames.append(input)
        output_filename=os.path.dirname(input) + '/' +os.path.basename(input)[:-2]+'asm'
    else:
        print('请输入正确的vm文件名或目录')
        exit(1)
    print("输出目录为：",output_filename)

    codeWriter = CodeWriter(output_filename,len(source_filenames)>1)
    # 为目录下文件创建一个parser和codeWriter
    
    commands = []
    for filename in source_filenames:
        assert filename[-2:] == 'vm','应输入名为Xxx.vm的文件'
        print("当前解析文件：",filename)
        vm_commands=[]
        with open(filename,'r') as f:
            for command in f:
                command=command.strip()
                if len(command)==0 or command[0]=='/':
                    continue
                if command.find('/') !=-1:
                    command=command[:command.find('/')]
                command=command.strip()
                vm_commands.append(command)
        label_prefix = os.path.basename(filename)[:-3]
        codeWriter.set_current_vm_source(os.path.basename(filename)[:-3])
        print('解析到的vm指令',vm_commands)
        for command in vm_commands:
            print(command + '->')
            commands.append(command)
            fields=command.split(' ')
            if len(fields) == 1:
                if fields[0] == 'return':
                    codeWriter.writeReturn()
                else:
                    codeWriter.writeArithmetic(command)
            elif command.startswith('push'):
                codeWriter.writePush(fields[1],fields[2])
            elif command.startswith('pop'):
                codeWriter.writePop(fields[1],fields[2])
            elif command.startswith('label'):
                codeWriter.writeLabel(label_prefix+'$'+fields[1])
            elif command.startswith('goto'):
                codeWriter.writeGoto(label_prefix+'$'+fields[1])
            elif command.startswith('if-goto'):
                codeWriter.writeIf(label_prefix+'$'+fields[1])
            elif command.startswith('function'):
                codeWriter.writeFunction(fields[1],int(fields[2]))
            elif command.startswith('call'):
                codeWriter.writeCall(fields[1],int(fields[2]))
            else:
                raise ValueError('非法VM码')  
    codeWriter.save(commands)    

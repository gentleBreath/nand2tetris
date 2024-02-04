import sys
import os


class CodeWriter:
    def __init__(self,filename:str) -> None:
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
        self.base_filename=os.path.basename(filename)
        self.asm_codes=[]
        self.symbol_index=0
        pass
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
                'D=M', # 取得第二个参数
                'A=A-1', 
                'M=M'+self.arith_dict[command]+'D' # M[SP-2]=M[SP-2]+D
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
        self.asm_codes.extend(res)
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
                    '@'+self.base_filename[:-4]+'.'+index,
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
            self.asm_codes.extend(res)

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
                    '@'+self.base_filename[:-4]+'.'+index,
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
            self.asm_codes.extend(res)


    def save(self):
        with open(self.output_filename,'w') as f:
            for code in self.asm_codes:
                f.write(code)
                f.write('\n')
        return

if __name__ == '__main__':
    print('当前工作目录为：',os.getcwd())
    input=os.getcwd() + '/'+sys.argv[1]
    source_filenames=[]
    output_filename=''
    # 判断是否是目录，获取到所有后缀名为.vm的文件
    if os.path.isdir(input):
        for filename in os.listdir(input):
            if os.path.isfile(input+'/'+filename) and filename[-2:] == 'vm' :
                    source_filenames.append(filename)
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

    codeWriter = CodeWriter(output_filename)
    
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
        print('解析到的vm指令为',vm_commands)
        for command in vm_commands:
            print(command + '->')
            # 写入结果
            if command.startswith('push'):
                fields=command.split(' ')
                codeWriter.writePush(fields[1],fields[2])
            elif command.startswith('pop'):
                fields=command.split(' ')
                codeWriter.writePop(fields[1],fields[2])
            else:
                codeWriter.writeArithmetic(command)
    codeWriter.save()
        

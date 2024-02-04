//-start push constant 0
@0      //0
D=A      //1
@SP      //2
A=M      //3
M=D      //4
@SP      //5
M=M+1      //6
//-end push constant 0
//-start pop local 0
@0      //7
D=A      //8
@LCL      //9
D=M+D      //10
@R15      //11
M=D      //12
@SP      //13
AM=M-1      //14
D=M      //15
@R15      //16
A=M      //17
M=D      //18
//-end pop local 0
//-start label LOOP
(BasicLoop$label$BasicLoop$LOOP)
//-end label LOOP
//-start push argument 0
@0      //19
D=A      //20
@ARG      //21
A=M+D      //22
D=M      //23
@SP      //24
A=M      //25
M=D      //26
@SP      //27
M=M+1      //28
//-end push argument 0
//-start push local 0
@0      //29
D=A      //30
@LCL      //31
A=M+D      //32
D=M      //33
@SP      //34
A=M      //35
M=D      //36
@SP      //37
M=M+1      //38
//-end push local 0
//-start add
@SP      //39
AM=M-1      //40
D=M      //41
A=A-1      //42
M=M+D      //43
//-end add
//-start pop local 0
@0      //44
D=A      //45
@LCL      //46
D=M+D      //47
@R15      //48
M=D      //49
@SP      //50
AM=M-1      //51
D=M      //52
@R15      //53
A=M      //54
M=D      //55
//-end pop local 0
//-start push argument 0
@0      //56
D=A      //57
@ARG      //58
A=M+D      //59
D=M      //60
@SP      //61
A=M      //62
M=D      //63
@SP      //64
M=M+1      //65
//-end push argument 0
//-start push constant 1
@1      //66
D=A      //67
@SP      //68
A=M      //69
M=D      //70
@SP      //71
M=M+1      //72
//-end push constant 1
//-start sub
@SP      //73
AM=M-1      //74
D=M      //75
A=A-1      //76
M=M-D      //77
//-end sub
//-start pop argument 0
@0      //78
D=A      //79
@ARG      //80
D=M+D      //81
@R15      //82
M=D      //83
@SP      //84
AM=M-1      //85
D=M      //86
@R15      //87
A=M      //88
M=D      //89
//-end pop argument 0
//-start push argument 0
@0      //90
D=A      //91
@ARG      //92
A=M+D      //93
D=M      //94
@SP      //95
A=M      //96
M=D      //97
@SP      //98
M=M+1      //99
//-end push argument 0
//-start if-goto LOOP
@SP      //100
AM=M-1      //101
D=M      //102
@BasicLoop$label$BasicLoop$LOOP      //103
D;JNE      //104
//-end if-goto LOOP
//-start push local 0
@0      //105
D=A      //106
@LCL      //107
A=M+D      //108
D=M      //109
@SP      //110
A=M      //111
M=D      //112
@SP      //113
M=M+1      //114
//-end push local 0

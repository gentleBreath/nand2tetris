//-start push argument 1
@1      //0
D=A      //1
@ARG      //2
A=M+D      //3
D=M      //4
@SP      //5
A=M      //6
M=D      //7
@SP      //8
M=M+1      //9
//-end push argument 1
//-start pop pointer 1
@1      //10
D=A      //11
@3      //12
D=A+D      //13
@R15      //14
M=D      //15
@SP      //16
AM=M-1      //17
D=M      //18
@R15      //19
A=M      //20
M=D      //21
//-end pop pointer 1
//-start push constant 0
@0      //22
D=A      //23
@SP      //24
A=M      //25
M=D      //26
@SP      //27
M=M+1      //28
//-end push constant 0
//-start pop that 0
@0      //29
D=A      //30
@THAT      //31
D=M+D      //32
@R15      //33
M=D      //34
@SP      //35
AM=M-1      //36
D=M      //37
@R15      //38
A=M      //39
M=D      //40
//-end pop that 0
//-start push constant 1
@1      //41
D=A      //42
@SP      //43
A=M      //44
M=D      //45
@SP      //46
M=M+1      //47
//-end push constant 1
//-start pop that 1
@1      //48
D=A      //49
@THAT      //50
D=M+D      //51
@R15      //52
M=D      //53
@SP      //54
AM=M-1      //55
D=M      //56
@R15      //57
A=M      //58
M=D      //59
//-end pop that 1
//-start push argument 0
@0      //60
D=A      //61
@ARG      //62
A=M+D      //63
D=M      //64
@SP      //65
A=M      //66
M=D      //67
@SP      //68
M=M+1      //69
//-end push argument 0
//-start push constant 2
@2      //70
D=A      //71
@SP      //72
A=M      //73
M=D      //74
@SP      //75
M=M+1      //76
//-end push constant 2
//-start sub
@SP      //77
AM=M-1      //78
D=M      //79
A=A-1      //80
M=M-D      //81
//-end sub
//-start pop argument 0
@0      //82
D=A      //83
@ARG      //84
D=M+D      //85
@R15      //86
M=D      //87
@SP      //88
AM=M-1      //89
D=M      //90
@R15      //91
A=M      //92
M=D      //93
//-end pop argument 0
//-start label LOOP
(FibonacciSeries$label$FibonacciSeries$LOOP)
//-end label LOOP
//-start push argument 0
@0      //94
D=A      //95
@ARG      //96
A=M+D      //97
D=M      //98
@SP      //99
A=M      //100
M=D      //101
@SP      //102
M=M+1      //103
//-end push argument 0
//-start if-goto COMPUTE_ELEMENT
@SP      //104
AM=M-1      //105
D=M      //106
@FibonacciSeries$label$FibonacciSeries$COMPUTE_ELEMENT      //107
D;JNE      //108
//-end if-goto COMPUTE_ELEMENT
//-start goto END
@FibonacciSeries$label$FibonacciSeries$END      //109
0;JMP      //110
//-end goto END
//-start label COMPUTE_ELEMENT
(FibonacciSeries$label$FibonacciSeries$COMPUTE_ELEMENT)
//-end label COMPUTE_ELEMENT
//-start push that 0
@0      //111
D=A      //112
@THAT      //113
A=M+D      //114
D=M      //115
@SP      //116
A=M      //117
M=D      //118
@SP      //119
M=M+1      //120
//-end push that 0
//-start push that 1
@1      //121
D=A      //122
@THAT      //123
A=M+D      //124
D=M      //125
@SP      //126
A=M      //127
M=D      //128
@SP      //129
M=M+1      //130
//-end push that 1
//-start add
@SP      //131
AM=M-1      //132
D=M      //133
A=A-1      //134
M=M+D      //135
//-end add
//-start pop that 2
@2      //136
D=A      //137
@THAT      //138
D=M+D      //139
@R15      //140
M=D      //141
@SP      //142
AM=M-1      //143
D=M      //144
@R15      //145
A=M      //146
M=D      //147
//-end pop that 2
//-start push pointer 1
@1      //148
D=A      //149
@3      //150
A=A+D      //151
D=M      //152
@SP      //153
A=M      //154
M=D      //155
@SP      //156
M=M+1      //157
//-end push pointer 1
//-start push constant 1
@1      //158
D=A      //159
@SP      //160
A=M      //161
M=D      //162
@SP      //163
M=M+1      //164
//-end push constant 1
//-start add
@SP      //165
AM=M-1      //166
D=M      //167
A=A-1      //168
M=M+D      //169
//-end add
//-start pop pointer 1
@1      //170
D=A      //171
@3      //172
D=A+D      //173
@R15      //174
M=D      //175
@SP      //176
AM=M-1      //177
D=M      //178
@R15      //179
A=M      //180
M=D      //181
//-end pop pointer 1
//-start push argument 0
@0      //182
D=A      //183
@ARG      //184
A=M+D      //185
D=M      //186
@SP      //187
A=M      //188
M=D      //189
@SP      //190
M=M+1      //191
//-end push argument 0
//-start push constant 1
@1      //192
D=A      //193
@SP      //194
A=M      //195
M=D      //196
@SP      //197
M=M+1      //198
//-end push constant 1
//-start sub
@SP      //199
AM=M-1      //200
D=M      //201
A=A-1      //202
M=M-D      //203
//-end sub
//-start pop argument 0
@0      //204
D=A      //205
@ARG      //206
D=M+D      //207
@R15      //208
M=D      //209
@SP      //210
AM=M-1      //211
D=M      //212
@R15      //213
A=M      //214
M=D      //215
//-end pop argument 0
//-start goto LOOP
@FibonacciSeries$label$FibonacciSeries$LOOP      //216
0;JMP      //217
//-end goto LOOP
//-start label END
(FibonacciSeries$label$FibonacciSeries$END)
//-end label END

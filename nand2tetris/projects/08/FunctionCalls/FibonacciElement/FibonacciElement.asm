@256      //0
D=A      //1
@SP      //2
M=D      //3
@1      //4
D=A      //5
@LCL      //6
M=D      //7
@2      //8
D=A      //9
@ARG      //10
M=D      //11
@3      //12
D=A      //13
@THIS      //14
M=D      //15
@4      //16
D=A      //17
@THAT      //18
M=D      //19
@FibonacciElement$label$bootstrap      //20
D=A      //21
@SP      //22
A=M      //23
M=D      //24
@SP      //25
M=M+1      //26
@LCL      //27
D=M      //28
@SP      //29
A=M      //30
M=D      //31
@SP      //32
M=M+1      //33
@ARG      //34
D=M      //35
@SP      //36
A=M      //37
M=D      //38
@SP      //39
M=M+1      //40
@THIS      //41
D=M      //42
@SP      //43
A=M      //44
M=D      //45
@SP      //46
M=M+1      //47
@THAT      //48
D=M      //49
@SP      //50
A=M      //51
M=D      //52
@SP      //53
M=M+1      //54
@5      //55
D=A      //56
@SP      //57
D=M-D      //58
@ARG      //59
M=D      //60
@SP      //61
D=M      //62
@LCL      //63
M=D      //64
@FibonacciElement$func$Sys.init      //65
0;JMP      //66
(FibonacciElement$label$bootstrap)
@FibonacciElement$label$bootstrap      //67
0;JMP      //68
//-start function Sys.init 0
(FibonacciElement$func$Sys.init)
//-end function Sys.init 0
//-start push constant 4
@4      //69
D=A      //70
@SP      //71
A=M      //72
M=D      //73
@SP      //74
M=M+1      //75
//-end push constant 4
//-start call Main.fibonacci 1
@FibonacciElement$func$Main.fibonacci_return_address0      //76
D=A      //77
@SP      //78
A=M      //79
M=D      //80
@SP      //81
M=M+1      //82
@LCL      //83
D=M      //84
@SP      //85
A=M      //86
M=D      //87
@SP      //88
M=M+1      //89
@ARG      //90
D=M      //91
@SP      //92
A=M      //93
M=D      //94
@SP      //95
M=M+1      //96
@THIS      //97
D=M      //98
@SP      //99
A=M      //100
M=D      //101
@SP      //102
M=M+1      //103
@THAT      //104
D=M      //105
@SP      //106
A=M      //107
M=D      //108
@SP      //109
M=M+1      //110
@6      //111
D=A      //112
@SP      //113
D=M-D      //114
@ARG      //115
M=D      //116
@SP      //117
D=M      //118
@LCL      //119
M=D      //120
@FibonacciElement$func$Main.fibonacci      //121
0;JMP      //122
(FibonacciElement$func$Main.fibonacci_return_address0)
//-end call Main.fibonacci 1
//-start label END
(FibonacciElement$label$Sys$END)
//-end label END
//-start goto END
@FibonacciElement$label$Sys$END      //123
0;JMP      //124
//-end goto END
//-start function Main.fibonacci 0
(FibonacciElement$func$Main.fibonacci)
//-end function Main.fibonacci 0
//-start push argument 0
@0      //125
D=A      //126
@ARG      //127
A=M+D      //128
D=M      //129
@SP      //130
A=M      //131
M=D      //132
@SP      //133
M=M+1      //134
//-end push argument 0
//-start push constant 2
@2      //135
D=A      //136
@SP      //137
A=M      //138
M=D      //139
@SP      //140
M=M+1      //141
//-end push constant 2
//-start lt
@SP      //142
AM=M-1      //143
D=M      //144
A=A-1      //145
D=M-D      //146
M=0      //147
@FibonacciEle_lt_0      //148
D;JGE      //149
@SP      //150
A=M-1      //151
M=-1      //152
(FibonacciEle_lt_0)
//-end lt
//-start if-goto N_LT_2
@SP      //153
AM=M-1      //154
D=M      //155
@FibonacciElement$label$Main$N_LT_2      //156
D;JNE      //157
//-end if-goto N_LT_2
//-start goto N_GE_2
@FibonacciElement$label$Main$N_GE_2      //158
0;JMP      //159
//-end goto N_GE_2
//-start label N_LT_2
(FibonacciElement$label$Main$N_LT_2)
//-end label N_LT_2
//-start push argument 0
@0      //160
D=A      //161
@ARG      //162
A=M+D      //163
D=M      //164
@SP      //165
A=M      //166
M=D      //167
@SP      //168
M=M+1      //169
//-end push argument 0
//-start return
@LCL      //170
D=M      //171
@R15      //172
M=D      //173
@5      //174
D=A      //175
@R15      //176
A=M-D      //177
D=M      //178
@R14      //179
M=D      //180
@SP      //181
AM=M-1      //182
D=M      //183
@ARG      //184
A=M      //185
M=D      //186
@ARG      //187
D=M+1      //188
@SP      //189
M=D      //190
@R15      //191
AM=M-1      //192
D=M      //193
@THAT      //194
M=D      //195
@R15      //196
AM=M-1      //197
D=M      //198
@THIS      //199
M=D      //200
@R15      //201
AM=M-1      //202
D=M      //203
@ARG      //204
M=D      //205
@R15      //206
AM=M-1      //207
D=M      //208
@LCL      //209
M=D      //210
@R14      //211
A=M      //212
0;JMP      //213
//-end return
//-start label N_GE_2
(FibonacciElement$label$Main$N_GE_2)
//-end label N_GE_2
//-start push argument 0
@0      //214
D=A      //215
@ARG      //216
A=M+D      //217
D=M      //218
@SP      //219
A=M      //220
M=D      //221
@SP      //222
M=M+1      //223
//-end push argument 0
//-start push constant 2
@2      //224
D=A      //225
@SP      //226
A=M      //227
M=D      //228
@SP      //229
M=M+1      //230
//-end push constant 2
//-start sub
@SP      //231
AM=M-1      //232
D=M      //233
A=A-1      //234
M=M-D      //235
//-end sub
//-start call Main.fibonacci 1
@FibonacciElement$func$Main.fibonacci_return_address1      //236
D=A      //237
@SP      //238
A=M      //239
M=D      //240
@SP      //241
M=M+1      //242
@LCL      //243
D=M      //244
@SP      //245
A=M      //246
M=D      //247
@SP      //248
M=M+1      //249
@ARG      //250
D=M      //251
@SP      //252
A=M      //253
M=D      //254
@SP      //255
M=M+1      //256
@THIS      //257
D=M      //258
@SP      //259
A=M      //260
M=D      //261
@SP      //262
M=M+1      //263
@THAT      //264
D=M      //265
@SP      //266
A=M      //267
M=D      //268
@SP      //269
M=M+1      //270
@6      //271
D=A      //272
@SP      //273
D=M-D      //274
@ARG      //275
M=D      //276
@SP      //277
D=M      //278
@LCL      //279
M=D      //280
@FibonacciElement$func$Main.fibonacci      //281
0;JMP      //282
(FibonacciElement$func$Main.fibonacci_return_address1)
//-end call Main.fibonacci 1
//-start push argument 0
@0      //283
D=A      //284
@ARG      //285
A=M+D      //286
D=M      //287
@SP      //288
A=M      //289
M=D      //290
@SP      //291
M=M+1      //292
//-end push argument 0
//-start push constant 1
@1      //293
D=A      //294
@SP      //295
A=M      //296
M=D      //297
@SP      //298
M=M+1      //299
//-end push constant 1
//-start sub
@SP      //300
AM=M-1      //301
D=M      //302
A=A-1      //303
M=M-D      //304
//-end sub
//-start call Main.fibonacci 1
@FibonacciElement$func$Main.fibonacci_return_address2      //305
D=A      //306
@SP      //307
A=M      //308
M=D      //309
@SP      //310
M=M+1      //311
@LCL      //312
D=M      //313
@SP      //314
A=M      //315
M=D      //316
@SP      //317
M=M+1      //318
@ARG      //319
D=M      //320
@SP      //321
A=M      //322
M=D      //323
@SP      //324
M=M+1      //325
@THIS      //326
D=M      //327
@SP      //328
A=M      //329
M=D      //330
@SP      //331
M=M+1      //332
@THAT      //333
D=M      //334
@SP      //335
A=M      //336
M=D      //337
@SP      //338
M=M+1      //339
@6      //340
D=A      //341
@SP      //342
D=M-D      //343
@ARG      //344
M=D      //345
@SP      //346
D=M      //347
@LCL      //348
M=D      //349
@FibonacciElement$func$Main.fibonacci      //350
0;JMP      //351
(FibonacciElement$func$Main.fibonacci_return_address2)
//-end call Main.fibonacci 1
//-start add
@SP      //352
AM=M-1      //353
D=M      //354
A=A-1      //355
M=M+D      //356
//-end add
//-start return
@LCL      //357
D=M      //358
@R15      //359
M=D      //360
@5      //361
D=A      //362
@R15      //363
A=M-D      //364
D=M      //365
@R14      //366
M=D      //367
@SP      //368
AM=M-1      //369
D=M      //370
@ARG      //371
A=M      //372
M=D      //373
@ARG      //374
D=M+1      //375
@SP      //376
M=D      //377
@R15      //378
AM=M-1      //379
D=M      //380
@THAT      //381
M=D      //382
@R15      //383
AM=M-1      //384
D=M      //385
@THIS      //386
M=D      //387
@R15      //388
AM=M-1      //389
D=M      //390
@ARG      //391
M=D      //392
@R15      //393
AM=M-1      //394
D=M      //395
@LCL      //396
M=D      //397
@R14      //398
A=M      //399
0;JMP      //400
//-end return

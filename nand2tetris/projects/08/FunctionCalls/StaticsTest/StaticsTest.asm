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
@StaticsTest$label$bootstrap      //20
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
@StaticsTest$func$Sys.init      //65
0;JMP      //66
(StaticsTest$label$bootstrap)
@StaticsTest$label$bootstrap      //67
0;JMP      //68
//-start function Class2.set 0
(StaticsTest$func$Class2.set)
//-end function Class2.set 0
//-start push argument 0
@0      //69
D=A      //70
@ARG      //71
A=M+D      //72
D=M      //73
@SP      //74
A=M      //75
M=D      //76
@SP      //77
M=M+1      //78
//-end push argument 0
//-start pop static 0
@StaticsTest$Class2$static$0      //79
D=A      //80
@R15      //81
M=D      //82
@SP      //83
AM=M-1      //84
D=M      //85
@R15      //86
A=M      //87
M=D      //88
//-end pop static 0
//-start push argument 1
@1      //89
D=A      //90
@ARG      //91
A=M+D      //92
D=M      //93
@SP      //94
A=M      //95
M=D      //96
@SP      //97
M=M+1      //98
//-end push argument 1
//-start pop static 1
@StaticsTest$Class2$static$1      //99
D=A      //100
@R15      //101
M=D      //102
@SP      //103
AM=M-1      //104
D=M      //105
@R15      //106
A=M      //107
M=D      //108
//-end pop static 1
//-start push constant 0
@0      //109
D=A      //110
@SP      //111
A=M      //112
M=D      //113
@SP      //114
M=M+1      //115
//-end push constant 0
//-start return
@LCL      //116
D=M      //117
@R15      //118
M=D      //119
@5      //120
D=A      //121
@R15      //122
A=M-D      //123
D=M      //124
@R14      //125
M=D      //126
@SP      //127
AM=M-1      //128
D=M      //129
@ARG      //130
A=M      //131
M=D      //132
@ARG      //133
D=M+1      //134
@SP      //135
M=D      //136
@R15      //137
AM=M-1      //138
D=M      //139
@THAT      //140
M=D      //141
@R15      //142
AM=M-1      //143
D=M      //144
@THIS      //145
M=D      //146
@R15      //147
AM=M-1      //148
D=M      //149
@ARG      //150
M=D      //151
@R15      //152
AM=M-1      //153
D=M      //154
@LCL      //155
M=D      //156
@R14      //157
A=M      //158
0;JMP      //159
//-end return
//-start function Class2.get 0
(StaticsTest$func$Class2.get)
//-end function Class2.get 0
//-start push static 0
@StaticsTest$Class2$static$0      //160
D=M      //161
@SP      //162
A=M      //163
M=D      //164
@SP      //165
M=M+1      //166
//-end push static 0
//-start push static 1
@StaticsTest$Class2$static$1      //167
D=M      //168
@SP      //169
A=M      //170
M=D      //171
@SP      //172
M=M+1      //173
//-end push static 1
//-start sub
@SP      //174
AM=M-1      //175
D=M      //176
A=A-1      //177
M=M-D      //178
//-end sub
//-start return
@LCL      //179
D=M      //180
@R15      //181
M=D      //182
@5      //183
D=A      //184
@R15      //185
A=M-D      //186
D=M      //187
@R14      //188
M=D      //189
@SP      //190
AM=M-1      //191
D=M      //192
@ARG      //193
A=M      //194
M=D      //195
@ARG      //196
D=M+1      //197
@SP      //198
M=D      //199
@R15      //200
AM=M-1      //201
D=M      //202
@THAT      //203
M=D      //204
@R15      //205
AM=M-1      //206
D=M      //207
@THIS      //208
M=D      //209
@R15      //210
AM=M-1      //211
D=M      //212
@ARG      //213
M=D      //214
@R15      //215
AM=M-1      //216
D=M      //217
@LCL      //218
M=D      //219
@R14      //220
A=M      //221
0;JMP      //222
//-end return
//-start function Sys.init 0
(StaticsTest$func$Sys.init)
//-end function Sys.init 0
//-start push constant 6
@6      //223
D=A      //224
@SP      //225
A=M      //226
M=D      //227
@SP      //228
M=M+1      //229
//-end push constant 6
//-start push constant 8
@8      //230
D=A      //231
@SP      //232
A=M      //233
M=D      //234
@SP      //235
M=M+1      //236
//-end push constant 8
//-start call Class1.set 2
@StaticsTest$func$Class1.set_return_address0      //237
D=A      //238
@SP      //239
A=M      //240
M=D      //241
@SP      //242
M=M+1      //243
@LCL      //244
D=M      //245
@SP      //246
A=M      //247
M=D      //248
@SP      //249
M=M+1      //250
@ARG      //251
D=M      //252
@SP      //253
A=M      //254
M=D      //255
@SP      //256
M=M+1      //257
@THIS      //258
D=M      //259
@SP      //260
A=M      //261
M=D      //262
@SP      //263
M=M+1      //264
@THAT      //265
D=M      //266
@SP      //267
A=M      //268
M=D      //269
@SP      //270
M=M+1      //271
@7      //272
D=A      //273
@SP      //274
D=M-D      //275
@ARG      //276
M=D      //277
@SP      //278
D=M      //279
@LCL      //280
M=D      //281
@StaticsTest$func$Class1.set      //282
0;JMP      //283
(StaticsTest$func$Class1.set_return_address0)
//-end call Class1.set 2
//-start pop temp 0
@0      //284
D=A      //285
@5      //286
D=A+D      //287
@R15      //288
M=D      //289
@SP      //290
AM=M-1      //291
D=M      //292
@R15      //293
A=M      //294
M=D      //295
//-end pop temp 0
//-start push constant 23
@23      //296
D=A      //297
@SP      //298
A=M      //299
M=D      //300
@SP      //301
M=M+1      //302
//-end push constant 23
//-start push constant 15
@15      //303
D=A      //304
@SP      //305
A=M      //306
M=D      //307
@SP      //308
M=M+1      //309
//-end push constant 15
//-start call Class2.set 2
@StaticsTest$func$Class2.set_return_address1      //310
D=A      //311
@SP      //312
A=M      //313
M=D      //314
@SP      //315
M=M+1      //316
@LCL      //317
D=M      //318
@SP      //319
A=M      //320
M=D      //321
@SP      //322
M=M+1      //323
@ARG      //324
D=M      //325
@SP      //326
A=M      //327
M=D      //328
@SP      //329
M=M+1      //330
@THIS      //331
D=M      //332
@SP      //333
A=M      //334
M=D      //335
@SP      //336
M=M+1      //337
@THAT      //338
D=M      //339
@SP      //340
A=M      //341
M=D      //342
@SP      //343
M=M+1      //344
@7      //345
D=A      //346
@SP      //347
D=M-D      //348
@ARG      //349
M=D      //350
@SP      //351
D=M      //352
@LCL      //353
M=D      //354
@StaticsTest$func$Class2.set      //355
0;JMP      //356
(StaticsTest$func$Class2.set_return_address1)
//-end call Class2.set 2
//-start pop temp 0
@0      //357
D=A      //358
@5      //359
D=A+D      //360
@R15      //361
M=D      //362
@SP      //363
AM=M-1      //364
D=M      //365
@R15      //366
A=M      //367
M=D      //368
//-end pop temp 0
//-start call Class1.get 0
@StaticsTest$func$Class1.get_return_address2      //369
D=A      //370
@SP      //371
A=M      //372
M=D      //373
@SP      //374
M=M+1      //375
@LCL      //376
D=M      //377
@SP      //378
A=M      //379
M=D      //380
@SP      //381
M=M+1      //382
@ARG      //383
D=M      //384
@SP      //385
A=M      //386
M=D      //387
@SP      //388
M=M+1      //389
@THIS      //390
D=M      //391
@SP      //392
A=M      //393
M=D      //394
@SP      //395
M=M+1      //396
@THAT      //397
D=M      //398
@SP      //399
A=M      //400
M=D      //401
@SP      //402
M=M+1      //403
@5      //404
D=A      //405
@SP      //406
D=M-D      //407
@ARG      //408
M=D      //409
@SP      //410
D=M      //411
@LCL      //412
M=D      //413
@StaticsTest$func$Class1.get      //414
0;JMP      //415
(StaticsTest$func$Class1.get_return_address2)
//-end call Class1.get 0
//-start call Class2.get 0
@StaticsTest$func$Class2.get_return_address3      //416
D=A      //417
@SP      //418
A=M      //419
M=D      //420
@SP      //421
M=M+1      //422
@LCL      //423
D=M      //424
@SP      //425
A=M      //426
M=D      //427
@SP      //428
M=M+1      //429
@ARG      //430
D=M      //431
@SP      //432
A=M      //433
M=D      //434
@SP      //435
M=M+1      //436
@THIS      //437
D=M      //438
@SP      //439
A=M      //440
M=D      //441
@SP      //442
M=M+1      //443
@THAT      //444
D=M      //445
@SP      //446
A=M      //447
M=D      //448
@SP      //449
M=M+1      //450
@5      //451
D=A      //452
@SP      //453
D=M-D      //454
@ARG      //455
M=D      //456
@SP      //457
D=M      //458
@LCL      //459
M=D      //460
@StaticsTest$func$Class2.get      //461
0;JMP      //462
(StaticsTest$func$Class2.get_return_address3)
//-end call Class2.get 0
//-start label END
(StaticsTest$label$Sys$END)
//-end label END
//-start goto END
@StaticsTest$label$Sys$END      //463
0;JMP      //464
//-end goto END
//-start function Class1.set 0
(StaticsTest$func$Class1.set)
//-end function Class1.set 0
//-start push argument 0
@0      //465
D=A      //466
@ARG      //467
A=M+D      //468
D=M      //469
@SP      //470
A=M      //471
M=D      //472
@SP      //473
M=M+1      //474
//-end push argument 0
//-start pop static 0
@StaticsTest$Class1$static$0      //475
D=A      //476
@R15      //477
M=D      //478
@SP      //479
AM=M-1      //480
D=M      //481
@R15      //482
A=M      //483
M=D      //484
//-end pop static 0
//-start push argument 1
@1      //485
D=A      //486
@ARG      //487
A=M+D      //488
D=M      //489
@SP      //490
A=M      //491
M=D      //492
@SP      //493
M=M+1      //494
//-end push argument 1
//-start pop static 1
@StaticsTest$Class1$static$1      //495
D=A      //496
@R15      //497
M=D      //498
@SP      //499
AM=M-1      //500
D=M      //501
@R15      //502
A=M      //503
M=D      //504
//-end pop static 1
//-start push constant 0
@0      //505
D=A      //506
@SP      //507
A=M      //508
M=D      //509
@SP      //510
M=M+1      //511
//-end push constant 0
//-start return
@LCL      //512
D=M      //513
@R15      //514
M=D      //515
@5      //516
D=A      //517
@R15      //518
A=M-D      //519
D=M      //520
@R14      //521
M=D      //522
@SP      //523
AM=M-1      //524
D=M      //525
@ARG      //526
A=M      //527
M=D      //528
@ARG      //529
D=M+1      //530
@SP      //531
M=D      //532
@R15      //533
AM=M-1      //534
D=M      //535
@THAT      //536
M=D      //537
@R15      //538
AM=M-1      //539
D=M      //540
@THIS      //541
M=D      //542
@R15      //543
AM=M-1      //544
D=M      //545
@ARG      //546
M=D      //547
@R15      //548
AM=M-1      //549
D=M      //550
@LCL      //551
M=D      //552
@R14      //553
A=M      //554
0;JMP      //555
//-end return
//-start function Class1.get 0
(StaticsTest$func$Class1.get)
//-end function Class1.get 0
//-start push static 0
@StaticsTest$Class1$static$0      //556
D=M      //557
@SP      //558
A=M      //559
M=D      //560
@SP      //561
M=M+1      //562
//-end push static 0
//-start push static 1
@StaticsTest$Class1$static$1      //563
D=M      //564
@SP      //565
A=M      //566
M=D      //567
@SP      //568
M=M+1      //569
//-end push static 1
//-start sub
@SP      //570
AM=M-1      //571
D=M      //572
A=A-1      //573
M=M-D      //574
//-end sub
//-start return
@LCL      //575
D=M      //576
@R15      //577
M=D      //578
@5      //579
D=A      //580
@R15      //581
A=M-D      //582
D=M      //583
@R14      //584
M=D      //585
@SP      //586
AM=M-1      //587
D=M      //588
@ARG      //589
A=M      //590
M=D      //591
@ARG      //592
D=M+1      //593
@SP      //594
M=D      //595
@R15      //596
AM=M-1      //597
D=M      //598
@THAT      //599
M=D      //600
@R15      //601
AM=M-1      //602
D=M      //603
@THIS      //604
M=D      //605
@R15      //606
AM=M-1      //607
D=M      //608
@ARG      //609
M=D      //610
@R15      //611
AM=M-1      //612
D=M      //613
@LCL      //614
M=D      //615
@R14      //616
A=M      //617
0;JMP      //618
//-end return

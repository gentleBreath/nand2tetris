// R2 = 0
@R2
M=0
(LOOP)
// if M[R0] == 0 Jump
@R0
D=M
@END
D;JEQ
// M[R0]=M[R0]-1
@R0
M=M-1
// M[R2]=M[R2]+M[R1]
@R1
D=M
@R2
M=M+D
@LOOP
0;JMP
(END)
@END
0;JMP

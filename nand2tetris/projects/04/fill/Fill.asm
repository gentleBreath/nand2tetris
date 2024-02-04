// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.


// cur = screen
@SCREEN
D=A
@CURSOR
M=D

(LOOP)
@KBD
D=M
@BLACK
D;JGT
@WHITE
D;JMP

(WHITE)
@SCREEN
D=A
@CURSOR
D=M-D
@LOOP
D;JLT
@CURSOR
AM=M-1
M=0
@WHITE
0;JMP

(BLACK)
@KBD
D=A
@CURSOR
D=M-D
@LOOP
D;JGE
@CURSOR
A=M
M=-1
@CURSOR
M=M+1
@BLACK
0;JMP
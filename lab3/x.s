@@@ file x.s - COMP1203 2016/17 Lab3 @@@@@@@@@@@@
	.syntax unified
        .align  2
        .global x
        .type   x, %function
x:
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@ r0, r1 are the two arguments              @@@
@@@ at end of function, result must be in r0  @@@
@@@ start user-defined assembly language code @@@

        add     r0, r0, #5                         @@@ - "line 12"

@@@ end user-defined assembly language code   @@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        bx      lr
        .size   x, .-x
        .ident  "GCC: (Raspbian 4.9.2-10) 4.9.2"
        .section        .note.GNU-stack,"",%progbits


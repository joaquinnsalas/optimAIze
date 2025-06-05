
.globl lab04b

lab04b:
    SUB SP, SP, 16     // Decrement the stack pointer by 16 to make space
    STUR LR, [SP, #8]
    STUR X0, [SP, #0]  // Store n on the stack. X0 is the initial value of n

    CMP X0, #1         // Compare n and 1.
    B.GE else          // if n <= 1, go to else
    MOV X0, #1
    ADD SP, SP, #16    // pop stack
    BR LR

else:
    SUB X0, X0, #1     // Calculate n-1
    BL lab04b          // Recursive call to lab04b with n-1 
    LDUR X1, [SP, #0]


    BL my_mul          // Multiply n with result of recursive call


    LDUR LR, [SP, #8]  // Restore caller's return address
    ADD SP, SP, #16    // Restore stack pointer
    BR LR              // return










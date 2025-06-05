//`timescale 1ns / 1ps

module NextPClogic(NextPC, CurrentPC, SignExtImm64, Branch, ALUZero, Uncondbranch); 
   input [63:0] CurrentPC, SignExtImm64; 
   input 	Branch, ALUZero, Uncondbranch; 
   output reg [63:0] NextPC; 

   /* write your code here */ 

    //calculating NextPC based on the condition of the Branch, Unconditional Branch and ALUZero
    always @(*) begin
        //Check if a conditional branch should be taken (branch and ALUZero are true) or if its an unconditional branch
        if ((Branch && ALUZero) || Uncondbranch) begin //If unconditional, branch regardless of ALUZero
            //This is the offset for branching, signextend 64
            NextPC = CurrentPC + SignExtImm64; //got rid of the <<2 and everything worked
        end
        else begin 
            //If neither are true, the next instruction is sequential, so add 4 to the CurrentPC
            NextPC = CurrentPC + 64'd4; 
        end
    end

    endmodule
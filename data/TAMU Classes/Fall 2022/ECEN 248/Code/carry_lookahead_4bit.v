`timescale 1ns / 1ps
`default_nettype none

module carry_lookahead_4bit(Cout, S, X, Y, Cin);
    output wire Cout; //C4 for a 4-bit adder
    output wire [3:0] S; // final 4-bit sum vector
    input wire [3:0] X, Y; //the 4-bit addends
    input wire Cin; //input carry
    
    wire [3:0] G, P;
    wire [4:1] carry;
    
    generate_propagate_unit unit0(G, P, X, Y);
    carry_lookahead_unit unit1(carry, G, P, Cin);
    summation_unit unit2(S, P, {carry[3:1], Cin});
    
    assign Cout = carry[4];
    
endmodule


`timescale 1ns / 1ps
`default_nettype none

module generate_propagate_unit(G, P, X, Y);
    output wire [3:0] G, P;
    input wire [3:0] X, Y;

    assign #2 G[0] = X[0] & Y[0];
    assign #2 P[0] = X[0] ^ Y[0];
    assign #2 G[1] = X[1] & Y[1];
    assign #2 P[1] = X[1] ^ Y[1];
    assign #2 G[2] = X[2] & Y[2];
    assign #2 P[2] = X[2] ^ Y[2];
    assign #2 G[3] = X[3] & Y[3];
    assign #2 P[3] = X[3] ^ Y[3];
   
endmodule

`timescale 1ns / 1ps
`default_nettype none

module summation_unit(S, P, C);
    output wire [3:0] S;
    input wire [3:0] P;
    input wire [3:0] C;

    //delay will be added here to prevent from any error
    assign #4 S[0] = P[0] ^ C[0];
    assign #4 S[1] = P[1] ^ C[1];
    assign #4 S[2] = P[2] ^ C[2];
    assign #4 S[3] = P[3] ^ C[3];
endmodule

`timescale 1ns / 1ps
`default_nettype none

module carry_lookahead_unit(C, G, P, C0);
    output wire [4:1] C;
    input wire [3:0] G, P;
    input wire C0;
    
    assign C[1] = G[0] | (P[0] & C0);
    assign C[2] = G[1] | (P[1] & C[1]);
    assign C[3] = G[2] | (P[2] & C[2]);
    assign C[4] = G[3] | (P[3] & C[3]);
endmodule


///////// LAB 10 //////////

`timescale 1ns / 1ps
`default_nettype none

module combination_lock_fsm(
    output reg [1:0] state,
    output wire [3:0] Lock, // asserted when locked
    input wire Key1, //unlock button 1
    input wire Key2, //unlock button 2
    input wire [3:0] Password, //indicate number
    input wire Reset, //reset
    input wire Clk);
    
    parameter s0 = 2'b00;
    parameter s1 = 2'b01;
    parameter s2 = 2'b10;
    parameter s3 = 2'b11;

    reg [1:0] state;
    reg [1:0] nextState;
    
    always@(*) //ourely combinational
        case(state)
            s0: begin
                if (Key1 == 1 && Password == 1101) //move to next state
                      nextState = s1;
                else 
                      nextState = s0;          
            end
            s1: begin
                if (Key2 == 1 && Password == 0111) //move to next state
                      nextState = s2; //onto the next state
                if (Key2 == 1 && Password != 0111) //move to the last state
                      nextState = s2; //onto the next state
                else 
                      nextState = s1;
            end 
            s2: begin
                if (Key1 == 1 && Password == 1001)
                      nextState = s3; //Onto the next state
                if (Key1 == 1 && Password != 1001) //Go to state 0
                      nextState = s0;
                else
                      nextState = s2; //stay in 2nd state
            end
            s3: begin
                if (Reset == 1)
                      nextState = s0;
                else
                      nextState = s3;
            end
        endcase
    assign Lock = (state == s3)? 4'b1111: 4'b0000;
endmodule 
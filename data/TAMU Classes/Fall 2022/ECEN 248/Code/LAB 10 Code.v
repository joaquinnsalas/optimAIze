`timescale 1ns / 1ps
`default_nettype none

module combination_lock_fsm(
    output reg [1:0] state,
    output wire [3:0] Lock, // asserted when locked
    input wire Key1, //unlock button 1
    input wire Key2, //unlock button 2
    input wire [3:0] Password, //indicate number
    input wire Reset, //reset
    input wire Clk
    );
    parameter s0 = 3'b000;
    parameter s1 = 3'b001;
    parameter s2 = 3'b010;
    parameter s3 = 3'b011;
    parameter s4 = 3'b111;

    reg [1:0] state;
    reg [1:0] nextState;
    
    always@(*) //ourely combinational
        case(state)
            s0: begin
                if (Key1 == 1 && Password == 110) //move to next state
                      nextState = s1;
                else 
                      nextState = s0;          
            end
            s1: begin
                if (Key2 == 1 && Password == 011) //move to next state
                      nextState = s2; //onto the next state
                if (Key2 == 1 && Password != 011) //move to the last state
                      nextState = s2; //onto the next state
                else 
                      nextState = s1;
            end 
            s2: begin
                if (Key1 == 1 && Password == 101)
                      nextState = s3; //Onto the next state
                if (Key1 == 1 && Password != 101) //Go to state 0
                      nextState = s0;
                else
                      nextState = s2; //stay in 2nd state
            end
            s3: begin
                if (Key2 == 1 && Password == 1111)
                      nextState = s4;
                if (Key2 == 1 && Password != 1111)
                      nextState = s0;
                else
                      nextState = s3;
            end
            s4: begin
                if (Reset == 1)
                      nextState = s0;
                else 
                      nextState = s4;
            end
        endcase
    assign Lock = (state == s3)? 3'b111: 3'b000;
endmodule

////////// 4 NUMBERS //////////

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
`timescale 1ns / 1ps

//EXAMPLE FOR MINI REGISTER
// module MiniRegisterFile(BusA, BusB, BusW, RW, RegWr, Clk);
//     output [63:0] BusA;
//     output [63:0] BusB;
//     input [63:0] BusW;
//     input RW;
//     input RegWr;
//     input Clk;
//     reg [31:0] registers [1:0];
     
//     assign #2 BusA = registers[0];
//     assign #2 BusB = registers[1];
     
//     always @ (negedge Clk) begin
//         if(RegWr)
//             registers[RW] <= #3 BusW;
//     end


module RegisterFile( BusA, BusB, BusW, RA, RB, RW, RegWr, Clk );
    output reg [63:0] BusA;
    output reg [63:0] BusB; //Make outputs "reg"
    input [63:0] BusW;
    input [4:0] RA;
    input [4:0] RB;
    input [4:0] RW;
    input RegWr;
    input Clk;
    reg[63:0] registers[31:0]; // Change from 32 to 64 bits with registers 32 bits wide

// Read operation with a delay
always @(*) begin
    // read from the registers with 2-ticks for the delay
    // The #2 is for the time delay
    // check that register 31 is incorporated in the read logic
    BusA <= #2 (RA == 5'b11111) ? 64'b0 : registers[RA];
    BusB <= #2 (RB == 5'b11111) ? 64'b0 : registers[RB]; //using <= non blocking so it loads all at once
end

// write to reg on the falling edge of a 3tick clock
always @(negedge Clk) begin
    if (RegWr && RW != 5'b11111) begin //check if regwr is on and the value in RW is not 32
        registers[RW] <= #3 BusW;
    end
end

endmodule


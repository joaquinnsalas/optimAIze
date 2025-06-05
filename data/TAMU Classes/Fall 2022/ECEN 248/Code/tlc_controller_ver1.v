`timescale 1ns / 1ps

module tlc_controller_ver1(
    output wire [1:0] highwaySignal, farmSignal,
    output wire [3:0] JB,
    input wire Clk,
    input wire Rst
);
    wire RstSync;
    wire RstCount;
    reg [30:0] Count;

    assign JB[3] = RstCount;

    synchronizer syncRst(RstSync, Rst, Clk);

    tlc_fsm FSM(
        .state(JB[2:0]),
        .RstCount(RstCount),
        .highwaySignal(highwaySignal),
        .farmSignal(farmSignal),
        .Count(Count),
        .Clk(Clk),
        .Rst(RstSync)
    );

        always@(posedge Clk)
        if(RstCount)
            Count <= 0;
        else
            Count <= Count + 1;
endmodule
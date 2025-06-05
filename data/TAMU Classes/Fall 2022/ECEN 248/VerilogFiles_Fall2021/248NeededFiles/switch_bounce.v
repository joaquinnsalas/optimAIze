`timescale 1ns / 1ps

module switch_bounce(
    input wire BTN,
    output wire JB_0
    );
    
    assign JB_0 = BTN;

endmodule

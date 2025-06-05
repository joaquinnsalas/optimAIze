`timescale 1ns / 1ps
`default_nettype none

module carry_lookahead_16bit(Cout, S, X, Y, Cin);

    /*ports are wires as we will use structural*/
    output wire Cout; //C_16 for a 16-bit adder
    output wire [15:0] S; //final 16-bit sum vector
    input wire [15:0] X, Y; //the 16-bit addends
    input wire Cin; //input carry!

    /*intermediate nets*/
    wire [16:0] C; //17-bit carry vector 
    wire [15:0] P, G; //generate and propagate vectors
    wire [3:0] P_star, G_star; //block gens and props

    /*hook up input and output carry*/
    assign C[0] = Cin;

    /*sub-modules*/
    //instantiate the generate/propagate unit here
    generate_propagate_unit GPU(G, P, X, Y);

    /*for the more complicated module instantiations *
    * you will probably find this form easier to read */
    block_carry_lookahead_unit BCLAU0(
        /*since we are being explicit with out ports,  *
        *the order does not matter!                    */
        .G_star (G_star[0]),
        .P_star (P_star[0]),
        .C (C[3:1]),
        .G (G[3:0]),
        .P (P[3:0]),
        .C0 (C[0]),
    ); 
    //instantiate BCLAUs 1-3 here (DONE)
    block_carry_lookahead_unit BCLAU1(
        .G_star (G_star[1]),
        .P_star (P_star[1]),
        .C (C[7:5]),
        .G (G[7:4]),
        .P (P[7:4]),
        .C0 (C[4]),
    );
    block_carry_lookahead_unit BCLAU2(
        .G_star (G_star[2]),
        .P_star (P_star[2]),
        .C (C[11:9]),
        .G (G[11:8]),
        .P (P[11:8]),
        .C0 (C[8]),
    );
    block_carry_lookahead_unit BCLAU3(
        .G_star (G_star[3]),
        .P_star (P_star[3]),
        .C (C[15:13]),
        .G (G[15:12]),
        .P (P[15:12]),
        .C0 (C[12]),
    );
    /*we will use the same form for this one too*/
    carry_lookahead_unit CLAU(
        /* we need to use some fancy             *
        *concatenation syntax to create the carry*
        * vector connected to this module        */
        .C ({C[16], C[12], C[8], C[4]}),
        .G (G_star),
        .P (P_star),
        .C0 (C[0]),
        //two lines are missing (NOT ANYMORE)
    );
    //instantiate the summation unit here 
    summation_unit SUM0(S, P, C[15:0]);
    assign Cout = C[16];

endmodule //fuckyes
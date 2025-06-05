`timescale 1ns / 1ps
`default_nettype none

/*This module describes the block carry-lookahead unit *
* for a 2-level carry-lookahead adder                  */
module block_carry_lookahead_unit(G_star, P_star, C, G, P, C0);

    /*ports are wires because we will use dataflow*/
    output wire G_star, P_star; //block generate and propagate
    output wire [3:1] C; //C3, C2, C1
    input wire [3:0] G, P; //generates and propagates
    input wire C0; //input carry

    .G_star (G_star[0]);
    
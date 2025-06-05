module Mux21 ( out , in , sel ) ;
  input [ 1 : 0 ] in ; //in[0] = a, in[1] = b
  input sel ; //select
  output out ; //out

  wire notsel;
  wire and1, and2;

  //not_sel
  not not_gate(notsel, sel);

  //AND gate for in[0] and notsel
  and and_gate1(and1, in[0], notsel);

  //AND in[1] and sel
  and and_gate2(and2, in[1], sel);

  // OR for output
  or or_gate(out, and1, and2);

endmodule

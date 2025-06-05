module Decode24 ( out , in ) ;
  input [ 1 : 0 ] in ;
  output reg [ 3 : 0 ] out ;
   

  always@(in)
    begin
    out = 4'b0000; //initialize output to 0
      if(in == 2'b00) //if the input is 00
        begin
          out = 4'b0001; //output is 0001
        end
      else if (in == 2'b01) //input is 01
        begin
          out = 4'b0010; //output is 0010
        end
      else if (in == 2'b10) // input is 10
        begin
          out = 4'b0100; // output is 0100
        end
      else if (in == 2'b11) //input is 11
        begin
          out = 4'b1000; //output is 1000
        end
  end
endmodule

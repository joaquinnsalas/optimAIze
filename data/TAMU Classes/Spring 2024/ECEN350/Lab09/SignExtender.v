// `timescale 1ns/1ps
// `default_nettype none 

module SignExtender(BusImm, Imm16, Ctrl); 
   output [63:0] BusImm; 
   input [25:0]  Imm16; 
   input [2:0]	 Ctrl; //For MOVZ
   reg[63:0] result; //We had to add this in to store the result

   always @(*) begin
	      case(Ctrl) //Cleaned up by removing begin and end clauses and simplifying down to one line of code per case
	   3'b000: //I-type
           begin
            result = {{52'b0}, Imm16[21:10]}; // Sign-extend from bit 21
           end
	   3'b001: //D-type data processing 
           begin
	      result = {{55{Imm16[20]}}, Imm16[20:12]};
           end
	   3'b010: //B-type
           begin
	      result = {{36{Imm16[25]}}, Imm16[25:0], 2'b00};
           end
	   3'b011: //BZ-type
           begin
	      result = {{43{Imm16[23]}}, Imm16[23:5], 2'b00};
           end
         3'b100: begin
            case (Imm16[22:21])
                  3'b00: begin
                        result = {{48{1'b0}}, Imm16[20:5]};
                  end
                  2'b01: begin
                        result = {{32{1'b0}}, Imm16[20:5],{16{1'b0}}};
                  end
                  2'b10: begin
                        result = {{16{1'b0}}, Imm16[20:5],{32{1'b0}}};
                  end
                  2'b11: begin
                        result = {Imm16[20:5], {48{1'b0}}};
                  end
            endcase
         end
      endcase
      end
      assign BusImm = result;
endmodule

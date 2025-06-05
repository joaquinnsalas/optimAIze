`timescale 1ns/1ps
`default_nettype none 

module SignExtender(BusImm, Imm16, Ctrl); 
   output reg [63:0] BusImm; 
   input [25:0]  Imm16; 
   input [1:0]	 Ctrl; 
   reg 	 extBit; 

   always@(*)
      begin
	case(Ctrl)
          
	   2'b00: //I-type
          begin
	     extBit = 0; //Since I-ype is unsigned extBit == 0
	     BusImm = {{52{extBit}}, Imm16[21:10]};
          end
	   2'b01: //D-type
          begin
	     extBit = Imm16[20];
	     BusImm = {{55{extBit}}, Imm16[20:12]};
          end
	   2'b10: //B-type
          begin
	     extBit = Imm16[25];
	     BusImm = {{36{extBit}}, Imm16[25:0],2'b00};
          end
	   2'b11: //BZ-type
          begin
	     extBit = Imm16[23];
	     BusImm = {{43{extBit}}, Imm16[23:5],2'b00};
          end
	endcase
      end
//   assign extBit = (Ctrl ? 1'b0 : Imm16[15]); 
//   assign BusImm = {{16{extBit}}, Imm16}; 
   
endmodule

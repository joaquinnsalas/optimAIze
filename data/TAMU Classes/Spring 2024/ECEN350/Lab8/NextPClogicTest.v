//THIS IS MY ALU TESTBENCH FILE, UPDATE IT ONCE NEXTPCLOGIC FILE HAS BEEN COMPLETED
`timescale 1ns / 1ps


`define STRLEN 15
module NextPClogicTest;
	initial begin
		$dumpfile("NextPClogicTest.vcd");
		$dumpvars(0, NextPClogicTest);
	end
	task passTest;
		input [63:0] actualOut, expectedOut;
		input [`STRLEN*8:0] testType;
		inout [7:0] passed;
	
		if(actualOut == expectedOut) begin $display ("%s passed", testType); passed = passed + 1; end
		else $display ("%s failed: %d should be %d", testType, actualOut, expectedOut);
	endtask
	
	task allPassed;
		input [14:0] passed;
		input [14:0] numTests;
		
		if(passed == numTests) $display ("All tests passed");
		else $display("Some tests failed");
	endtask
	
	// Inputs
    input [63:0] CurrentPC, SignExtImm64; 
    input 	Branch, ALUZero, Uncondbranch;
    input [7:0] passed;

	// Outputs
    wire [63:0] NextPC; 

	// Instantiate the Unit Under Test (UUT)
    NextPClogicTest uut (
        .CurrentPC(CurrentPC), 
        .SignExtImm64(SignExtImm64), 
        .Branch(Branch), 
        .ALUZero(ALUZero), 
        .Uncondbranch(Uncondbranch),
        .NextPC(NextPC)
    );

	initial begin
		// Initialize Inputs
		CurrentPC = 0;
		SignExtImm64 = 0;
        Branch = 0;
        ALUZero = 0;
        Uncondbranch = 0;
        passed = 0;

		// Add stimulus here
        $display("Something");
        #90; CurrentPC = 64'b0; SignExtImm64 = 64'b1; Branch =64'b0 ; ALUZero = 64'b1; Uncondbranch = 64 'b1; #10; passTest(NextPC, 64'b01, "Test 1", passed);
        // #90; CurrentPC= 64'b1; SignExtImm64 = 64'b1; Branch = ; #10; passTest(BusW, 64'b1, "Test 2", passed);
        // #90; CurrentPC = 64'b0; SignExtImm64 = 64'b1; Branch = ; #10; passTest(BusW, 64'b0, "Test 3", passed);

        // #90; CurrentPC = 64'b0; SignExtImm64 = 64'b1; ALUCtrl = `OR; #10; passTest(BusW, 64'b1, "Test 4", passed);
        // #90; CurrentPC = 64'b1; SignExtImm64 = 64'b1; ALUCtrl = `OR; #10; passTest(BusW, 64'b1, "Test 5", passed);
        // #90; CurrentPC = 64'b1; SignExtImm64 = 64'b0; ALUCtrl = `OR; #10; passTest(BusW, 64'b1, "Test 6", passed);

		allPassed(passed, 5);

        //15 total test

	end
      
endmodule

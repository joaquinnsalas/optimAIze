`timescale 1ns / 1ps


`define STRLEN 15
module ALUTest;
	initial begin
		$dumpfile("ALUTest.vcd");
		$dumpvars(0, ALUTest);
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
    reg [63:0] BusA, BusB;
    reg [3:0] ALUCtrl;
    reg [14:0] passed;

	// Outputs
    wire [63:0] BusW;
    wire Zero;

	// Instantiate the Unit Under Test (UUT)
    ALU uut (
        .BusW(BusW), 
        .BusA(BusA), 
        .BusB(BusB), 
        .ALUCtrl(ALUCtrl), 
        .Zero(Zero)
    );

	initial begin
		// Initialize Inputs
		BusA = 0;
		BusB = 0;
        ALUCtrl = 0;
        passed = 0;

		// Add stimulus here
        //AND
        #90; BusA = 64'b1; BusB = 64'b0; ALUCtrl = `AND; #10; passTest(BusW, 64'b0, "AND Test 1", passed);
        #90; BusA = 64'b1; BusB = 64'b1; ALUCtrl = `AND; #10; passTest(BusW, 64'b1, "AND Test 2", passed);
        #90; BusA = 64'b0; BusB = 64'b1; ALUCtrl = `AND; #10; passTest(BusW, 64'b0, "AND Test 3", passed);

        //OR
        #90; BusA = 64'b0; BusB = 64'b1; ALUCtrl = `OR; #10; passTest(BusW, 64'b1, "OR Test 4", passed);
        #90; BusA = 64'b1; BusB = 64'b1; ALUCtrl = `OR; #10; passTest(BusW, 64'b1, "OR Test 5", passed);
        #90; BusA = 64'b1; BusB = 64'b0; ALUCtrl = `OR; #10; passTest(BusW, 64'b1, "OR Test 6", passed);

        //ADD
        #90; BusA = 64'd10; BusB = 64'd20; ALUCtrl = `ADD; #10; passTest(BusW, 64'd30, "ADD Test 7", passed);
        #90; BusA = 64'd15; BusB = 64'd3; ALUCtrl = `ADD; #10; passTest(BusW, 64'd18, "ADD Test 8", passed);
        #90; BusA = 64'd34; BusB = 64'd43; ALUCtrl = `ADD; #10; passTest(BusW, 64'd77, "ADD Test 9", passed);

        //SUB
        #90; BusA = 64'd50; BusB = 64'd20; ALUCtrl = `SUB; #10; passTest(BusW, 64'd30, "SUB Test 10", passed);
        #90; BusA = 64'd400; BusB = 64'd200; ALUCtrl = `SUB; #10; passTest(BusW, 64'd200, "SUB Test 11", passed);
        #90; BusA = 64'd9; BusB = 64'd3; ALUCtrl = `SUB; #10; passTest(BusW, 64'd6, "SUB Test 12", passed);

        //PassB
        #90; BusA = 64'd0; BusB = 64'd123; ALUCtrl = `PassB; #10; passTest(BusW, 64'd123, "PassB Test 13", passed);
        #90; BusA = 64'd0; BusB = 64'd400; ALUCtrl = `PassB; #10; passTest(BusW, 64'd400, "PassB Test 14", passed);
        #90; BusA = 64'd0; BusB = 64'd200; ALUCtrl = `PassB; #10; passTest(BusW, 64'd200, "PassB Test 15", passed);

		allPassed(passed, 15);

        //15 total test

	end
      
endmodule

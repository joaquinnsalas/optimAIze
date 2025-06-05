module HalfAdd(A, B, Sum, Cout);
	input A, B;
	output Sum, Cout;
	wire notA, notB, AnotB, BnotA, AB; //wires for the SUM

	nand Carry(Carry, A, B);
	//A and B nand
	nand nand1(AB, A, B); //first NAND
	nand nand2(Cout, AB, AB); //Carry is NAND AB
	// sum output
	nand nand3(notA, A, A);     // notA
	nand nand4(notB, B, B);     // notB
	nand nand5(AnotB, notA, B); // A NAND (A NAND B)
	nand nand6(BnotA, A, notB); // B NAND (A NAND B)
	nand nand7(Sum, AnotB, BnotA);   // Sum is the NAND of the last 2 results
endmodule


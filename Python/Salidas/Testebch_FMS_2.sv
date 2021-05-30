`timescale 1ns/1ns

module FSM_Mealy_TB;

	reg Clk, Reset;
	reg X;
	wire outp;
	wire [2 : 0 ] Estado_Salida;

	FSM_Mealy UUT (.Clk(Clk), .Reset(Reset), .Estado_Salida(Estado_Salida), .X(X), .outp(outp));

	always #1 Clk = ~Clk;

initial begin
	$dumpfile("dump.vcd");
	$dumpvars(0, FSM_Mealy_TB);

	Clk <= 0;
$finish;
	end
endmodule
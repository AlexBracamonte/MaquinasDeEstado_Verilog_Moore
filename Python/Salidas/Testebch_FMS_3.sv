`timescale 1ns/1ns

module FSM_Mealy_TB;

	reg Clk, Reset;
	reg IN;
	wire Out_1;
	wire [2 : 0 ] Estado_Salida;

	FSM_Mealy UUT (.Clk(Clk), .Reset(Reset), .Estado_Salida(Estado_Salida), .IN(IN), .Out_1(Out_1));

	always #1 Clk = ~Clk;

initial begin
	$dumpfile("dump.vcd");
	$dumpvars(0, FSM_Mealy_TB);

	Clk <= 0;
$finish;
	end
endmodule
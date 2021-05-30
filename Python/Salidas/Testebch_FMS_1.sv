`timescale 1ns/1ns

module FSM_Mealy_TB;

	reg Clk, Reset;
	wire [2 : 0] output;
	wire [3 : 0 ] Estado_Salida;

	FSM_Mealy UUT (.Clk(Clk), .Reset(Reset), .Estado_Salida(Estado_Salida), .output(output));

	always #1 Clk = ~Clk;

initial begin
	$dumpfile("dump.vcd");
	$dumpvars(0, FSM_Mealy_TB);

	Clk <= 0;
$finish;
	end
endmodule
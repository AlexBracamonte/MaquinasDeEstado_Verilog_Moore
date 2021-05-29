`timescale 1ns/1ns

module FSM_TB;

reg clk;
reg rst;
reg X;

wire outp;

wire [2 : 0] Estado;


always #1 clk= ~{clk};

FSM UTT (.Estado(Estado), .clk(clk), .rst(rst), .X(X), .outp(outp));

initial
  begin
	$dumpfile("dump.vcd");
	$dumpvars(0,FSM_TB);
	clk <= 0;
	rst = 1;  #1


	//Agregar condiciones de verriciacion

	$finish;
  end
endmodule

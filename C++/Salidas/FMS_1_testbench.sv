`timescale 1ns/1ns

module FSM_TB;

reg clk;
reg rst;



	always #1 clk= ~{clk};

FSM UTT (.clk(clk), .rst(rst), .Out_1(Out_1));

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

module FSM_Mealy (Estado_Salida, Clk, Reset, output);

output reg [2 : 0] output;

input Clk, Reset;
output reg [3 : 0 ] Estado_Salida; // Salida para verificar estados 
reg [2 : 0] state, next_state;


assign Estado_Salida = state; 	 // Para verificar las salidas en el TB

parameter S0 = 3'b000;
parameter S1 = 3'b001;
parameter S2 = 3'b010;
parameter S3 = 3'b011;
parameter S4 = 3'b100;
parameter S5 = 3'b101;
parameter S6 = 3'b110;
parameter S7 = 3'b111;

always @ (posedge Clk or Reset)
  begin
	 if (Reset)
		 state <= S0;
	 else
		 state <= next_state;
  end


always @ (state)
  begin
	case(state)
		S0:
		  begin
			output= 0;
		  end
		S1:
		  begin
			output= 1;
		  end
		S2:
		  begin
			output= 2;
		  end
		S3:
		  begin
			output= 3;
		  end
		S4:
		  begin
			output= 4;
		  end
		S5:
		  begin
			output= 5;
		  end
		S6:
		  begin
			output= 6;
		  end
		S7:
		  begin
			output= 7;
		  end
	endcase
  end

always @ ( state)
  begin
	case (state)
		S0:
			next_state = S1;
		S1:
			next_state = S2;
		S2:
			next_state = S3;
		S3:
			next_state = S4;
		S4:
			next_state = S5;
		S5:
			next_state = S6;
		S6:
			next_state = S7;
		S7:
			next_state = S0;
		default: next_state = S0;
	endcase
  end
endmodule
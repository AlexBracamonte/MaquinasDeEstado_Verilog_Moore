module FSM_Mealy (Estado_Salida, Clk, Reset, X, outp);

input X;
output reg outp;

input Clk, Reset;
output reg [2 : 0 ] Estado_Salida; // Salida para verificar estados 
reg [1 : 0] state, next_state;


assign Estado_Salida = state; 	 // Para verificar las salidas en el TB

parameter S1 = 2'b00;
parameter S2 = 2'b01;
parameter S3 = 2'b10;
parameter S4 = 2'b11;

always @ (posedge Clk or Reset)
  begin
	 if (Reset)
		 state <= S1;
	 else
		 state <= next_state;
  end


always @ (state)
  begin
	case(state)
		S1:
		  begin
			outp= 1;
		  end
		S2:
		  begin
			outp= 1;
		  end
		S3:
		  begin
			outp= 0;
		  end
		S4:
		  begin
			outp= 0;
		  end
	endcase
  end

always @ (X or  state)
  begin
	case (state)
		S1:
		  begin
			if ( X == 0  )
			  begin
				next_state = S3;
			  end
			if ( X == 1  )
			  begin
				next_state = S2;
			  end
		  end
		S2:
			next_state = S4;
		S3:
			next_state = S4;
		S4:
			next_state = S1;
		default: next_state = S1;
	endcase
  end
endmodule
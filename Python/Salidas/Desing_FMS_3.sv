module FSM_Mealy (Estado_Salida, Clk, Reset, IN, Out_1);

input IN;
output reg Out_1;

input Clk, Reset;
output reg [2 : 0 ] Estado_Salida; // Salida para verificar estados 
reg [1 : 0] state, next_state;


assign Estado_Salida = state; 	 // Para verificar las salidas en el TB

parameter A = 2'b00;
parameter B = 2'b01;
parameter C = 2'b10;
parameter D = 2'b11;

always @ (posedge Clk or Reset)
  begin
	 if (Reset)
		 state <= A;
	 else
		 state <= next_state;
  end


always @ (state)
  begin
	case(state)
		A:
		  begin
			Out_1= 0;
		  end
		B:
		  begin
			Out_1= 0;
		  end
		C:
		  begin
			Out_1= 0;
		  end
		D:
		  begin
			Out_1= 1;
		  end
	endcase
  end

always @ (IN or  state)
  begin
	case (state)
		A:
		  begin
			if ( IN == 0  )
			  begin
				next_state = A;
			  end
			if ( IN == 1  )
			  begin
				next_state = B;
			  end
		  end
		B:
		  begin
			if ( IN == 1  )
			  begin
				next_state = B;
			  end
			if ( IN == 0  )
			  begin
				next_state = C;
			  end
		  end
		C:
		  begin
			if ( IN == 0  )
			  begin
				next_state = A;
			  end
			if ( IN == 1  )
			  begin
				next_state = D;
			  end
		  end
		D:
		  begin
			if ( IN == 0  )
			  begin
				next_state = C;
			  end
			if ( IN == 1  )
			  begin
				next_state = B;
			  end
		  end
		default: next_state = A;
	endcase
  end
endmodule
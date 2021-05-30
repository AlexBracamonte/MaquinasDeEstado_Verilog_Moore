module FSM_Mealy (Estado_Salida, Clk, Reset, IN, Rojo, Verde, Amarillo, Pasar_Persona);

input IN;
output reg Rojo;
output reg Verde;
output reg Amarillo;
output reg Pasar_Persona;

input Clk, Reset;
output reg [3 : 0 ] Estado_Salida; // Salida para verificar estados 
reg [2 : 0] state, next_state;


assign Estado_Salida = state; 	 // Para verificar las salidas en el TB

parameter S0 = 3'b000;
parameter S1 = 3'b001;
parameter S2 = 3'b010;
parameter S3 = 3'b011;
parameter S4 = 3'b100;

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
			Rojo= 1;
			Verde= 0;
			Amarillo= 0;
			Pasar_Persona= 0;
		  end
		S1:
		  begin
			Rojo= 0;
			Verde= 0;
			Amarillo= 1;
			Pasar_Persona= 0;
		  end
		S2:
		  begin
			Rojo= 0;
			Verde= 1;
			Amarillo= 0;
			Pasar_Persona= 0;
		  end
		S3:
		  begin
			Rojo= 1;
			Verde= 0;
			Amarillo= 0;
			Pasar_Persona= 1;
		  end
		S4:
		  begin
			Rojo= 1;
			Verde= 0;
			Amarillo= 1;
			Pasar_Persona= 0;
		  end
	endcase
  end

always @ (IN or  state)
  begin
	case (state)
		S0:
		  begin
			if ( IN == 0  )
			  begin
				next_state = S1;
			  end
			if ( IN == 1  )
			  begin
				next_state = S3;
			  end
		  end
		S1:
		  begin
			if ( IN == 0  )
			  begin
				next_state = S2;
			  end
			if ( IN == 1  )
			  begin
				next_state = S3;
			  end
		  end
		S2:
		  begin
			if ( IN == 0  )
			  begin
				next_state = S0;
			  end
			if ( IN == 1  )
			  begin
				next_state = S3;
			  end
		  end
		S3:
			next_state = S4;
		S4:
			next_state = S0;
		default: next_state = S0;
	endcase
  end
endmodule
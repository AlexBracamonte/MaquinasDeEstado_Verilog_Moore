module FSM_Mealy (Estado_Salida, Clk, Reset, IN, Led);

input IN;
output reg Led;

input Clk, Reset;
output reg [1 : 0 ] Estado_Salida; // Salida para verificar estados 
reg [0 : 0] state, next_state;


assign Estado_Salida = state; 	 // Para verificar las salidas en el TB

parameter Apagado = 1'b0;
parameter Encendido = 1'b1;

always @ (posedge Clk or Reset)
  begin
	 if (Reset)
		 state <= Apagado;
	 else
		 state <= next_state;
  end


always @ (state)
  begin
	case(state)
		Apagado:
		  begin
			Led= 0;
		  end
		Encendido:
		  begin
			Led= 1;
		  end
	endcase
  end

always @ (IN or  state)
  begin
	case (state)
		Apagado:
		  begin
			if ( IN == 1  )
			  begin
				next_state = Encendido;
			  end
			if ( IN == 0  )
			  begin
				next_state = Apagado;
			  end
		  end
		Encendido:
		  begin
			if ( IN == 1  )
			  begin
				next_state = Encendido;
			  end
			if ( IN == 0  )
			  begin
				next_state = Apagado;
			  end
		  end
		default: next_state = Apagado;
	endcase
  end
endmodule
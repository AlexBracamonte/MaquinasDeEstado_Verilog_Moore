module FSM(Estado, clk, rst, IN, Led);

	input clk;
	input rst;
	input IN;

	output reg Led;


	parameter Apagado = 1'b0;
	parameter Encendido = 1'b1;

output reg [1 : 0] Estado;

assign Estado = state;
	
reg [1 : 0] state, next_state;

always @ (posedge clk or rst)
  begin
	if (rst)
		state <= Apagado;
	else
		state <= next_state;
  end

always @ (IN or state)
  begin
	case (state)
		Apagado:
		  begin
			 if( IN == 1 )
			  begin
				next_state = Encendido;
			  end

			 if( IN == 0 )
			  begin
				next_state = Apagado;
			  end

		  end

		Encendido:
		  begin
			 if( IN == 1 )
			  begin
				next_state = Encendido;
			  end

			 if( IN == 0 )
			  begin
				next_state = Apagado;
			  end

		  end

		default: next_state = Apagado;
	endcase

  end


always @ (state)
  begin
	case(state)
		Apagado:
		  begin
			Led= 1;
		  end
		Encendido:
		  begin
			Led= 0;
		  end
		default:
		  begin
			Led= 'bz;
		  end
	endcase

  end


endmodule

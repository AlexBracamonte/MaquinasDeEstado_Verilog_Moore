module FSM(Estado, clk, rst, IN, Rojo, Verde, Amarillo, Pasar_Persona);

	input clk;
	input rst;
	input IN;

	output reg Rojo;
	output reg Verde;
	output reg Amarillo;
	output reg Pasar_Persona;


	parameter S0 = 3'b000;
	parameter S1 = 3'b001;
	parameter S2 = 3'b010;
	parameter S3 = 3'b011;
	parameter S4 = 3'b100;

output reg [3 : 0] Estado;

assign Estado = state;
	
reg [3 : 0] state, next_state;

always @ (posedge clk or rst)
  begin
	if (rst)
		state <= S0;
	else
		state <= next_state;
  end

always @ (IN or state)
  begin
	case (state)
		S0:
		  begin
			 if( IN == 0 )
			  begin
				next_state = S1;
			  end

			 if( IN == 1 )
			  begin
				next_state = S3;
			  end

		  end

		S1:
		  begin
			 if( IN == 0 )
			  begin
				next_state = S2;
			  end

			 if( IN == 1 )
			  begin
				next_state = S3;
			  end

		  end

		S2:
		  begin
			 if( IN == 0 )
			  begin
				next_state = S0;
			  end

			 if( IN == 1 )
			  begin
				next_state = S3;
			  end

		  end

		S3:
		  begin
			 if( 1)
			  begin
				next_state = S4;
			  end

		  end

		S4:
		  begin
			 if( 1)
			  begin
				next_state = S0;
			  end

		  end

		default: next_state = S0;
	endcase

  end


always @ (state)
  begin
	case(state)
		S0:
		  begin
			Rojo= 1;
			Verde=  0;
			Amarillo=  0;
			Pasar_Persona=  0;
		  end
		S1:
		  begin
			Rojo= 0;
			Verde=  0;
			Amarillo=  1;
			Pasar_Persona=  0;
		  end
		S2:
		  begin
			Rojo= 0;
			Verde=  1;
			Amarillo=  0;
			Pasar_Persona=  0;
		  end
		S3:
		  begin
			Rojo= 1;
			Verde=  0;
			Amarillo=  0;
			Pasar_Persona=  1;
		  end
		S4:
		  begin
			Rojo= 1;
			Verde=  0;
			Amarillo=  1;
			Pasar_Persona=  0;
		  end
		default:
		  begin
			Rojo= 'bz;
			Verde= 'bz;
			Amarillo= 'bz;
			Pasar_Persona= 'bz;
		  end
	endcase

  end


endmodule

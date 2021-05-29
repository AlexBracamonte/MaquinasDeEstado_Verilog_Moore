module FSM(Estado, clk, rst, X, outp);

	input clk;
	input rst;
	input X;

	output reg outp;


	parameter S1 = 2'b00;
	parameter S2 = 2'b01;
	parameter S3 = 2'b10;
	parameter S4 = 2'b11;

output reg [2 : 0] Estado;

assign Estado = state;
	
reg [2 : 0] state, next_state;

always @ (posedge clk or rst)
  begin
	if (rst)
		state <= S1;
	else
		state <= next_state;
  end

always @ (X or state)
  begin
	case (state)
		S1:
		  begin
			 if( X == 0 )
			  begin
				next_state = S3;
			  end

			 if( X == 1 )
			  begin
				next_state = S2;
			  end

		  end

		S2:
		  begin
			 if( 1)
			  begin
				next_state = S4;
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
				next_state = S1;
			  end

		  end

		default: next_state = S1;
	endcase

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
		default:
		  begin
			outp= 'bz;
		  end
	endcase

  end


endmodule

module FSM(Estado, clk, rst, IN, Out_1);

	input clk;
	input rst;
	input IN;

	output reg Out_1;


	parameter A = 2'b00;
	parameter B = 2'b01;
	parameter C = 2'b10;
	parameter D = 2'b11;

output reg [2 : 0] Estado;

assign Estado = state;
	
reg [2 : 0] state, next_state;

always @ (posedge clk or rst)
  begin
	if (rst)
		state <= A;
	else
		state <= next_state;
  end

always @ (IN or state)
  begin
	case (state)
		A:
		  begin
			 if( IN == 0 )
			  begin
				next_state = A;
			  end

			 if( IN == 1 )
			  begin
				next_state = B;
			  end

		  end

		B:
		  begin
			 if( IN == 1 )
			  begin
				next_state = B;
			  end

			 if( IN == 0 )
			  begin
				next_state = C;
			  end

		  end

		C:
		  begin
			 if( IN == 0 )
			  begin
				next_state = A;
			  end

			 if( IN == 1 )
			  begin
				next_state = D;
			  end

		  end

		D:
		  begin
			 if( IN == 0 )
			  begin
				next_state = C;
			  end

			 if( IN == 1 )
			  begin
				next_state = B;
			  end

		  end

		default: next_state = A;
	endcase

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
		default:
		  begin
			Out_1= 'bz;
		  end
	endcase

  end


endmodule

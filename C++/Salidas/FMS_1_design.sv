module FSM(clk, rst, Out_1);

	input clk;
	input rst;

	output reg [4 : 0] Out_1;


	parameter S0 = 4'b0000;
	parameter S1 = 4'b0001;
	parameter S2 = 4'b0010;
	parameter S3 = 4'b0011;
	parameter S4 = 4'b0100;
	parameter S5 = 4'b0101;
	parameter S6 = 4'b0110;
	parameter S7 = 4'b0111;
	parameter S8 = 4'b1000;
	parameter S9 = 4'b1001;
	parameter S10 = 4'b1010;
	parameter S11 = 4'b1011;
	parameter S12 = 4'b1100;
	
reg [4 : 0] state, next_state;

always @ (posedge clk or rst)
  begin
	if (rst)
		state <= S0;
	else
		state <= next_state;
  end

always @ (state)
  begin
	case (state)
		S0:
		  begin
			next_state = S1;
		  end

		S1:
		  begin
			next_state = S2;
		  end

		S2:
		  begin
			next_state = S3;
		  end

		S3:
		  begin
			next_state = S4;
		  end

		S4:
		  begin
			next_state = S5;
		  end

		S5:
		  begin
			next_state = S6;
		  end

		S6:
		  begin
			next_state = S7;
		  end

		S7:
		  begin
			next_state = S8;
		  end

		S8:
		  begin
			next_state = S9;
		  end

		S9:
		  begin
			next_state = S10;
		  end

		S10:
		  begin
			next_state = S11;
		  end

		S11:
		  begin
			next_state = S12;
		  end

		S12:
		  begin
			next_state = S0;
		  end

		default: next_state = S0;
	endcase

  end


always @ (state)
  begin
	case(state)
		S0:
		  begin
			Out_1= 0;
		  end
		S1:
		  begin
			Out_1= 1;
		  end
		S2:
		  begin
			Out_1= 2;
		  end
		S3:
		  begin
			Out_1= 3;
		  end
		S4:
		  begin
			Out_1= 4;
		  end
		S5:
		  begin
			Out_1= 5;
		  end
		S6:
		  begin
			Out_1= 6;
		  end
		S7:
		  begin
			Out_1= 7;
		  end
		S8:
		  begin
			Out_1= 8;
		  end
		S9:
		  begin
			Out_1= 9;
		  end
		S10:
		  begin
			Out_1= 10;
		  end
		S11:
		  begin
			Out_1= 11;
		  end
		S12:
		  begin
			Out_1= 12;
		  end
		default:
		  begin
			Out_1= 'bz;
		  end
	endcase

  end


endmodule

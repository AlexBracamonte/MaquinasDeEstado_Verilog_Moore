#include <iostream>
#include <vector>


//---------------------------------------------------------------- Librerias creadas por nosotros
#include "clases.h"


//------------------------------ Algo nuestro
using namespace std;

//---------------------------------------------------------------------------------------



int main(int argc, char *argv[])
{
    string file = "FMS_5";
    string config = "Salidas/" + file + ".txt";
    string design = "Salidas/" + file + "_design.sv";
    string testbench = "Salidas/" + file + "_testbench.sv";


    python(file);
    
    cout << "******************" << endl
         << "*   Esto es C++  *" << endl
         << "******************" << endl;


    Moore FSM(config, testbench, design);
    FSM.abrir_archivo();
    FSM.config_variables_inputs();
    FSM.config_variables_outputs();
    FSM.config_variables_states();
    FSM.config_conditions();
    FSM.config_output_values();
    FSM.write_design();
    FSM.write_test();

    system("pause");
    return 0;
}
//----------------------------------------------------------------------------------------
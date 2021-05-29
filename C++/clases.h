#ifndef __CLASES_H__
#define __CLASES_H__

#include <iostream>
#include <string>
#include <fstream>
#include <math.h>
#include <bitset>
#include <vector>
#include <cstring>

//-------------------------------------------------------------
#define MAX_BITS 32

//----------------------------------------------------------------------



//----------------------------------------------------------------------

using namespace std;

void python(string excel = "Algo", string salida = "Otra cosa");
vector<string> string_to_vector(string str);

//-----------------------------------------
void python(string excel, string salida)
{
    cout << endl
         << "**************" << endl
         << "    python" << endl
         << endl
         << "**************" << endl;
    try
    {
        system("mkdir Salidas  > Salidas/info.txt");
        cout << "Se creo una carpeta Salidas" << endl
             << endl;
        system("pip install pandas");
        system("pip install xlrd");
        system("pip install openpyxl");

        cout << endl
             << "********** Salidas de Python *************" << endl
             << endl;

        string cmd;
        cmd = "python LeerExcel.py Tablas/" + excel + ".xlsx" + " Salidas/" + excel;
        string cmd2 = "python LeerExcel.py Tablas/FMS_1.xlsx Salidas/FSM_1";
        int n = cmd.length();
        char comando[n + 1];

        strcpy(comando, cmd.c_str());
        cout << endl
             << "Comando: " << comando << endl
             << endl;
        system(comando);
    }
    catch (...)
    {
        cout << "ERROR" << endl;
    }
}

vector <string> string_to_vector(string str)
{
    str += ',';
    vector<string> valores;
    string aux = "";
    for (int i = 0; i < str.length(); i++)
    {
        if (str[i] == ',')
        {
            valores.push_back(aux);
            aux = "";
        }
        else
        {
            aux += str[i];
        }
    }
    return valores;
}

//----------------------------------------- Clases ----------------------------------------------------------------

class Moore
{
private:
    string Nombre_Design;
    string Nombre_Testbench;

    string Nombre_Modulo;
    string Nombre_Variables;
    string Nombre_Doc_in;

    int bits_estados;

public:
    Moore(string in = "Salidas/Design_Alex.txt", string out_test = "Salidas/Testbench_Alex.sv", string out_design = "Salidas/Design_Alex.sv", string mod = "FSM");
    ~Moore();

    void write_testbench(void);
    void abrir_archivo(void);

    void config_variables_inputs(void);
    void config_variables_outputs(void);
    void config_variables_states(void);
    void config_conditions(void);
    void config_output_values(void);

    void write_design(void);
    void write_test(void);

    vector<string> clk_reset; // VAriables de entrada
    vector<string> inputs;    // VAriables de entrada           // {a, b, c}
    vector<int> inputs_size;  // TAmaño de bits de entrada      // {1, 10, 2}

    vector<string> outputs;        // Variable de Salidas
    vector<int> outputs_size;      // Tamaño de bits de salida  {q1, q2. q3}
    vector<string> outputs_values; // VAriables de entrada  {"1, 2, 4",  "0, 0 0", ......}

    vector<string> states;  // VAriables de entrada
    vector<int> states_num; // Tamaño de bits de salida

    vector<string> condiciones;   // VAriables de entrada  ["x=1, y= 10,"]
    vector<string> edo_actual;    // Estado actul
    vector<string> edo_siguiente; // VAriables de entrada
};

Moore::Moore(string in, string out_test, string out_design, string mod)
{
    cout << "***********************" << endl
         << "     Constructor       " << endl
         << "***********************" << endl;

    Nombre_Design = out_design;
    Nombre_Testbench = out_test;
    Nombre_Variables = in;
    Nombre_Modulo = mod;

    clk_reset = {"clk", "rst"};
}

Moore::~Moore()
{
}

void Moore::abrir_archivo(void)
{
    cout << "***********************" << endl
         << "     Abrir Archivo     " << endl
         << "***********************" << endl;

    cout << "EL archivo se encuentra en " << Nombre_Variables << endl;

    string lineas;
    ifstream file; // Se crea el objeto fichero design

    int bandera = 0;

    try
    {
        file.open(Nombre_Variables);

        if (file)
        {
            while (getline(file, lineas))
            {

                if ((lineas == "---"))
                {
                    cout << "************************" << endl;
                    bandera++;
                }
                switch (bandera) //donde opción es la variable a comparar
                {
                case 1: //Bloque de instrucciones 1;
                {
                    inputs.push_back(lineas);       // x=3;
                    break;
                }
                case 2: //Bloque de instrucciones 1;
                {
                    outputs.push_back(lineas);
                    break;
                }
                case 3: //Bloque de instrucciones 1;
                {
                    states.push_back(lineas);
                    break;
                }
                case 4: //Bloque de instrucciones 1;
                {
                    condiciones.push_back(lineas);
                    break;
                }
                case 5:
                {
                    outputs_values.push_back(lineas);  // 
                    break;
                }
                default:
                    break; //Bloque de instrucciones por defecto;
                           //default, es el bloque que se ejecuta en caso de que no se de ningún caso
                }
                cout << "Una línea: ";
                cout << lineas << " --- " << endl;
            }
            for (auto valor : outputs_values)
            {
                cout << "VAlor en ese lugar " << valor << endl;
            }
        }
        else
        {
            cout << "No se pudo abrir el archivo: " << Nombre_Variables << "'" << endl;
            cout << "Es probable que el documento no exista, o no este en la misma carpeta" << endl;
        }
    }
    catch (...)
    {
        cerr << "No se pudo abrir el archivo" << Nombre_Variables << "'" << endl;
        cout << "No se pudo abrir el archivo" << Nombre_Variables << "'" << endl;
    }
}

void Moore::config_variables_inputs(void)
{
    cout << "***********************" << endl
         << "    Config_Entradas     " << endl
         << "***********************" << endl;
    vector<string> auxiliar = inputs;
    inputs.clear();
    for (auto entrada : auxiliar)  
    {
        // cout << "El valor es " << entrada << endl;
        if (entrada.find("=") != string::npos)
        {
            // cout << "Solo " << entrada << " contiene" << endl;
            int bandera_input = 0;
            string aux = "";
            for (int i = 0; i < entrada.length(); i++)
            {
                if (entrada[i] == '=')
                {
                    bandera_input = 1;
                    cout << "Lo que consegui en " << entrada << " fue " << aux << endl;
                    inputs.push_back(aux);
                    aux = "";
                }
                if (entrada[i] == ';')
                {
                    bandera_input = 2;
                    cout << "La otra parte para " << entrada << " es " << aux << endl;
                    int numero_bits;
                    numero_bits = atoi(aux.c_str());
                    inputs_size.push_back(numero_bits);

                    aux = "";
                }
                if (bandera_input == 0)
                {
                    aux += entrada[i];
                }
                if (!(entrada[i] == '='))
                {
                    if (bandera_input == 1)
                        aux += entrada[i];
                }
            }
        }
    }
    for (auto valor : inputs)
    {
        cout << "Inputs: " << valor << endl;
    }
    for (auto valor : inputs_size)
    {
        cout << "Bits: " << valor << endl;
    }
}

void Moore::config_variables_outputs(void)
{
    cout << "***********************" << endl
         << "    Config_Salidas     " << endl
         << "***********************" << endl;
    vector<string> auxiliar = outputs;
    outputs.clear();
    for (auto entrada : auxiliar)
    {
        // cout << "El valor es " << entrada << endl;
        if (entrada.find("=") != string::npos)
        {
            // cout << "Solo " << entrada << " contiene" << endl;
            int bandera_input = 0;
            string aux = "";
            for (int i = 0; i < entrada.length(); i++)
            {
                if (entrada[i] == '=')
                {
                    bandera_input = 1;
                    cout << "Lo que consegui en " << entrada << " fue " << aux << endl;
                    outputs.push_back(aux);
                    aux = "";
                }
                if (entrada[i] == ';')
                {
                    bandera_input = 2;
                    cout << "La otra parte para " << entrada << " es " << aux << endl;
                    int numero_bits;
                    numero_bits = atoi(aux.c_str());
                    outputs_size.push_back(numero_bits);

                    aux = "";
                }
                if (bandera_input == 0)
                {
                    aux += entrada[i];
                }
                if (!(entrada[i] == '='))
                {
                    if (bandera_input == 1)
                        aux += entrada[i];
                }
            }
        }
    }
    for (auto valor : outputs)
    {
        cout << "Outputs: " << valor << endl;
    }
    for (auto valor : outputs_size)
    {
        cout << "Bits: " << valor << endl;
    }
}

void Moore::config_variables_states(void)
{
    cout << endl
         << endl
         << "***********************" << endl
         << "    Config_States    " << endl
         << "***********************" << endl;
    vector<string> auxiliar = states;
    states.clear();
    for (auto entrada : auxiliar)
    {
        // cout << "El valor es " << entrada << endl;
        if (entrada.find("=") != string::npos)
        {
            // cout << "Solo " << entrada << " contiene" << endl;
            int bandera_input = 0;
            string aux = "";
            for (int i = 0; i < entrada.length(); i++)
            {
                if (entrada[i] == '=')
                {
                    bandera_input = 1;
                    cout << "Lo que consegui en " << entrada << " fue " << aux << endl;
                    states.push_back(aux);
                    aux = "";
                }
                if (entrada[i] == ';')
                {
                    bandera_input = 2;
                    cout << "La otra parte para " << entrada << " es " << aux << endl;
                    int numero_bits;
                    numero_bits = atoi(aux.c_str());
                    states_num.push_back(numero_bits);

                    aux = "";
                }
                if (bandera_input == 0)
                {
                    aux += entrada[i];
                }
                if (!(entrada[i] == '='))
                {
                    if (bandera_input == 1)
                        aux += entrada[i];
                }
            }
        }
    }
    for (auto valor : states)
    {
        cout << "State: " << valor << endl;
    }
    for (auto valor : states_num)
    {
        cout << "Bits: " << valor << endl;
    }
}

void Moore::config_conditions(void)
{
    cout << endl
         << endl
         << "***********************" << endl
         << "    Conditions    " << endl
         << "***********************" << endl;
    vector<string> auxiliar = condiciones;
    condiciones.clear();

    for (auto entrada : auxiliar)
    {
        // cout << "Lo que se encuentra en condiciones es " << entrada << endl;
        if (entrada.find("=") != string::npos)
        {
            // cout << "Se encontro algo en -- = -- " << entrada << endl;
            if (entrada.find("Actual") != string::npos)
            {
                int inicio = entrada.find('=');
                int fin = entrada.find(';');
                string aux2 = entrada.substr((inicio + 1), (fin - inicio - 1));
                cout << "La entrada actual es: " << aux2 << endl;
                edo_actual.push_back(aux2);
            }

            if (entrada.find("Siguiente") != string::npos)
            {
                int inicio = entrada.find('=');
                int fin = entrada.find(';');
                string aux2 = entrada.substr((inicio + 1), (fin - inicio - 1));
                cout << "La siguiente: " << aux2 << endl;
                edo_siguiente.push_back(aux2);
            }

            if (entrada.find("Condiciones") != string::npos)
            {
                int inicio = entrada.find('[');
                int fin = entrada.find(']');
                string aux2 = entrada.substr((inicio + 1), (fin - inicio - 1));
                for (int i = 0; i < aux2.size(); i++) // Eliminar espacios en blanco
                {
                    if (aux2[i] == ' ')
                    {
                        aux2.erase(i, 1);
                        i--;
                    }
                    if (aux2[i] == '\'')
                    {
                        aux2.erase(i, 1);
                        i--;
                    }
                }
                condiciones.push_back(aux2);
                cout << "La Condicion es: " << aux2 << endl;
            }
        }
    }
}

void Moore::config_output_values(void)
{
    cout << endl
         << endl
         << "***********************" << endl
         << "Config_Values_Of_Outputs    " << endl
         << "***********************" << endl;

    vector<string> auxiliar = outputs_values;
    outputs_values.clear();

    for (auto valor : auxiliar)
    {
        //cout << "Los valores de salidas son: " << valor << endl;
        if (valor.find("=") != string::npos)
        {
            // cout << "Se encontro algo en -- = -- " << entrada << endl;

            int inicio = valor.find('[');
            int fin = valor.find(']');
            string aux2 = valor.substr((inicio + 1), (fin - inicio - 1));
            cout << "Los valores de la salida son: " << aux2 << endl;
            outputs_values.push_back(aux2);
        }
    }
}

void Moore::write_design(void)
{
    cout << endl
         << "***********************" << endl
         << "       Design       " << endl
         << "***********************" << endl
         << endl;

    ofstream sv; // objeto de la clase ofstream
    sv.open(Nombre_Design);

    float res = states.size();
    int num_bits = 0; ////num de bits para las combinaciones

    //cout<<"Res "<< res<<endl;
    while (res > 1)
    {
        res = res / 2;
        num_bits += 1;
    }
    bits_estados = num_bits;

    if (!sv)
    {
        cout << "No se pudoa abrir el archivo: " << Nombre_Design << endl;
    }
    if (sv)
    {
        string aux = "";
        for (auto valor : clk_reset)
        {
            aux += valor + ", ";
        }
        for (auto valor : inputs)
        {
            aux += valor + ", ";
        }
        for (auto valor : outputs)
        {
            aux += valor + ", ";
        }
        aux.pop_back();
        aux.pop_back();

        sv << "module " + Nombre_Modulo + "(Estado, " + aux + ");" << endl
           << endl;

        for (auto valor : clk_reset)
        {
            sv << "\tinput " << valor << ";" << endl;
        }

        for (int i = 0; i < inputs.size(); i++)
        {
            if (inputs_size[i] == 1)
            {
                sv << "\tinput " << inputs[i] << ";" << endl;
            }
            else
            {
                sv << "\tinput "
                   << "[" << (inputs_size[i] - 1) << " : 0] " << inputs[i] << ";" << endl;
            }
        }

        sv << endl; // Pasamos a las salidas
        for (int i = 0; i < outputs.size(); i++)
        {
            if (outputs_size[i] == 1)
            {
                sv << "\toutput reg " << outputs[i] << ";" << endl;
            }
            else
            {
                sv << "\toutput reg "
                   << "[" << (outputs_size[i] - 1) << " : 0] " << outputs[i] << ";" << endl;
            }
        }
        sv << endl
           << endl;


        //--------------------------------------------------------------------------- Estados.
        for (int i = 0; i < states.size(); i++)
        {
            bitset<MAX_BITS> bs2(i);
            string aux = "";
            for (int i = 0; i < num_bits; i++)
            { //solo guarda cantidad de digitos necesarios para las combinaciones
                aux += to_string(bs2[i]);
            }
            string aux_r; /////Voltea valores en binario de 100 -> 001
            aux_r.resize(aux.size());
            copy(aux.rbegin(), aux.rend(), aux_r.begin());

            sv << "\tparameter " << states[i] << " = " << num_bits << "'b" << aux_r << ";" << endl;
        }

        sv << endl << "output reg " << "[" << bits_estados << " : 0] " << "Estado;" << endl << endl;
        sv << "assign Estado = state;" << endl;

        sv << "\t\nreg " << "[" << num_bits << " : 0] " << "state, next_state;" << endl;

        //------------- Estado inicial
        sv << "\n"
           << "always @ (posedge " << clk_reset[0] << " or " << clk_reset[1] << ")" << endl
           << "  begin" << endl
           << "\tif (" << clk_reset[1] << ")" << endl
           << "\t\tstate <= " << states[0] << ";" << endl
           << "\telse" << endl
           << "\t\tstate <= next_state;" << endl
           << "  end" << endl
           << endl;

        //------------ Condiciones
        aux = "";
        for (auto valor : inputs)
        {
            aux += valor + " or ";
        }
        sv << "always @ (" << aux << "state)" << endl
           << "  begin" << endl
           << "\tcase (state)" << endl;

        for (auto estado : states)
        {
            sv << "\t\t" << estado << ":" << endl
               << "\t\t  begin" << endl;

            string algo = "";
            algo.length();

            for (int i = 0; i < edo_actual.size(); i++) // Recorremos todo el vector de estados actuales
            {
                if (edo_actual[i] == estado) // Comparamos con el estado actual
                {
                    if (condiciones[i].length() == 0) // Si la condiciones "" se agrega sin condiciones
                    {
                        sv << "\t\t\tnext_state = " << edo_siguiente[i] << ";" << endl;
                    }
                    else
                    {
                        vector<string> vec_aux;
                        vec_aux = string_to_vector(condiciones[i]);
                        string condiciones_valores = "";
                        for (int i = 0; i < vec_aux.size(); i++)
                        {
                            if (!(vec_aux[i] == "X"))
                            {
                                if (!(vec_aux[i] == "x"))
                                {
                                    condiciones_valores += inputs[i] + " == " + vec_aux[i] + " & ";
                                }
                            }
                        }
                        if(condiciones_valores.size() > 2)
                        {
                            condiciones_valores.pop_back();
                            condiciones_valores.pop_back();
                        }
                        else
                        {
                            condiciones_valores = "1";
                        }
                        
                        // cout << "VOy a imprimir un " << condiciones_valores << endl;
                        sv << "\t\t\t if( " << condiciones_valores << ")" << endl
                           << "\t\t\t  begin" << endl
                           << "\t\t\t\tnext_state = " << edo_siguiente[i] << ";" << endl
                           << "\t\t\t  end\n"
                           << endl;
                    }
                }
            }
            sv << "\t\t  end" << endl
               << endl;
        }
        sv << "\t\tdefault: next_state = " << states[0] << ";" << endl;
        sv << "\tendcase\n\n"
           << "  end\n"
           << endl
           << endl;

        sv << "always @ (state)" << endl
           << "  begin" << endl
           << "\tcase(state)" << endl;

        for (int i = 0; i < states.size(); i++)
        {
            sv << "\t\t" << states[i] << ":" << endl
               << "\t\t  begin" << endl;

            vector<string> vec_aux;
            vec_aux = string_to_vector(outputs_values[i]);

            for (int index = 0; index < vec_aux.size(); index++)
            {
                sv << "\t\t\t" << outputs[index] << "= " << vec_aux[index] << ";" << endl;
            }

            sv << "\t\t  end" << endl;
        }
        sv << "\t\tdefault:" << endl
           << "\t\t  begin" << endl;

        for (int index = 0; index < outputs.size(); index++)
        {
            sv << "\t\t\t" << outputs[index] << "= "
               << "'bz;" << endl;
        }
        sv << "\t\t  end" << endl;

        sv << "\tendcase\n\n"
           << "  end\n\n\n"
           << "endmodule" << endl;
    }
}

void Moore::write_test(void)
{
    cout << endl
         << "***********************" << endl
         << "       Testbench       " << endl
         << "***********************" << endl
         << endl;

    ofstream test; // objeto de la clase ofstream
    test.open(Nombre_Testbench);
    if (!test)
    {
        cout << "No se pudoa abrir el archivo: " << Nombre_Testbench << endl;
    }
    if (test)
    {
        string aux; // VAriable auxiliar

        cout << "Se pudo abrir el archivo: " << Nombre_Testbench << endl;

        test << "`timescale 1ns/1ns" << endl
             << endl;
        test << "module " + Nombre_Modulo + "_TB;" << endl
             << endl;

        // ------------------------------------------ Escribe el reg
        for (auto valor : clk_reset)
        {
            test << "reg " << valor << ";" << endl;
        }
        for (int i = 0; i < inputs.size(); i++)
        {
            test << "reg ";
            if (inputs_size[i] == 1)
            {
                test << inputs[i] << ";" << endl;
            }
            else
            {
                test << "[" << (inputs_size[i] - 1) << ": 0] " << inputs[i] << ";" << endl;
            }
        }
        test << endl;

        // ------------------------------------------ Escribe el wire
        for (int i = 0; i < outputs.size(); i++)
        {
            test << "wire ";
            if (outputs_size[i] == 1)
            {
                test << outputs[i] << ";" << endl;
            }
            else
            {
                test << "[" << (outputs_size[i] - 1) << ": 0] " << outputs[i] << ";" << endl;
            }
        }
        
        test << endl << "wire " << "[" << bits_estados << " : 0] " << "Estado;" << endl << endl;;
        test << "\nalways #1 " << clk_reset[0] << "= ~{" << clk_reset[0] << "};\n\n"; // Always del reloj

        aux = "";
        for (auto valor : clk_reset)
        {
            aux += "." + valor + "(" + valor + ")" + ", ";
        }
        for (auto valor : inputs)
        {
            aux += "." + valor + "(" + valor + ")" + ", ";
        }
        for (auto valor : outputs)
        {
            aux += "." + valor + "(" + valor + ")" + ", ";
        }
        aux.pop_back();
        aux.pop_back();

        test << Nombre_Modulo << " UTT (.Estado(Estado), " << aux << ");" << endl
             << endl;

        test << "initial" << endl
             << "  begin" << endl
             << "\t$dumpfile(\"dump.vcd\");" << endl
             << "\t$dumpvars(0," << Nombre_Modulo << "_TB);" << endl
             << "\t" << clk_reset[0] << " <= 0;" << endl
             << "\t" << clk_reset[1] << " = 1;  #1" << endl;


             // Aqui van a agregar a CHRIS!!! JAjaja

             test << "\n\n\t//Agregar condiciones de verriciacion\n\n";

        test << "\t$finish;" << endl
             << "  end" << endl
             << "endmodule" << endl;
    }
}

//------------------------------------------------------------------------------------------------------------------


#endif // __CLASES_H__
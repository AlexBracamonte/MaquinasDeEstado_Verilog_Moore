import logging
import os

from LeerExcel import ReadExcel
import sys
import math

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s',
                    level=logging.DEBUG)


class MooreMachine:
    def __init__(self, file: object, design_name: str = "Design_FSM.txt", test: str = "test.sv", module: str = "FSM_Mealy"):
        self.inputs = []
        self.outputs = []
        self.states = []
        self.clk = "Clk"
        self.reset = "Reset"
        self.module = module
        self.bits_state = None
        self.aux = ""

        self.file = file
        self.file_out = design_name + ".sv"
        self.file_test = test + ".sv"

    def __del__(self):
        print(f"----- | Se esta borrando el objeto {__class__.__name__} | -----------")

    def get_inputs_vector(self):
        for valor in self.file.inputs:
            if 0 < self.file.inputs[valor] > 1:
                aux = f"[{self.file.inputs[valor] - 1} : 0] {valor}"
            if self.file.inputs[valor] == 1:
                aux = f"{valor}"
            self.inputs.append(aux)
        print(f"Las entradas son: {self.inputs}")
        return self.inputs

    def get_outputs_vector(self):
        for valor in self.file.outputs:
            if 0 < self.file.outputs[valor] > 1:
                aux = f"[{self.file.outputs[valor] - 1} : 0] {valor}"
            if self.file.outputs[valor] == 1:
                aux = f"{valor}"
            self.outputs.append(aux)
        print(f"Las salidas son: {self.outputs}")
        return self.outputs

    def get_paramters_states(self):
        print(f"El largo de los estados es {len(self.file.states)}")
        log2 = math.log2(len(self.file.states))
        bits = math.ceil(log2)
        self.bits_state = bits

        print(f"El numero de bits necesarios es {log2} y el numero máximo de bits es {bits}")
        for valor in self.file.states:
            num_in_bin = format(valor, f"0{str(bits)}b")
            aux = [self.file.states[valor], f"{bits}'b{num_in_bin}"]
            self.states.append(aux)
        print(f"Los estados son: {self.states}")
        self.aux = f"[{bits} : 0 ]"
        return self.states

    def write_design(self):
        try:
            with open(self.file_out, "w") as design:
                design.writelines(f"module {self.module} (Estado_Salida, ")

                aux = f"{self.clk}, {self.reset}, "
                for valor in self.file.inputs:
                    aux += f"{valor}, "
                for valor in self.file.outputs:
                    aux += f"{valor}, "
                design.writelines(f"{aux[:-2]});\n\n")         # Escribimos la primer parte del design

                # Imprimimos los valores de inputs
                for valor in self.inputs:
                    design.writelines(f"input {valor};\n")
                for valor in self.outputs:
                    design.writelines(f"output reg {valor};\n")

                design.writelines(f"\ninput {self.clk}, {self.reset};\n"
                                  f"output reg {self.aux} Estado_Salida; // Salida para verificar estados \n"
                                  f"reg [{self.bits_state - 1} : 0] state, next_state;\n\n"
                                  f"\nassign Estado_Salida = state; \t // Para verificar las salidas en el TB\n\n") # Asignamos los valores de clk y reset

                for estado, valor in self.states:
                    design.writelines(f"parameter {estado} = {valor};\n")

                design.writelines(f"\nalways @ (posedge {self.clk} or {self.reset})\n"
                                  f"  begin\n"
                                  f"\t if ({self.reset})\n"
                                  f"\t\t state <= {self.states[0][0]};\n"
                                  f"\t else\n"
                                  f"\t\t state <= next_state;\n"
                                  f"  end\n\n")

                design.writelines(f"\nalways @ (state)\n"
                                  f"  begin\n"
                                  f"\tcase(state)\n")
                for estado in self.file.states:
                    design.writelines(f"\t\t{self.file.states[estado]}:\n"
                                      f"\t\t  begin\n")

                    salidas = list(self.file.outputs.keys())
                    valores = self.file.outputs_values[self.file.states[estado]]
                    for index in range(0, len(salidas)):
                        design.writelines(f"\t\t\t{salidas[index]}= {valores[index]};\n")
                    design.writelines(f"\t\t  end\n")

                design.writelines(f"\tendcase\n"
                                  f"  end\n\n")

                # Ahora van las condiciones

                aux = ""
                for entrada in self.file.inputs:
                    aux += f"{entrada} or "
                design.writelines(f"always @ ({aux} state)\n"       # Escribimos el always de las funciones
                                  f"  begin\n"
                                  f"\tcase (state)\n")

                for estado in self.file.condicions2:
                    design.writelines(f"\t\t{estado}:\n")
                    if len(self.file.condicions2[estado]) == 1:         # SI no hay condiciones
                        design.writelines(f"\t\t\tnext_state = {self.file.condicions2[estado][0][0]};\n")
                    else:
                        design.writelines("\t\t  begin\n")
                        for condiciones in self.file.condicions2[estado]:
                            aux = ""
                            entradas = list(self.file.inputs.keys())
                            for index in range(0, len(entradas)):
                                if condiciones[index + 1] != ('X' or 'x'):
                                    aux += f"{entradas[index]} == {condiciones[index + 1]} & "
                            next = condiciones[0]
                            design.writelines(f"\t\t\tif ( {aux[:-2]} )\n")             #  End del estado
                            design.writelines(f"\t\t\t  begin\n")                       # begin del if
                            design.writelines(f"\t\t\t\tnext_state = {next};\n")
                            design.writelines(f"\t\t\t  end\n")                         # end del if
                        design.writelines("\t\t  end\n")

                design.writelines(f"\t\tdefault: next_state = {self.states[0][0]};\n"
                                  f"\tendcase\n"
                                  f"  end\n"
                                  f"endmodule")

        except Exception as inst:
            logging.error("No se encontro el archivo %s", self.file_out)
            logging.debug("%s", inst)
            sys.exit(1)

    def write_testbench(self):
        try:
            with open(f"{self.file_test}", "w+") as testbench:
                testbench.write("`timescale 1ns/1ns\n\n")
                testbench.write(f"module {self.module}_TB;\n\n")

                testbench.write(f"\treg {self.clk}, {self.reset};\n")

                for valor in self.inputs:
                    testbench.write(f"\treg {valor};\n")

                for valor in self.outputs:
                    testbench.write(f"\twire {valor};\n")
                testbench.write(f"\twire {self.aux} Estado_Salida;\n")

                aux = f".{self.clk}({self.clk}), .{self.reset}({self.reset}), .Estado_Salida(Estado_Salida), "
                for entrada in self.file.inputs:
                    aux += f".{str(entrada)}({str(entrada)}), "
                for salida in self.file.outputs:
                    aux += f".{str(salida)}({str(salida)}), "

                testbench.write(f"\n\t{self.module} UUT ({aux[:-2]});\n\n")

                testbench.write(f"\talways #1 {self.clk} = ~{self.clk};\n\n")

                testbench.write(f'initial begin\n'
                                f'\t$dumpfile("dump.vcd");\n'
                                f'\t$dumpvars(0, {self.module}_TB);\n\n'
                                f'\t{self.clk} <= 0;\n'
                                #f'\t{self.reset} = 1;  #1\n\n'
                                )


                testbench.write(f'$finish;\n'
                                f'\tend\n'
                                f'endmodule')

        except Exception as inst:
            logging.error("No se encontro el archivo %s", self.file_out)
            logging.debug("%s", inst)
            sys.exit(1)

    def run(self):
        self.get_inputs_vector()
        self.get_outputs_vector()
        self.get_paramters_states()
        self.write_design()
        self.write_testbench()

class MealyMachine:
    def __init__(self, file: object, design_name: str = "Design_FSM.txt", test: str = "test.sv", module: str = "FSM_Mealy"):
        self.inputs = []
        self.outputs = []
        self.states = []
        self.clk = "Clk"
        self.reset = "Reset"
        self.module = module
        self.bits_state = None

        self.file = file
        self.file_out = design_name
        self.file_test = test

    def __del__(self):
        print(f"Se esta borrando el objeto {__class__.__name__}")

    def get_inputs_vector(self):
        for valor in self.file.inputs:
            print(self.file.inputs[valor])
            if 0 < self.file.inputs[valor] > 1:
                aux = f"[{self.file.inputs[valor] - 1} : 0] {valor}"
            if self.file.inputs[valor] == 1:
                aux = f"{valor}"
            self.inputs.append(aux)
        print(self.inputs)
        return self.inputs

    def get_outputs_vector(self):
        for valor in self.file.outputs:
            print(self.file.outputs[valor])
            if 0 < self.file.outputs[valor] > 1:
                aux = f"[{self.file.outputs[valor] - 1} : 0] {valor}"
            if self.file.outputs[valor] == 1:
                aux = f"{valor};"
            self.outputs.append(aux)
        print(self.outputs)
        return self.outputs

    def get_paramters_states(self):
        print(f"El largo de los estados es {len(self.file.states)}")
        log2 = math.log2(len(self.file.states))
        bits = math.ceil(log2)
        self.bits_state = bits

        print(f"El numero de bits necesarios es {log2} y el numero máximo de bits es {bits}")
        for valor in self.file.states:
            num_in_bin = format(valor, f"0{str(bits)}b")
            aux = [self.file.states[valor], f"{bits}'b{num_in_bin}"]
            self.states.append(aux)
        print(self.states)
        return self.states

    def write_design(self):
        try:
            with open(self.file_out, "w") as design:
                if design.writable():
                    logging.debug("El archivo se abrio correctamente")

                    design.writelines(f"module {self.module} (")
                    for valor in self.file.inputs:
                        print(valor)
                        design.writelines(f"{valor}, ")
                    aux = f"{self.clk}, {self.reset}, "
                    for valor in self.file.outputs:
                        print(valor)
                        aux += f"{valor}, "
                    design.writelines(f"{aux[:-2]});\n\n")
                    for valor in self.inputs:
                        design.writelines(f"\tinput {valor};\n")
                    for valor in self.outputs:
                        design.writelines(f"\toutput {valor};\n")
                        design.writelines(f"\treg {valor};\n")
                    design.writelines(f"\n\n")

                    design.writelines(f"\tinput {self.clk}, {self.reset};\n\n")
                    for estado, valor in self.states:
                        design.writelines(f"\tparameter {estado} = {valor};\n")

                    design.writelines(f"\n\treg [{self.bits_state-1} : 0] state, next_state;\n")
                    design.writelines(f"\n\talways @ (posedge {self.clk} , {self.reset})\n")  #Aqui cambie
                    design.writelines(f"\t  begin\n")
                    design.writelines(f"\t\t if ({self.reset})\n")
                    design.writelines(f"\t\t\t state <= {self.states[0][0]};\n")
                    design.writelines(f"\t\t else\n")
                    design.writelines(f"\t\t\t state <= next_state;\n")
                    design.writelines(f"\t  end\n\n")

                    aux = ""
                    design.writelines(f"\talways @ (")
                    for valor in self.file.inputs:
                        print(valor)
                        aux += f"{valor} , "                            #Aqui cambie
                    design.writelines(f"{aux} state)\n")

                    design.writelines(f"\t  begin\n")
                    design.writelines(f"\t\t  case(state)\n")

                    for estado in self.file.condicions2:
                        print(f"PAra el estado : {estado}")

                        design.writelines(f"\t\t\t{estado}:\n")
                        design.writelines(f"\t\t\t  begin\n")           # begin del estado

                        """ ---- Los valores de las condiciones ---- """

                        print(f"Los valores obtenidos en los estados son: {estado} con un largo de {len(self.file.condicions2[estado])}")

                        if len(self.file.condicions2[estado]) == 1:
                            salidas = list(self.file.outputs.keys())
                            largo = len(salidas)  # Tamaño de la cadena
                            for index in range(0, largo):
                                design.writelines(
                                    f"\t\t\t\t\t{salidas[index]} = {self.file.outputs_values[estado][index]};\n")
                            design.writelines(f"\t\t\t\t\tnext_state = {self.file.condicions2[estado][0][0]};\n")
                        else:
                            for valor in self.file.condicions2[estado]:


                                aux = ""
                                entradas = list(self.file.inputs.keys())
                                largo = len(entradas)  # Tamaño de la cadena
                                print(f"{entradas} = {valor}")
                                for index in range(0, largo):
                                    aux += f"{entradas[index]} == {valor[index + 1]} & "
                                design.writelines(f"\t\t\t\tif ( {aux[:-2]} )\n")  # End del estado
                                design.writelines(f"\t\t\t\t  begin\n")  # begin del if


                                salidas = list(self.file.outputs.keys())
                                largo = len(salidas)  # Tamaño de la cadena
                                for index in range(0, largo):
                                    design.writelines(f"\t\t\t\t\t{salidas[index]} = {self.file.outputs_values[estado][index]};\n")

                                design.writelines(f"\t\t\t\t\tnext_state = {valor[0]};\n")



                                design.writelines(f"\t\t\t\t  end\n")  # End del if



                        design.writelines(f"\t\t\t  end\n\n")           # End del estado

                    design.writelines(f"\t\t  endcase\n")


                    design.writelines(f"\t  end\n\n")
                    design.writelines(f"endmodule\n\n")

                else:
                    print(f"El archivo no es editable")

        except Exception as inst:
            logging.error("No se encontro el archivo %s", self.file_out)
            logging.debug("%s", inst)
            sys.exit(1)

    def write_testbench(self):
       
        try:
            
            
            with open(f"{self.file_test}", "w+") as testbench:
                testbench.write("`timescale 1ns/1ns\n\n")
                testbench.write(f"module {self.module}_TB;\n\n")

                testbench.write(f"\treg {self.clk}, {self.reset};\n")

                for valor in self.inputs:
                    testbench.write(f"\treg {valor};\n")

                for valor in self.outputs:
                    testbench.write(f"\twire {valor};\n")

                aux = f".{self.clk}({self.clk}), .{self.reset}({self.reset}), "
                for entrada in self.file.inputs:
                    aux += f".{str(entrada)}({str(entrada)}), "
                for salida in self.file.outputs:
                    aux += f".{str(salida)}({str(salida)}), "
                
                de_clk = input("ingresa un delay para el clk: ")                   ####

                testbench.write(f"\n\t{self.module} UUT ({aux[:-2]});\n\n")

                testbench.write(f"\talways #{de_clk} {self.clk} = ~{self.clk};\n\n")

                testbench.write(f'initial begin\n'
                                f'\t$dumpfile("dump.vcd");\n'
                                f'\t$dumpvars(0, {self.module}_TB);\n\n'
                                f'\t{self.clk} <= 0;\n'
                               )
                
                f = open('comb_pruebas.txt','r')
                lineas = f.readlines()
                for item in lineas:
                    testbench.write(item)
        



                testbench.write(f'\t$finish;\n'
                                f'end\n'
                                f'endmodule')

        except Exception as inst:
            logging.error("No se encontro el archivo %s", self.file_out)
            logging.debug("%s", inst)
            sys.exit(1)

    def __str__(self) -> str:
        return f"Este es el objeto con las siguientes caracetisticas: "



if __name__ == '__main__':
    Excel = f"FMS_5"

    Test = f"Salidas/Testebch_{Excel}"
    Design = f"Salidas/Desing_{Excel}"
    Archivo_IN = f"Tablas/{Excel}"
    Archivo_OUT = f"Salidas/{Excel}"



    try:
        os.mkdir("Salidas")
    except Exception as Signal:
        logging.info(f"La carpeta ya existe\n")


    Excel = ReadExcel(file_name=Archivo_IN, file_out=Archivo_OUT)
    Excel.run()

    FSM2 = MooreMachine(file=Excel, design_name=Design, test=Test)
    FSM2.run()




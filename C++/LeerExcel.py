import pandas as pd
import sys
import logging
import json


logging.basicConfig(format='%(levelname)s - %(asctime)s - %(filename)s  - %(message)s',
                    level=logging.DEBUG)


class ReadExcel:
    def __init__(self, file_name: str, file_out: str = "data"):
        self.file_name = file_name
        self.file_name_out = file_out + ".json"
        self.file_name_configuracion = file_out + ".txt"
        self.file = None

        self.states = {}
        self.inputs = {}
        self.outputs = {}
        self.transiciones = {}
        self.condicions = []
        self.condicions2 = {}
        self.outputs_values = {}

    def __del__(self):
        print(f"Se esta borrando el objeto {__class__.__name__}")

    def __str__(self):
        logging.debug("Todo lo que se encontro fue:\n")
        return f"Este es una linea que obtenemos de una clase, los valores son:\n\n" \
               f"Inputs: {self.inputs} \n" \
               f"Outputs: {self.outputs} \n" \
               f"States: {self.states}\n" \
               f"Conditions {self.condicions2}\n" \
               f"Transiciones: {self.transiciones}\n\n"

    def open_file(self):
        try:
            self.file = pd.ExcelFile(self.file_name)
            if(self.file):
                logging.debug("Se abrio correctamente el archivo %s", self.file_name)
                print(f"El nombre de las hojas es {self.file.sheet_names}")
        except Exception as inst:
            logging.error("No se encontro el archivo %s", self.file_name)
            logging.debug("%s", inst)
            sys.exit(1)

    def get_states(self):
        logging.debug("Se activa get_states")
        sh1 = pd.read_excel(self.file_name, sheet_name='Estados')
        Estados = sh1.loc[:, "Estados"]
        Num_Estado = sh1.loc[:, "Numero_Estado"]
        for key in range(len(Estados)):
            self.states[Num_Estado[key]] = Estados[key]
        return self.states

    def get_outputs(self):
        logging.debug("Se activa get_inpus")
        sh1 = pd.read_excel(self.file_name, sheet_name='Salidas')
        Salidas = sh1.loc[:, "Nombre_Salida"]
        Longitud = sh1.loc[:, "Longitud"]
        for key in range(len(Salidas)):
            self.outputs[Salidas[key]] = Longitud[key]
        return self.outputs

    def get_inputs(self):
        logging.debug("Se activa get_outpus")
        sh1 = pd.read_excel(self.file_name, sheet_name='Entradas')
        Entradas = sh1.loc[:, "Nombre_Entradas"]
        Longitud = sh1.loc[:, "Longitud"]
        for key in range(len(Entradas)):
            self.inputs[Entradas[key]] = Longitud[key]
        return self.inputs

    def get_transicions(self):
        logging.debug("Se activa get_transiciones")
        sh2 = pd.read_excel(self.file_name, sheet_name='Transiciones')
        q = (sh2.iloc[:, 0])  # imprimir una columna
        r = (sh2.iloc[1, :])  # imprimir una fila

        for i in range(1, len(q)):  # recorre cada item de la primer columna
            s = sh2.iat[i, 0]
            self.transiciones[s] = []
            for j in range(1, len(r)):
                t = sh2.iat[i, j]
                self.transiciones[s].append(t)
        return self.transiciones

    def get_conditions(self):
        logging.debug("Se activa - Get_conditions")

        sh2 = pd.read_excel(self.file_name, sheet_name="Condiciones")
        q = (sh2.iloc[:, 0])  # imprimir una columna
        r = (sh2.iloc[0, :])  # imprimir una fila

        for i in range(1, len(q)):  # recorre cada item de la primer columna
            aux10 = []
            for j in range(0, len(r)):
                t = sh2.iat[i, j]
                aux10.append(t)
            self.condicions.append(aux10)
        return self.condicions

    def get_conditions2(self):
        logging.debug("Se activa -- get_conditions2 -- ")
        for valor in self.states:
            self.condicions2.update({self.states[valor]: []})

        sh2 = pd.read_excel(self.file_name, sheet_name="Condiciones")
        q = (sh2.iloc[:, 0])  # imprimir una columna
        r = (sh2.iloc[0, :])  # imprimir una fila

        for i in range(0, len(q)):  # recorre cada item de la primer columna
            aux10 = []
            for j in range(0, len(r)):
                t = sh2.iat[i, j]
                aux10.append(t)
            self.condicions2[aux10[0]].append(aux10[1:])

    def get_output_values(self):
        logging.debug("Se capturan los valores de salidas")
        sh2 = pd.read_excel(self.file_name, sheet_name="Valores_De_Salida")
        q = (sh2.iloc[:, 0])  # imprimir una columna
        r = (sh2.iloc[1, :])  # imprimir una fila

        for i in range(0, len(q)):  # recorre cada item de la primer columna
            aux10 = []
            s = sh2.iat[i, 0]
            for j in range(0, len(r)):
                t = sh2.iat[i, j]
                aux10.append(t)
            self.outputs_values[s] = aux10[1:]
        return self.outputs_values

    def write_variables(self):
        try:
            with open(self.file_name_configuracion, "w") as config:
                if config.writable():
                    logging.debug("El archivo se abrio correctamente")
                    config.write(f"---\n"
                                 f"Entradas: \n")
                    for valor in self.inputs:
                        config.write(f"{valor}={self.inputs[valor]};\n")
                    config.write(f"\n---\n"
                                 f"Salidas: \n")
                    for valor in self.outputs:
                        config.write(f"{valor}={self.outputs[valor]};\n")

                    config.write(f"\n---\n"
                                 f"Estados: \n")
                    for valor in self.states:
                        config.write(f"{self.states[valor]}={valor};\n")

                    config.write(f"\n---\n"
                                 f"Condiciones: \n")
                    for valor in self.condicions2:
                        for condiciones in self.condicions2[valor]:
                            config.write(f"Actual={valor};\n"
                                         f"Siguiente={condiciones[0]};\n"
                                         f"Condiciones={condiciones[1:]};\n\n")

                    config.write(f"---\n"
                                 f"Valores_Salidas: \n")
                    for valor in self.outputs_values:
                        config.write(f"{valor}={self.outputs_values[valor]};\n")

                else:
                    self.__del__()

        except Exception as inst:
            logging.error("No se encontro el archivo")
            logging.debug("%s", inst)
            sys.exit(1)

    def write_json(self):
        logging.debug("Se activa write_json")
        data = {"Entradas": []}
        for valor in self.inputs:
            aux2 = {str(valor): str(self.inputs[valor])}
            data["Entradas"].append(aux2)

        data["Salidas"] = []
        for valor in self.outputs:
            aux2 = {str(valor): str(self.outputs[valor])}
            data["Salidas"].append(aux2)

        data["Estados"] = []
        for valor in self.states:
            aux2 = {str(valor): str(self.states[valor])}
            data["Estados"].append(aux2)

        data["Transiciones"] = []
        for valor in self.transiciones:
            aux2 = {str(valor): self.transiciones[valor]}
            data["Transiciones"].append(aux2)

        data["Condiciones"] = []
        for transicion in self.condicions:
            aux = []
            aux.append({"EstadoActual": str(transicion[0])})
            aux.append({"EstadoSiguiente": str(transicion[1])})
            aux3 = []
            for valor in transicion[2:]:
                aux3.append(str(valor))
            aux.append({"Condiciones": aux3})
            valores = {self.condicions.index(transicion): aux}
            data["Condiciones"].append(valores)

        with open(self.file_name_out, 'w') as file:
            json.dump(data, file, indent=5)
            logging.info("Archivo, %s generado", self.file_name_out)
    
    def run(self):
        self.open_file()
        self.get_inputs()
        self.get_outputs()
        self.get_states()
        self.get_transicions()
        self.get_conditions()
        self.get_conditions2()
        self.get_output_values()
        # self.write_json()
        self.write_variables()

    

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print(sys.argv)
        p = ReadExcel(file_name= sys.argv[1], file_out= sys.argv[2])
        p.run()
        print(p)
    else:
        #p = ReadExcel('FMS_Base3.xlsx')
        print("No se agrego nada")
    #
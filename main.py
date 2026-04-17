import sys 
from simulador import Simulador
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from interfaz import Ui_MainWindow

# Comando para actualizar el archivo de Python de la Interfaz
# pyuic5 -x "Interfaz Modelo Teoria de Colas.ui" -o interfaz.py

class MiApp(QMainWindow):
    def __init__(self):
        super().__init__()

        print("Iniciando app...")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        print("UI cargada correctamente")
        self.Simulador=Simulador()
        # Conectar botón
        self.ui.pushButton_Simular.clicked.connect(self.simular)


    
    def obtener_parametros(self):
        parametros = {}


        # TIEMPO DE LLEGADA
        if self.ui.checkBox_t_llegada_constante.isChecked():
            parametros["llegada"] = {
                "tipo": "constante",
                "valor": float(self.ui.lineEdit_t_llegada_constante.text())
            }
        elif self.ui.comboBox_distribucion_t_llegada.currentText()=="Uniforme":
            parametros["llegada"] = {
                "tipo": "uniforme",
                "min": float(self.ui.lineEdit_t_llegada_min.text()),
                "max": float(self.ui.lineEdit_t_llegada_max.text())
            }
        elif self.ui.comboBox_distribucion_t_llegada.currentData()=="Normal":
            parametros["llegada"] = {
                "tipo": "normal",
                "min": float(self.ui.lineEdit_t_llegada_min.text()),
                "max": float(self.ui.lineEdit_t_llegada_max.text())
            }


        # TIEMPO DE SERVICIO 
        if self.ui.checkBox_t_fin_servicio_constante.isChecked():
            parametros["servicio"] = {
                "tipo": "constante",
                "valor": float(self.ui.lineEdit_t_fin_servicio_constante.text())
            }
        else:
            # Elegir distribucion del servicio
            match self.ui.comboBox_distribucion_t_fin_servicio.currentText():

                case "Uniforme":
                    parametros["llegada"] = {
                        "tipo": "uniforme",
                        "min": float(self.ui.lineEdit_t_llegada_min.text()),
                        "max": float(self.ui.lineEdit_t_llegada_max.text())
                    }
                case "Normal":
                    parametros["llegada"] = {
                        "tipo": "normal",
                        "min": float(self.ui.lineEdit_t_llegada_min.text()),
                        "max": float(self.ui.lineEdit_t_llegada_max.text())
                    }



        # DESCANSO
        if self.ui.groupBox_descanso.isChecked():
            if self.ui.checkBox_descanso_constante.isChecked():
                parametros["descanso"] = {
                    "tiempo_descanso":{
                        "tipo": "constante",
                        "valor": float(self.ui.lineEdit_tiempo_descanso_constante.text()),
                    },
                    "tiempo_entre_descanso": {
                        "tipo": "constante",
                        "valor": float(self.ui.lineEdit_tiempo_regreso_descanso_constante.text())
                    }
                }
                
            else:
                # Elegir distribucion del Descanso
                match self.ui.comboBox_distribucion_t_descanso.currentText():
                    case "Uniforme":
                        parametros["descanso"] = {
                            "tiempo_descanso": {
                                "tipo": "uniforme",
                                "min": float(self.ui.lineEdit_tiempo_descanso_min.text()),
                                "max": float(self.ui.lineEdit_tiempo_descanso_max.text()),
                            },
                            "tiempo_entre_descanso": {
                                "tipo": "uniforme",
                                "min": float(self.ui.lineEdit_tiempo_regreso_descanso_min.text()),
                                "max": float(self.ui.lineEdit_tiempo_regreso_descanso_max.text())
                            }
                        }

                    case "Normal":
                        parametros["descanso"] = {
                            "tiempo_descanso": {
                                "tipo": "normal",
                                "min": float(self.ui.lineEdit_tiempo_descanso_min.text()),
                                "max": float(self.ui.lineEdit_tiempo_descanso_max.text()),
                            },
                            "tiempo_entre_descanso": {
                                "tipo": "normal",
                                "min": float(self.ui.lineEdit_tiempo_regreso_descanso_min.text()),
                                "max": float(self.ui.lineEdit_tiempo_regreso_descanso_max.text())
                            }
                        }

        # TIPOS DE CLIENTES
        if self.ui.groupBox_tipos_clientes.isChecked()==True:
            if self.ui.checkBox_t_llegada_B_constante.isChecked()==True:
                parametros["tipos_clientes"]={
                    "tipo":"constante",
                    "valor": float(self.ui.lineEdit_t_llegada_B_constante.text())
                }
            else:
                # Elegir distribucion de la llegada de los clientes B
                match self.ui.comboBox_distribucion_t_llegada_B.currentText():
                    case "Uniforme":
                        parametros["tipos_clientes"] = {
                            "tipo": "uniforme",
                            "min": float(self.ui.lineEdit_t_llegada_min.text()),
                            "max": float(self.ui.lineEdit_t_llegada_max.text())
                        }

                    case "Normal":
                        parametros["tipos_clientes"] = {
                            "tipo": "normal",
                            "min": float(self.ui.lineEdit_t_llegada_min.text()),
                            "max": float(self.ui.lineEdit_t_llegada_max.text())
                        }


        elif self.ui.comboBox_distribucion_t_llegada.currentData()=="Normal":
            parametros["llegada"] = {
                "tipo": "normal",
                "min": float(self.ui.lineEdit_t_llegada_min.text()),
                "max": float(self.ui.lineEdit_t_llegada_max.text())
            }


        # ABANDONO
        if self.ui.checkBox_abandono.isChecked():

            parametros["abandono"] = {
                "tipo": "constante",
                "valor": float(self.ui.lineEdit_t_abandono.text())
            }


        # ZONA DE SEGURIDAD
        if self.ui.checkBox_zona_seguridad.isChecked():
            parametros["zona_seguridad"] = {
                "tipo": "uniforme",
                "valor": float(self.ui.lineEdit_t_zona_seguridad.text())
            }
        
        # TIEMPO DE SIMULACION
        parametros["t_simumulacion"] = float(self.ui.lineEdit_t_simulacion.text())

        return parametros

    def mostrar_tabla(self, datos):
        tabla = self.ui.tableWidget_tabla_sim

        tabla.setRowCount(len(datos))
        tabla.setColumnCount(len(datos[0]))

        for i, fila in enumerate(datos):
            for j, valor in enumerate(fila):
                tabla.setItem(i, j, QTableWidgetItem(str(valor)))


    def simular(self):
        print("Botón presionado")

        parametros = self.obtener_parametros()

        resultados = self.Simulador.simular_cola(parametros)

        self.mostrar_tabla(resultados["tabla"])

        

        self.ui.tableWidget_tabla_sim.setHorizontalHeaderLabels(resultados["headers"])
        self.ui.tableWidget_tabla_sim.resizeColumnsToContents()
         



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiApp()
    ventana.show()
    sys.exit(app.exec_())
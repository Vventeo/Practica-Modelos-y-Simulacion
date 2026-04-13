from collections import deque
import random

class Evento:
    def __init__(self, tiempo, tipo, datos=None):
        self.tiempo = tiempo
        self.tipo = tipo
        self.datos = datos

class Simulador():

    
        
    
        





    def generar_tiempo(self, config):
        if config["tipo"] == "constante":
            return config["valor"]
        elif config["tipo"] == "uniforme":
            return random.uniform(config["min"], config["max"])
        elif config["tipo"] == "normal":
            return random.normalvariate(config["min"], config["max"])

    def simular_cola(self,params):


        # ---------------- PARÁMETROS ----------------
        TIEMPO_SIMULACION=500
        config_llegada = params["llegada"]
        config_servicio = params["servicio"]

        
        if "descanso" in params:
            hay_descanso=True
            config_t_descanso=params["descanso"]["tiempo_descanso"]
            config_t_entre_descansos=params["descanso"]["tiempo_entre_descanso"]
        
        if "abandono" in params:
            hay_abandono=True
            config_abandono=params["abandono"]

        if "zona_seguridad" in params:
            hay_zona_seguridad = True
            config_zona_seguridad=params["zona_seguridad"]

        if "tipos_clientes" in params:
            hay_tipos_clientes = True
            config_llegada_clientes_B=params["zona_seguridad"]




        # ---------------- ESTADO ----------------
        tiempo_actual = 0
        servidor_ocupado = False
        servidor_presente = True
        cola = deque()
        cola_b = deque()
        

        proxima_llegada = self.generar_tiempo(config_llegada)
        proximo_fin_servicio = float('inf')
        proximo_abandono = float('inf')
        proximo_inicio_descanso = float('inf')
        proximo_fin_descanso = float('inf')
        proxima_llegada_cliente_B = self.generar_tiempo(config_llegada_clientes_B)
        proxima_zona_seguridad = float('inf')

        tabla = []

        # ---------------- ESTADÍSTICAS ----------------
        clientes_atendidos = 0
        clientes_abandonan = 0


        


        # ---------------- SIMULACIÓN ----------------

        while tiempo_actual < TIEMPO_SIMULACION:



            # ---------------- EVENTOS ----------------
            eventos = [
                ("llegada", proxima_llegada),
                ("fin_servicio", proximo_fin_servicio),               
                ]
            headers

            if hay_abandono: eventos.append(("abandono", proximo_abandono))
            if hay_descanso: eventos.extend( [ ("inicio_descanso", proximo_inicio_descanso), ("fin_descanso", proximo_fin_descanso) ] )
            if hay_tipos_clientes: eventos.append(("llegada_clientes_B", proxima_llegada_cliente_B))
            if hay_zona_seguridad: eventos.append(("zona_seguridad", proxima_zona_seguridad))

            # determinar evento con prioridad
            

            def prioridad(e):
                return {"fin_servicio": 1, 
                        "llegada": 2, 
                        "abandono": 3}[e]

            eventos.sort(key=lambda x: (x[1], prioridad(x[0])))
            tipo_evento, tiempo_evento = eventos[0]

            tiempo_actual = tiempo_evento

        
                
            # ---------------- EVENTOS ----------------

            if tipo_evento == "llegada":

                proxima_llegada += self.generar_tiempo(config_llegada)

                cliente = {
                    "llegada": tiempo_actual,
                }

                if hay_descanso:
                    if servidor_presente and (not servidor_ocupado):
                        servidor_ocupado = True
                        proximo_fin_servicio = tiempo_actual + self.generar_tiempo(config_servicio)

                    else:
                        cola.append(cliente)
                        if hay_abandono:
                            cliente["abandono"] = tiempo_actual + self.generar_tiempo(config_abandono)

                if not servidor_ocupado:
                    servidor_ocupado = True
                    proximo_fin_servicio = tiempo_actual + self.generar_tiempo(config_servicio)
                else:
                    cola.append(cliente)
                    if hay_abandono:
                            cliente["abandono"] = tiempo_actual + self.generar_tiempo(config_abandono)




            if tipo_evento=="llegada_b":

                proxima_llegada_cliente_B += self.generar_tiempo(config_llegada_clientes_B)

                cliente = {
                    "llegada": tiempo_actual,
                }

                if hay_descanso:
                    if servidor_presente and (not servidor_ocupado):
                        servidor_ocupado = True
                        proximo_fin_servicio = tiempo_actual + self.generar_tiempo(config_servicio)

                    else:
                        cola_b.append(cliente)
                        if hay_abandono:
                            cliente["abandono"] = tiempo_actual + self.generar_tiempo(config_abandono)

                if not servidor_ocupado:
                    servidor_ocupado = True
                    proximo_fin_servicio = tiempo_actual + self.generar_tiempo(config_servicio)
                else:
                    cola_b.append(cliente)
                    if hay_abandono:
                            cliente["abandono"] = tiempo_actual + self.generar_tiempo(config_abandono)

                


            elif tipo_evento == "fin_servicio":

                clientes_atendidos += 1

                if len(cola) > 0:
                    cliente = cola.popleft()  # FIFO correcto
                    proximo_fin_servicio = tiempo_actual + self.generar_tiempo(config_servicio)
                    
                else:
                    servidor_ocupado = False
                    proximo_fin_servicio = float('inf')



            elif tipo_evento == "abandono":

                # encontrar cliente que abandona
                for c in cola:
                    if c["abandono"] == tiempo_actual:
                        cola.remove(c)
                        clientes_abandonan += 1
                        break

            elif tipo_evento=="inicio_descanso":

                servidor_presente=False
                proximo_inicio_descanso=float("inf")
                proximo_fin_descanso=tiempo_actual+ self.generar_tiempo(config_t_descanso)

                if servidor_ocupado==True:
                    proximo_fin_servicio = proximo_fin_servicio + self.generar_tiempo(config_t_descanso)

                

            elif tipo_evento=="fin_descanso":

                servidor_presente=True
                proximo_fin_descanso=float("inf")
                proximo_inicio_descanso = tiempo_actual + self.generar_tiempo(config_t_entre_descansos)


                
            
            if hay_abandono and len(cola) > 0:
                proximo_abandono = min([c["abandono"] for c in cola])
            else:
                proximo_abandono = float('inf')


            # ---------------- REGISTRO ----------------
            tabla.append([
                tiempo_actual,
                proxima_llegada,
                proxima_llegada_cliente_B,
                proximo_abandono,
                proximo_fin_servicio,
                proximo_inicio_descanso,
                proximo_fin_descanso,
                proxima_zona_seguridad,
                servidor_ocupado,
                servidor_presente,
                len(cola),
                len(cola_b),
                tipo_evento
            ])

        
        headers=["Tiempo Actual",
                 "Prox Llegada", 
                 "Prox Llegada B", 
                 "Prox Abandono", 
                 "Prox Fin Servicio",
                 "Prox Inicio Descanso", 
                 "Prox Fin Descanso",
                 "Prox Zona Seguridad",
                 "Serv Ocupado",
                 "Serv Presente",
                 "Cola",
                 "Cola B",
                 "Evento"]


        # ---------------- RESULTADO ----------------
        return {
            "tabla": tabla,
            "headers": headers,
            "clientes_atendidos": clientes_atendidos,
            "clientes_abandonan": clientes_abandonan
        }
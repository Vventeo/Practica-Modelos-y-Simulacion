import random
from tabulate import tabulate
from collections import deque

#Constantes
TIEMPO_LLEGADA = 45
TIEMPO_LLEGADA_B = 30
TIEMPO_SERVICIO = 35
TIEMPO_SIMULACION=300


#Variables de Estado
tiempo_actual = 0
servidor_ocupado = False
servidor_presente = True
cola = deque()
cola_b =deque()
tabla=[]

#Variables de Eventos
proxima_llegada = TIEMPO_LLEGADA
proxima_llegada_b = TIEMPO_LLEGADA_B
proximo_fin_servicio = float('inf')
proximo_fin_descanso=float('inf')

eventos=[]

#Estadisticas
clientes_atendidos=0


print("Simulación de sistema de colas\n")



while tiempo_actual < TIEMPO_SIMULACION:

    eventos = [
                ("llegada", proxima_llegada),
                ("fin_servicio", proximo_fin_servicio),
                ("llegada_b", proxima_llegada_b)               
                ]

    def prioridad(e):
        return {"fin_servicio": 1, 
                "llegada": 2, 
                "llegada_b": 3}[e]

    eventos.sort(key=lambda x: (x[1], prioridad(x[0])))
    proximo_evento, tiempo_evento = eventos[0]

    tiempo_actual = tiempo_evento



    match proximo_evento:

        case "llegada":     

            proxima_llegada += TIEMPO_LLEGADA

            if servidor_ocupado==False and servidor_presente==True:
                servidor_ocupado = True
                proximo_fin_servicio = tiempo_actual + TIEMPO_SERVICIO
                
            else:
                cola.append(tiempo_actual)
            


        case "llegada_b":
            proxima_llegada_b=tiempo_actual+TIEMPO_LLEGADA_B

            if servidor_ocupado==False and servidor_presente==True:
                servidor_ocupado = True
                proximo_fin_servicio = tiempo_actual + TIEMPO_SERVICIO
                
            else:
                cola_b.append(tiempo_actual)
        


        case "fin_servicio":

            clientes_atendidos += 1

            if len(cola) > 0:
                llegada_cliente = cola.popleft()
                proximo_fin_servicio = tiempo_actual+ TIEMPO_SERVICIO
            # elif len(cola_b)>0:
            #     llegada_cliente=cola_b.popleft()
            #     proximo_fin_servicio =tiempo_actual + TIEMPO_SERVICIO
            else:
                servidor_ocupado = False
                proximo_fin_servicio = float('inf')


 


    tabla.append([tiempo_actual,
                  proxima_llegada,
                  proxima_llegada_b,
                  proximo_fin_servicio,
                  servidor_ocupado,
                  len(cola),
                  len(cola_b),
                  proximo_evento])
    

print(tabulate(tabla, 
               headers=["Tiempo Actual",
                        "Prox Llegada",
                        "Prox Llegada B",
                        "Prox Salida",
                        "PS", 
                        "Cola", 
                        "Cola B",
                        "Evento"]))
        
print("\n",clientes_atendidos)


print("\nSimulación terminada")
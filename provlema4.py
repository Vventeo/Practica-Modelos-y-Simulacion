from collections import deque


TIEMPO_LLEGADA = 45
TIEMPO_LLEGADA_B = 30
TIEMPO_SERVICIO = 40
NUM_CLIENTES = 5


tiempo_actual = 0
servidor_ocupado = False
cola = deque()
cola_b=deque()


proxima_llegada = TIEMPO_LLEGADA
proxima_llegada_b= TIEMPO_LLEGADA_B
proximo_fin_servicio = float('inf')

# Estadísticas
clientes_atendidos = 0
tabla=[]
print("Simulación de sistema de colas\n")

while clientes_atendidos < NUM_CLIENTES:

    # Determinar próximo evento
    proximo_evento=min(proximo_fin_servicio,proxima_llegada, proxima_llegada_b)

    if proximo_evento==proxima_llegada:
        tiempo_actual = proxima_llegada
        evento = "llegada"
    elif proximo_evento==proximo_fin_servicio:
        tiempo_actual = proximo_fin_servicio
        evento = "fin_servicio"
    else:
        tiempo_actual=proxima_llegada_b
        evento = "llegada_b"

    # --------------------------------
    # EVENTO: LLEGADA
    # --------------------------------
    if evento == "llegada":

        

        proxima_llegada += TIEMPO_LLEGADA

        if not servidor_ocupado:
            servidor_ocupado = True
            proximo_fin_servicio = tiempo_actual + TIEMPO_SERVICIO

        else:
            cola.append(tiempo_actual)

        


    # --------------------------------
    # EVENTO: FIN DE SERVICIO
    # --------------------------------
    elif evento == "fin_servicio":

        

        clientes_atendidos += 1

        if len(cola) > 0:
            llegada_cliente = cola.popleft()
            proximo_fin_servicio = tiempo_actual + TIEMPO_SERVICIO
        elif len(cola_b)>0:
            
        else:
            servidor_ocupado = False
            proximo_fin_servicio = float('inf')

    else:
        proxima_llegada_b =tiempo_actual + TIEMPO_LLEGADA_B

        if not servidor_ocupado:
            servidor_ocupado = True
            proximo_fin_servicio = tiempo_actual + TIEMPO_SERVICIO
            

        else:
            cola_b.append(tiempo_actual)
        

    tabla.append([tiempo_actual,proxima_llegada,proximo_fin_servicio,servidor_ocupado,len(cola),evento])




print("\nSimulación terminada")
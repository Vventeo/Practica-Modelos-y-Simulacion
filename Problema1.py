from collections import deque


TIEMPO_LLEGADA = 25
TIEMPO_SERVICIO = 40
NUM_CLIENTES = 5


tiempo_actual = 0
servidor_ocupado = False
cola = deque()


proxima_llegada = TIEMPO_LLEGADA
fin_servicio = float('inf')

# Estadísticas
clientes_atendidos = 0

print("Simulación de sistema de colas\n")

while clientes_atendidos < NUM_CLIENTES:

    # Determinar próximo evento
    if proxima_llegada < fin_servicio:
        tiempo_actual = proxima_llegada
        evento = "llegada"
    else:
        tiempo_actual = fin_servicio
        evento = "fin_servicio"

    # --------------------------------
    # EVENTO: LLEGADA
    # --------------------------------
    if evento == "llegada":

        

        proxima_llegada += TIEMPO_LLEGADA

        if not servidor_ocupado:
            servidor_ocupado = True
            fin_servicio = tiempo_actual + TIEMPO_SERVICIO
            print("Tiempo Actual\tProx Llegada\tProx Salida\tPS\tCola")
            print(f"{tiempo_actual}\t\t{proxima_llegada}\t\t{fin_servicio}\t\t{int(servidor_ocupado)}\t{len(cola)}\n")

        else:
            cola.append(tiempo_actual)
            print("Tiempo Actual\tProx Llegada\tProx Salida\tPS\tCola")
            print(f"{tiempo_actual}\t\t{proxima_llegada}\t\t{fin_servicio}\t\t{int(servidor_ocupado)}\t{len(cola)}\n")

        


    # --------------------------------
    # EVENTO: FIN DE SERVICIO
    # --------------------------------
    else:

        print("Tiempo Actual\tProx Llegada\tProx Salida\tPS\tCola")

        clientes_atendidos += 1

        if len(cola) > 0:
            llegada_cliente = cola.popleft()
            fin_servicio = tiempo_actual + TIEMPO_SERVICIO
            print(f"{tiempo_actual}\t\t{proxima_llegada}\t\t{fin_servicio}\t\t{int(servidor_ocupado)}\t{len(cola)}", "\tcliente pasa de cola a servicio\n")

        else:
            servidor_ocupado = False
            fin_servicio = float('inf')
            print(f"{tiempo_actual}\t\t{proxima_llegada}\t\t{fin_servicio}\t\t{int(servidor_ocupado)}\t{len(cola)}", "\tcola vacía → servidor queda libre\n")


print("\nSimulación terminada")
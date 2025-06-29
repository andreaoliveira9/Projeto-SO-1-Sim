import argparse
import heapq
import random

# Parâmetros da simulação
MEAN_INTERARRIVAL = 1.0
MEAN_SERVICE_TYPE1 = 0.8
UNIF_SERVICE_TYPE2_MIN = 0.5
UNIF_SERVICE_TYPE2_MAX = 0.7
P_TYPE1 = 0.8
SIM_TIME = 1000.0

# Estado dos servidores
servers_A = [False, False]  # dois servidores tipo A
servers_B = [False]  # um servidor tipo B

# Filas
queue_type1 = []
queue_type2 = []

# Contadores estatísticos
delays_type1 = []
delays_type2 = []
area_num_in_queue_type1 = 0.0
area_num_in_queue_type2 = 0.0
server_A_time_type1 = [0.0 for _ in servers_A]
server_A_time_type2 = [0.0 for _ in servers_A]
server_B_time_type1 = [0.0 for _ in servers_B]
server_B_time_type2 = [0.0 for _ in servers_B]

# Relógio da simulação
clock = 0.0
last_event_time = 0.0

# Lista de eventos futuros
# Cada evento é um tuple: (instante, tipo_evento, dados_opcionais)
event_list = []


def schedule_event(time, event_type, data=None):
    heapq.heappush(event_list, (time, event_type, data))


def exponential(mean):
    return random.expovariate(1.0 / mean)


def uniform(a, b):
    return random.uniform(a, b)


def find_free_server(servers):
    for i, busy in enumerate(servers):
        if not busy:
            return i
    return None


def arrival():
    global clock

    # Agendar próxima chegada
    interarrival = exponential(MEAN_INTERARRIVAL)
    schedule_event(clock + interarrival, "arrival")

    # Determinar tipo de cliente
    if random.random() < P_TYPE1:
        # Tipo 1
        idx_A = find_free_server(servers_A)
        if idx_A is not None:
            service_time = exponential(MEAN_SERVICE_TYPE1)
            servers_A[idx_A] = True
            server_A_time_type1[idx_A] += service_time
            schedule_event(clock + service_time, "departure_type1", ("A", idx_A))
        else:
            idx_B = find_free_server(servers_B)
            if idx_B is not None:
                service_time = exponential(MEAN_SERVICE_TYPE1)
                servers_B[idx_B] = True
                server_B_time_type1[idx_B] += service_time
                schedule_event(clock + service_time, "departure_type1", ("B", idx_B))
            else:
                queue_type1.append(clock)
    else:
        # Tipo 2
        idx_A = find_free_server(servers_A)
        idx_B = find_free_server(servers_B)
        if idx_A is not None and idx_B is not None:
            service_time = uniform(UNIF_SERVICE_TYPE2_MIN, UNIF_SERVICE_TYPE2_MAX)
            servers_A[idx_A] = True
            servers_B[idx_B] = True
            server_A_time_type2[idx_A] += service_time
            server_B_time_type2[idx_B] += service_time
            schedule_event(clock + service_time, "departure_type2", (idx_A, idx_B))
        else:
            queue_type2.append(clock)


def departure_type1(info):
    server_type, server_idx = info

    if server_type == "A":
        servers_A[server_idx] = False
    else:
        servers_B[server_idx] = False

    idx_A = server_idx if server_type == "A" else find_free_server(servers_A)
    idx_B = server_idx if server_type == "B" else find_free_server(servers_B)
    if queue_type2 and idx_A is not None and idx_B is not None:
        arrival_time = queue_type2.pop(0)
        delay = clock - arrival_time
        delays_type2.append(delay)
        service_time = uniform(UNIF_SERVICE_TYPE2_MIN, UNIF_SERVICE_TYPE2_MAX)
        servers_A[idx_A] = True
        servers_B[idx_B] = True
        server_A_time_type2[idx_A] += service_time
        server_B_time_type2[idx_B] += service_time
        schedule_event(clock + service_time, "departure_type2", (idx_A, idx_B))
    elif queue_type1:
        if idx_A is not None:
            arrival_time = queue_type1.pop(0)
            delay = clock - arrival_time
            delays_type1.append(delay)
            service_time = exponential(MEAN_SERVICE_TYPE1)
            servers_A[idx_A] = True
            server_A_time_type1[idx_A] += service_time
            schedule_event(clock + service_time, "departure_type1", ("A", idx_A))
        elif idx_B is not None:
            arrival_time = queue_type1.pop(0)
            delay = clock - arrival_time
            delays_type1.append(delay)
            service_time = exponential(MEAN_SERVICE_TYPE1)
            servers_B[idx_B] = True
            server_B_time_type1[idx_B] += service_time
            schedule_event(clock + service_time, "departure_type1", ("B", idx_B))


def departure_type2(indices):
    server_idx_A, server_idx_B = indices

    servers_A[server_idx_A] = False
    servers_B[server_idx_B] = False

    if queue_type2:
        arrival_time = queue_type2.pop(0)
        delay = clock - arrival_time
        delays_type2.append(delay)
        service_time = uniform(UNIF_SERVICE_TYPE2_MIN, UNIF_SERVICE_TYPE2_MAX)
        servers_A[server_idx_A] = True
        servers_B[server_idx_B] = True
        server_A_time_type2[server_idx_A] += service_time
        server_B_time_type2[server_idx_B] += service_time
        schedule_event(
            clock + service_time, "departure_type2", (server_idx_A, server_idx_B)
        )
    elif queue_type1:
        arrival_time = queue_type1.pop(0)
        delay = clock - arrival_time
        delays_type1.append(delay)
        service_time = exponential(MEAN_SERVICE_TYPE1)
        servers_A[server_idx_A] = True
        server_A_time_type1[server_idx_A] += service_time
        schedule_event(clock + service_time, "departure_type1", ("A", server_idx_A))


def report():
    global area_num_in_queue_type1, area_num_in_queue_type2

    mean_delay_type1 = sum(delays_type1) / len(delays_type1) if delays_type1 else 0
    mean_delay_type2 = sum(delays_type2) / len(delays_type2) if delays_type2 else 0
    mean_area_num_in_queue_type1 = area_num_in_queue_type1 / SIM_TIME
    mean_area_num_in_queue_type2 = area_num_in_queue_type2 / SIM_TIME

    print("Tipo 1 - atraso médio:", mean_delay_type1)
    print("Tipo 2 - atraso médio:", mean_delay_type2)
    print("Tipo 1 - número médio na fila:", mean_area_num_in_queue_type1)
    print("Tipo 2 - número médio na fila:", mean_area_num_in_queue_type2)

    for i in range(len(servers_A)):
        print(
            f"Servidor A{i+1} - % tempo com tipo 1: {100 * server_A_time_type1[i] / SIM_TIME:.2f}%, tipo 2: {100 * server_A_time_type2[i] / SIM_TIME:.2f}%"
        )
    for i in range(len(servers_B)):
        print(
            f"Servidor B{i+1} - % tempo com tipo 1: {100 * server_B_time_type1[i] / SIM_TIME:.2f}%, tipo 2: {100 * server_B_time_type2[i] / SIM_TIME:.2f}%"
        )


def simulate():
    global clock, last_event_time, area_num_in_queue_type1, area_num_in_queue_type2

    schedule_event(0.0, "arrival")

    while event_list and clock < SIM_TIME:
        clock, event_type, data = heapq.heappop(event_list)
        dt = clock - last_event_time
        area_num_in_queue_type1 += len(queue_type1) * dt
        area_num_in_queue_type2 += len(queue_type2) * dt
        last_event_time = clock

        if event_type == "arrival":
            arrival()
        elif event_type == "departure_type1":
            departure_type1(data)
        elif event_type == "departure_type2":
            departure_type2(data)

    # Resultados
    report()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="Seed para aleatoriedade")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    simulate()

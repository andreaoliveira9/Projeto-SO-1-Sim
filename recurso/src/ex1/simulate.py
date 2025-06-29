from collections import deque
import heapq
import random
import config
import statistics


def init_state():
    global servers_A, servers_B, server_A_type, server_B_type
    global queue_type1, queue_type2
    global clock, last_event_time
    global event_list

    # Estado dos servidores
    servers_A = [False for _ in range(config.NUM_SERVERS_A)]
    servers_B = [False for _ in range(config.NUM_SERVERS_B)]

    server_A_type = [None for _ in range(config.NUM_SERVERS_A)]  # "type1" ou "type2"
    server_B_type = [None for _ in range(config.NUM_SERVERS_B)]

    # Inicializar os tempos de uso dos servidores em statistics
    statistics.server_A_time_type1 = [0.0 for _ in range(config.NUM_SERVERS_A)]
    statistics.server_A_time_type2 = [0.0 for _ in range(config.NUM_SERVERS_A)]
    statistics.server_B_time_type1 = [0.0 for _ in range(config.NUM_SERVERS_B)]
    statistics.server_B_time_type2 = [0.0 for _ in range(config.NUM_SERVERS_B)]

    # Filas
    queue_type1 = deque()
    queue_type2 = deque()

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


def serve_type1(idx, server_type):
    """Serve a type 1 customer on the specified server and schedules departure."""
    service_time = exponential(config.MEAN_SERVICE_TYPE1)
    if server_type == "A":
        servers_A[idx] = True
        server_A_type[idx] = "type1"
        statistics.server_A_time_type1[idx] += service_time
    else:
        servers_B[idx] = True
        server_B_type[idx] = "type1"
        statistics.server_B_time_type1[idx] += service_time
    schedule_event(clock + service_time, "departure_type1", (server_type, idx))
    return service_time


def serve_type2(idx_A, idx_B):
    """Serve a type 2 customer using servers A and B, and schedules departure."""
    service_time = uniform(config.UNIF_SERVICE_TYPE2_MIN, config.UNIF_SERVICE_TYPE2_MAX)
    servers_A[idx_A] = True
    servers_B[idx_B] = True
    server_A_type[idx_A] = "type2"
    server_B_type[idx_B] = "type2"
    statistics.server_A_time_type2[idx_A] += service_time
    statistics.server_B_time_type2[idx_B] += service_time
    schedule_event(clock + service_time, "departure_type2", (idx_A, idx_B))
    return service_time


def try_serve_type1_from_queue(idx, server_type):
    if queue_type1:
        arrival_time = queue_type1.popleft()
        delay = clock - arrival_time
        statistics.delays_type1.append(delay)
        service_time = serve_type1(idx, server_type)
        statistics.waiting_times_type1.append(delay + service_time)
        return True
    return False


def try_serve_type2_from_queue(idx_A, idx_B):
    if queue_type2:
        arrival_time = queue_type2.popleft()
        delay = clock - arrival_time
        statistics.delays_type2.append(delay)
        service_time = serve_type2(idx_A, idx_B)
        statistics.waiting_times_type2.append(delay + service_time)
        return True
    return False


def arrival():
    """Handles arrival events, assigns customers to servers or queues."""
    global clock

    # Agendar próxima chegada
    interarrival = exponential(config.MEAN_INTERARRIVAL)
    schedule_event(clock + interarrival, "arrival")

    # Determinar tipo de cliente
    if random.random() < config.P_TYPE1:
        # Tipo 1
        idx_A = find_free_server(servers_A)
        if idx_A is not None:
            serve_type1(idx_A, "A")
        else:
            idx_B = find_free_server(servers_B)
            if idx_B is not None:
                serve_type1(idx_B, "B")
            else:
                queue_type1.append(clock)
    else:
        # Tipo 2
        idx_A = find_free_server(servers_A)
        idx_B = find_free_server(servers_B)
        if idx_A is not None and idx_B is not None:
            serve_type2(idx_A, idx_B)
        else:
            queue_type2.append(clock)


def departure_type1(info):
    """Handles departure events for type 1 customers and manages queue servicing."""
    server_type, server_idx = info

    if server_type == "A":
        servers_A[server_idx] = False
        server_A_type[server_idx] = None
    else:
        servers_B[server_idx] = False
        server_B_type[server_idx] = None

    idx_A = server_idx if server_type == "A" else find_free_server(servers_A)
    idx_B = server_idx if server_type == "B" else find_free_server(servers_B)
    if (
        idx_A is not None
        and idx_B is not None
        and try_serve_type2_from_queue(idx_A, idx_B)
    ):
        return
    if idx_A is not None and try_serve_type1_from_queue(idx_A, "A"):
        return
    if idx_B is not None and try_serve_type1_from_queue(idx_B, "B"):
        return


def departure_type2(indices):
    """Handles departure events for type 2 customers and manages queue servicing."""
    server_idx_A, server_idx_B = indices

    servers_A[server_idx_A] = False
    server_A_type[server_idx_A] = None
    servers_B[server_idx_B] = False
    server_B_type[server_idx_B] = None

    if try_serve_type2_from_queue(server_idx_A, server_idx_B):
        return
    if try_serve_type1_from_queue(server_idx_A, "A"):
        return


def simulate():
    init_state()

    """Runs the simulation until the specified simulation time is reached."""
    global clock, last_event_time
    global statistics

    # Início da simulação: agenda o primeiro evento de chegada
    schedule_event(0.0, "arrival")

    while event_list and clock < config.SIM_TIME:
        clock, event_type, data = heapq.heappop(event_list)
        if config.VERBOSE:
            print(f"[{clock:.2f}] Evento: {event_type}, dados: {data}")
        dt = clock - last_event_time
        statistics.area_num_in_queue_type1 += len(queue_type1) * dt
        statistics.area_num_in_queue_type2 += len(queue_type2) * dt

        num_in_service_type1 = sum(1 for t in server_A_type if t == "type1") + sum(
            1 for t in server_B_type if t == "type1"
        )
        num_in_system_type1 = len(queue_type1) + num_in_service_type1
        num_in_service_type2 = sum(
            1 for t in server_A_type if t == "type2"
        )  # same count as B
        num_in_system_type2 = len(queue_type2) + num_in_service_type2
        statistics.area_num_in_system_type1 += num_in_system_type1 * dt
        statistics.area_num_in_system_type2 += num_in_system_type2 * dt

        last_event_time = clock

        if event_type == "arrival":
            arrival()
        elif event_type == "departure_type1":
            departure_type1(data)
        elif event_type == "departure_type2":
            departure_type2(data)

    # Resultados
    statistics.report()

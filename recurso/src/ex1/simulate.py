from collections import deque
import heapq
import random
import config
import stats


def init_state():
    """
    Inicializa o estado da simulação.
    Inputs: Nenhum
    Returns: Nenhum
    """
    global servers_A, servers_B, server_A_type, server_B_type
    global queue_type1, queue_type2
    global clock, last_event_time
    global event_list

    servers_A = [False for _ in range(config.NUM_SERVERS_A)]
    servers_B = [False for _ in range(config.NUM_SERVERS_B)]

    server_A_type = [None for _ in range(config.NUM_SERVERS_A)]
    server_B_type = [None for _ in range(config.NUM_SERVERS_B)]

    stats.server_A_time_type1 = [0.0 for _ in range(config.NUM_SERVERS_A)]
    stats.server_A_time_type2 = [0.0 for _ in range(config.NUM_SERVERS_A)]
    stats.server_B_time_type1 = [0.0 for _ in range(config.NUM_SERVERS_B)]
    stats.server_B_time_type2 = [0.0 for _ in range(config.NUM_SERVERS_B)]

    queue_type1 = deque()
    queue_type2 = deque()

    clock = 0.0
    last_event_time = 0.0

    event_list = []


def schedule_event(time, event_type, data=None):
    """
    Adiciona um novo evento à lista de eventos futuros por ordem.
    Inputs:
        time: tempo em que o evento ocorrerá
        event_type: tipo do evento
        data: dados associados ao evento
    Returns: Nenhum
    """
    heapq.heappush(event_list, (time, event_type, data))


def exponential(mean):
    """
    Gera uma variável aleatória exponencial com a média fornecida.
    Inputs:
        mean: média da distribuição exponencial
    Returns:
        float: valor gerado da distribuição exponencial
    """
    return random.expovariate(1.0 / mean)


def uniform(a, b):
    """
    Gera uma variável aleatória uniforme entre a e b.
    Inputs:
        a: limite inferior
        b: limite superior
    Returns:
        float: valor gerado da distribuição uniforme
    """
    return random.uniform(a, b)


def find_free_server(servers):
    """
    Encontra o índice de um servidor livre na lista dada, ou None se nenhum estiver livre.
    Inputs:
        servers: lista indicando se cada servidor está ocupado
    Returns:
        índice do servidor livre ou None se nenhum disponível
    """
    for i, busy in enumerate(servers):
        if not busy:
            return i
    return None


def serve_type1(idx, server_type):
    """
    Atende um cliente do tipo 1 no servidor especificado e agenda a sua saída.
    Inputs:
        idx: índice do servidor
        server_type: tipo do servidor ("A" ou "B")
    Returns:
        tempo de serviço gerado para o atendimento
    """
    service_time = exponential(config.MEAN_SERVICE_TYPE1)
    if server_type == "A":
        servers_A[idx] = True
        server_A_type[idx] = "type1"
        stats.server_A_time_type1[idx] += service_time
    else:
        servers_B[idx] = True
        server_B_type[idx] = "type1"
        stats.server_B_time_type1[idx] += service_time
    schedule_event(clock + service_time, "departure_type1", (server_type, idx))
    return service_time


def serve_type2(idx_A, idx_B):
    """
    Atende um cliente do tipo 2 utilizando servidores A e B e agenda a sua saída.
    Inputs:
        idx_A: índice do servidor A
        idx_B: índice do servidor B
    Returns:
        tempo de serviço gerado para o atendimento
    """
    service_time = uniform(config.UNIF_SERVICE_TYPE2_MIN, config.UNIF_SERVICE_TYPE2_MAX)
    servers_A[idx_A] = True
    servers_B[idx_B] = True
    server_A_type[idx_A] = "type2"
    server_B_type[idx_B] = "type2"
    stats.server_A_time_type2[idx_A] += service_time
    stats.server_B_time_type2[idx_B] += service_time
    schedule_event(clock + service_time, "departure_type2", (idx_A, idx_B))
    return service_time


def try_serve_type1_from_queue(idx, server_type):
    """
    Tenta atender um cliente do tipo 1 da fila, se houver algum à espera.
    Inputs:
        idx: índice do servidor disponível
        server_type: tipo do servidor ("A" ou "B")
    Returns:
        True se um cliente foi atendido, False caso contrário
    """
    if queue_type1:
        arrival_time = queue_type1.popleft()
        delay = clock - arrival_time
        stats.delays_type1.append(delay)
        service_time = serve_type1(idx, server_type)
        stats.waiting_times_type1.append(delay + service_time)
        return True
    return False


def try_serve_type2_from_queue(idx_A, idx_B):
    """
    Tenta atender um cliente do tipo 2 da fila, se houver algum à espera.
    Inputs:
        idx_A: índice do servidor A disponível
        idx_B: índice do servidor B disponível
    Returns:
        True se um cliente foi atendido, False caso contrário
    """
    if queue_type2:
        arrival_time = queue_type2.popleft()
        delay = clock - arrival_time
        stats.delays_type2.append(delay)
        service_time = serve_type2(idx_A, idx_B)
        stats.waiting_times_type2.append(delay + service_time)
        return True
    return False


def arrival():
    """
    Trata eventos de chegada: atribui clientes a servidores ou filas conforme apropriado.
    Inputs: Nenhum
    Returns: Nenhum
    """
    global clock

    interarrival = exponential(config.MEAN_INTERARRIVAL)
    schedule_event(clock + interarrival, "arrival")

    if random.random() < config.P_TYPE1:
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
        idx_A = find_free_server(servers_A)
        idx_B = find_free_server(servers_B)
        if idx_A is not None and idx_B is not None:
            serve_type2(idx_A, idx_B)
        else:
            queue_type2.append(clock)


def departure_type1(info):
    """
    Trata eventos de saída para clientes do tipo 1 e gerencia o atendimento das filas.
    Inputs:
        info: tuple contendo tipo do servidor e índice
    Returns: Nenhum
    """
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
    """
    Trata eventos de saída para clientes do tipo 2 e gerencia o atendimento das filas.
    Inputs:
        indices: tupla contendo índices dos servidores A e B
    Returns: Nenhum
    """
    server_idx_A, server_idx_B = indices

    servers_A[server_idx_A] = False
    server_A_type[server_idx_A] = None
    servers_B[server_idx_B] = False
    server_B_type[server_idx_B] = None

    if try_serve_type2_from_queue(server_idx_A, server_idx_B):
        return
    if try_serve_type1_from_queue(server_idx_A, "A"):
        return


def update_stats(dt):
    """
    Atualiza estatísticas dependentes do tempo com base no tempo desde o último evento.
    Inputs:
        dt: intervalo de tempo desde o último evento
    Returns: Nenhum
    """
    stats.area_num_in_queue_type1 += len(queue_type1) * dt
    stats.area_num_in_queue_type2 += len(queue_type2) * dt

    num_in_service_type1 = sum(1 for t in server_A_type if t == "type1") + sum(
        1 for t in server_B_type if t == "type1"
    )
    num_in_system_type1 = len(queue_type1) + num_in_service_type1
    num_in_service_type2 = sum(1 for t in server_A_type if t == "type2")
    num_in_system_type2 = len(queue_type2) + num_in_service_type2

    stats.area_num_in_system_type1 += num_in_system_type1 * dt
    stats.area_num_in_system_type2 += num_in_system_type2 * dt


def simulate(print_stats=True):
    """
    Executa a simulação até que o tempo especificado seja alcançado.
    Inputs:
        print_stats: indica se as estatísticas devem ser impressas ao final (padrão: True)
    Returns: Nenhum
    """
    init_state()

    global clock, last_event_time
    global stats

    schedule_event(0.0, "arrival")

    while event_list and clock < config.SIM_TIME:
        clock, event_type, data = heapq.heappop(event_list)
        if config.VERBOSE:
            print(f"[{clock:.2f}] Evento: {event_type}, dados: {data}")
        dt = clock - last_event_time
        update_stats(dt)

        last_event_time = clock

        if event_type == "arrival":
            arrival()
        elif event_type == "departure_type1":
            departure_type1(data)
        elif event_type == "departure_type2":
            departure_type2(data)

    stats.report(print_stats)

import simpy
import random
import statistics
import config
import stats


def init_state():
    """
    Inicializa o estado da simulação (apenas acumuladores estatísticos para a versão SimPy).
    Inputs:
        Nenhum
    Returns:
        Nenhum
    """
    stats.delays_type1 = []
    stats.delays_type2 = []
    stats.waiting_times_type1 = []
    stats.waiting_times_type2 = []
    stats.area_num_in_queue_type1 = 0.0
    stats.area_num_in_queue_type2 = 0.0
    stats.area_num_in_system_type1 = 0.0
    stats.area_num_in_system_type2 = 0.0
    stats.server_A_time_type1 = [0.0 for _ in range(config.NUM_SERVERS_A)]
    stats.server_A_time_type2 = [0.0 for _ in range(config.NUM_SERVERS_A)]
    stats.server_B_time_type1 = [0.0 for _ in range(config.NUM_SERVERS_B)]
    stats.server_B_time_type2 = [0.0 for _ in range(config.NUM_SERVERS_B)]


def customer_arrivals(env, queue_type1, queue_type2):
    """
    Gera chegadas de clientes e coloca-os nas filas correspondentes.
    Inputs:
        env: ambiente de simulação SimPy
        queue_type1: fila para clientes do tipo 1
        queue_type2: fila para clientes do tipo 2
    Returns:
        Nenhum
    """
    while True:
        yield env.timeout(random.expovariate(1.0 / config.MEAN_INTERARRIVAL))
        arrival_time = env.now
        if random.random() < config.P_TYPE1:
            queue_type1.put(arrival_time)
        else:
            queue_type2.put(arrival_time)


def try_serve_from_queues(env, idx_A, idx_B, busy_A, busy_B, queue_type1, queue_type2):
    """
    Tenta servir clientes das filas, verificando disponibilidade dos servidores.
    Inputs:
        env: ambiente de simulação SimPy
        idx_A: índice do servidor A
        idx_B: índice do servidor B
        busy_A: lista indicando se servidores A estão ocupados
        busy_B: lista indicando se servidores B estão ocupados
        queue_type1: fila para clientes do tipo 1
        queue_type2: fila para clientes do tipo 2
    Returns:
        Nenhum
    """
    if not busy_A[idx_A] and not busy_B[idx_B] and len(queue_type2.items) > 0:
        busy_A[idx_A] = True
        busy_B[idx_B] = True
        arrival_time = yield queue_type2.get()
        yield env.process(serve_type2(env, idx_A, idx_B, arrival_time, busy_A, busy_B))
    elif not busy_A[idx_A] and len(queue_type1.items) > 0:
        busy_A[idx_A] = True
        arrival_time = yield queue_type1.get()
        yield env.process(serve_type1(env, idx_A, arrival_time, busy_A, "A"))
    elif not busy_B[idx_B] and len(queue_type1.items) > 0:
        busy_B[idx_B] = True
        arrival_time = yield queue_type1.get()
        yield env.process(serve_type1(env, idx_B, arrival_time, busy_B, "B"))


def serve_type1(env, server_idx, arrival_time, busy_list, server_type):
    """
    Serve um cliente do tipo 1 num servidor específico.
    Inputs:
        env: ambiente de simulação SimPy
        server_idx: índice do servidor
        arrival_time: tempo de chegada do cliente
        busy_list: lista indicando ocupação dos servidores correspondentes
        server_type: tipo do servidor ("A" ou "B")
    Returns:
        Nenhum
    """
    delay = env.now - arrival_time
    stats.delays_type1.append(delay)
    service_time = random.expovariate(1.0 / config.MEAN_SERVICE_TYPE1)
    yield env.timeout(service_time)
    stats.waiting_times_type1.append(delay + service_time)
    if server_type == "A":
        stats.server_A_time_type1[server_idx] += service_time
    else:
        stats.server_B_time_type1[server_idx] += service_time
    busy_list[server_idx] = False


def serve_type2(env, idx_A, idx_B, arrival_time, busy_A, busy_B):
    """
    Serve um cliente do tipo 2 utilizando servidores A e B.
    Inputs:
        env: ambiente de simulação SimPy
        idx_A: índice do servidor A
        idx_B: índice do servidor B
        arrival_time: tempo de chegada do cliente
        busy_A: lista indicando ocupação dos servidores A
        busy_B: lista indicando ocupação dos servidores B
    Returns:
        Nenhum
    """
    delay = env.now - arrival_time
    stats.delays_type2.append(delay)
    service_time = random.uniform(
        config.UNIF_SERVICE_TYPE2_MIN, config.UNIF_SERVICE_TYPE2_MAX
    )
    yield env.timeout(service_time)
    stats.waiting_times_type2.append(delay + service_time)
    stats.server_A_time_type2[idx_A] += service_time
    stats.server_B_time_type2[idx_B] += service_time
    busy_A[idx_A] = False
    busy_B[idx_B] = False


def scheduler(env, busy_A, busy_B, queue_type1, queue_type2):
    """
    Agenda o atendimento dos clientes nas filas, alocando servidores disponíveis.
    Inputs:
        env: ambiente de simulação SimPy
        busy_A: lista indicando ocupação dos servidores A
        busy_B: lista indicando ocupação dos servidores B
        queue_type1: fila para clientes do tipo 1
        queue_type2: fila para clientes do tipo 2
    Returns:
        Nenhum
    """
    while True:
        free_A = [i for i, b in enumerate(busy_A) if not b]
        free_B = [i for i, b in enumerate(busy_B) if not b]
        while free_A and free_B and len(queue_type2.items) > 0:
            idx_A = free_A.pop(0)
            idx_B = free_B.pop(0)
            busy_A[idx_A] = True
            busy_B[idx_B] = True
            arrival_time = yield queue_type2.get()
            env.process(serve_type2(env, idx_A, idx_B, arrival_time, busy_A, busy_B))

        for idx_A in [i for i, b in enumerate(busy_A) if not b]:
            if len(queue_type1.items) == 0:
                break
            busy_A[idx_A] = True
            arrival_time = yield queue_type1.get()
            env.process(serve_type1(env, idx_A, arrival_time, busy_A, "A"))

        for idx_B in [i for i, b in enumerate(busy_B) if not b]:
            if len(queue_type1.items) == 0:
                break
            busy_B[idx_B] = True
            arrival_time = yield queue_type1.get()
            env.process(serve_type1(env, idx_B, arrival_time, busy_B, "B"))

        yield env.timeout(0.1)


def monitor(env, queue_type1, queue_type2):
    """
    Monitora o sistema atualizando as estatísticas de tempo e número de clientes.
    Inputs:
        env: ambiente de simulação SimPy
        queue_type1: fila para clientes do tipo 1
        queue_type2: fila para clientes do tipo 2
    Returns:
        Nenhum
    """
    last_time = env.now
    while True:
        yield env.timeout(0.1)
        dt = env.now - last_time
        last_time = env.now

        stats.area_num_in_queue_type1 += len(queue_type1.items) * dt
        stats.area_num_in_queue_type2 += len(queue_type2.items) * dt

        num_in_service_type1 = sum(1 for t in stats.server_A_time_type1 if t > 0) + sum(
            1 for t in stats.server_B_time_type1 if t > 0
        )
        num_in_system_type1 = len(queue_type1.items) + num_in_service_type1

        num_in_service_type2 = sum(1 for t in stats.server_A_time_type2 if t > 0)
        num_in_system_type2 = len(queue_type2.items) + num_in_service_type2

        stats.area_num_in_system_type1 += num_in_system_type1 * dt
        stats.area_num_in_system_type2 += num_in_system_type2 * dt


def simulate_simpy(print_stats=True):
    """
    Executa a simulação utilizando SimPy e gera relatório estatístico.
    Inputs:
        print_stats: indica se os resultados devem ser impressos
    Returns:
        Nenhum
    """
    init_state()

    env = simpy.Environment()
    queue_type1 = simpy.Store(env)
    queue_type2 = simpy.Store(env)

    busy_A = [False] * config.NUM_SERVERS_A
    busy_B = [False] * config.NUM_SERVERS_B

    env.process(customer_arrivals(env, queue_type1, queue_type2))
    env.process(monitor(env, queue_type1, queue_type2))

    env.process(scheduler(env, busy_A, busy_B, queue_type1, queue_type2))

    env.run(until=config.SIM_TIME)

    stats.report(print_stats)

import simpy
import random
import statistics

# python exercise1.py

# Parâmetros da simulação
RANDOM_SEED = 42
SIM_TIME = 160            # Tempo de simulação (horas)
MEAN_INTERARRIVAL = 2.0   # Tempo médio entre chegadas (horas)
INSPECTION_TIME_MIN = 0.25  # Tempo mínimo de inspeção (15 min = 0.25 h)
INSPECTION_TIME_MAX = 1.05  # Tempo máximo de inspeção (horas)
REPAIR_TIME_MIN = 2.1       # Tempo mínimo de reparo (horas)
REPAIR_TIME_MAX = 4.5       # Tempo máximo de reparo (horas)
REPAIR_PROB = 0.3         # Probabilidade de um autocarro necessitar de reparo

# Listas para estatísticas
inspection_wait_times = []  # tempos de espera na fila de inspeção
repair_wait_times = []      # tempos de espera na fila de reparo

# Para calcular comprimento médio das filas, faremos amostragem periódica
inspection_queue_lengths = []
repair_queue_lengths = []

class InspectionStation:
    def __init__(self, env):
        self.env = env
        self.resource = simpy.Resource(env, capacity=1)
        self.busy_time = 0.0  # acumula o tempo em que a estação está ocupada

    def inspect(self, bus_id):
        service_time = random.uniform(INSPECTION_TIME_MIN, INSPECTION_TIME_MAX)
        yield self.env.timeout(service_time)
        self.busy_time += service_time

class RepairStation:
    def __init__(self, env):
        self.env = env
        self.resource = simpy.Resource(env, capacity=2)
        self.busy_time = 0.0  # soma o tempo de serviço de ambas as estações

    def repair(self, bus_id):
        service_time = random.uniform(REPAIR_TIME_MIN, REPAIR_TIME_MAX)
        yield self.env.timeout(service_time)
        self.busy_time += service_time

def bus(env, bus_id, inspection_station, repair_station):
    # Chegada do autocarro
    arrival_time = env.now

    # Atendimento na inspeção
    with inspection_station.resource.request() as req:
        yield req
        # Tempo de espera na fila de inspeção
        wait_inspection = env.now - arrival_time
        inspection_wait_times.append(wait_inspection)
        # Processo de inspeção
        yield env.process(inspection_station.inspect(bus_id))

    # Verifica se necessita de reparo (30% dos casos)
    if random.random() < REPAIR_PROB:
        repair_arrival = env.now
        with repair_station.resource.request() as req:
            yield req
            wait_repair = env.now - repair_arrival
            repair_wait_times.append(wait_repair)
            yield env.process(repair_station.repair(bus_id))

def bus_arrivals(env, inspection_station, repair_station):
    bus_id = 0
    while True:
        bus_id += 1
        env.process(bus(env, f'Autocarro {bus_id}', inspection_station, repair_station))
        # Gerar o tempo até a próxima chegada (distribuição exponencial)
        interarrival = random.expovariate(1.0 / MEAN_INTERARRIVAL)
        yield env.timeout(interarrival)

def monitor_queues(env, inspection_station, repair_station, sample_interval=0.1):
    """Processo para amostrar periodicamente o comprimento das filas."""
    while True:
        inspection_queue_lengths.append(len(inspection_station.resource.queue))
        repair_queue_lengths.append(len(repair_station.resource.queue))
        yield env.timeout(sample_interval)

def run_simulation():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    inspection_station = InspectionStation(env)
    repair_station = RepairStation(env)
    
    # Inicia os processos: chegada de autocarros e monitoramento das filas
    env.process(bus_arrivals(env, inspection_station, repair_station))
    env.process(monitor_queues(env, inspection_station, repair_station))
    env.run(until=SIM_TIME)
    
    # Cálculo dos tempos médios de espera
    avg_inspection_wait = statistics.mean(inspection_wait_times) if inspection_wait_times else 0.0
    avg_repair_wait = statistics.mean(repair_wait_times) if repair_wait_times else 0.0
    
    # Comprimento médio aproximado das filas (amostragem)
    avg_inspection_queue = statistics.mean(inspection_queue_lengths) if inspection_queue_lengths else 0.0
    avg_repair_queue = statistics.mean(repair_queue_lengths) if repair_queue_lengths else 0.0
    
    # Utilização: razão entre o tempo total de serviço e o tempo de simulação.
    util_inspection = inspection_station.busy_time / SIM_TIME
    # Para as estações de reparo (2 unidades), a utilização é:
    util_repair = repair_station.busy_time / (2 * SIM_TIME)
    
    print("=== Resultados da Simulação (160 horas) ===")
    print(f"Tempo médio de espera na fila de inspeção: {avg_inspection_wait:.3f} horas")
    print(f"Tempo médio de espera na fila de reparo: {avg_repair_wait:.3f} horas")
    print(f"Comprimento médio da fila de inspeção: {avg_inspection_queue:.3f}")
    print(f"Comprimento médio da fila de reparo: {avg_repair_queue:.3f}")
    print(f"Utilização da estação de inspeção: {util_inspection:.3f}")
    print(f"Utilização das estações de reparo: {util_repair:.3f}")

if __name__ == '__main__':
    run_simulation()
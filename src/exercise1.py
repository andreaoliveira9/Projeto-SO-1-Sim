import simpy
import random
import statistics

# Execution example:
# python exercise1.py

# Simulation Parameters (Constants)
RANDOM_SEED = 42
SIMULATION_TIME = 160  # Total simulation time in hours
MEAN_INTERARRIVAL = 2.0  # Mean interarrival time (hours)
INSPECTION_TIME_MIN = 0.25  # Minimum inspection duration (hours)
INSPECTION_TIME_MAX = 1.05  # Maximum inspection duration (hours)
REPAIR_TIME_MIN = 2.1  # Minimum repair duration (hours)
REPAIR_TIME_MAX = 4.5  # Maximum repair duration (hours)
REPAIR_PROB = 0.3  # Probability that a bus requires repair

# Global lists for statistics
inspection_wait_times = []  # Waiting times for inspection
repair_wait_times = []  # Waiting times for repair
inspection_queue_lengths = []  # Sampled lengths of the inspection queue
repair_queue_lengths = []  # Sampled lengths of the repair queue


class InspectionStation:
    """
    Represents an inspection station with a single service resource.
    """

    def __init__(self, env):
        self.env = env
        self.resource = simpy.Resource(env, capacity=1)
        self.busy_time = 0.0  # Total time the station is occupied

    def inspect(self, bus_id):
        """
        Process for inspecting a bus.
        :param bus_id: Identifier of the bus.
        """
        service_time = random.uniform(INSPECTION_TIME_MIN, INSPECTION_TIME_MAX)
        yield self.env.timeout(service_time)
        self.busy_time += service_time


class RepairStation:
    """
    Represents a repair station with two service resources.
    """

    def __init__(self, env):
        self.env = env
        self.resource = simpy.Resource(env, capacity=2)
        self.busy_time = 0.0  # Combined busy time for both repair units

    def repair(self, bus_id):
        """
        Process for repairing a bus.
        :param bus_id: Identifier of the bus.
        """
        service_time = random.uniform(REPAIR_TIME_MIN, REPAIR_TIME_MAX)
        yield self.env.timeout(service_time)
        self.busy_time += service_time


def bus(env, bus_id, inspection_station, repair_station):
    """
    Process representing a bus undergoing inspection and, if necessary, repair.
    :param env: The simulation environment.
    :param bus_id: Identifier for the bus.
    :param inspection_station: Instance of InspectionStation.
    :param repair_station: Instance of RepairStation.
    """
    arrival_time = env.now

    # Inspection Phase
    with inspection_station.resource.request() as req:
        yield req
        wait_time = env.now - arrival_time
        inspection_wait_times.append(wait_time)
        yield env.process(inspection_station.inspect(bus_id))

    # Decide whether the bus needs repair based on probability
    if random.random() < REPAIR_PROB:
        repair_arrival_time = env.now
        with repair_station.resource.request() as req:
            yield req
            repair_wait = env.now - repair_arrival_time
            repair_wait_times.append(repair_wait)
            yield env.process(repair_station.repair(bus_id))


def bus_generator(env, inspection_station, repair_station):
    """
    Generates buses at intervals following an exponential distribution.
    :param env: The simulation environment.
    :param inspection_station: Instance of InspectionStation.
    :param repair_station: Instance of RepairStation.
    """
    bus_count = 0
    while True:
        bus_count += 1
        env.process(bus(env, f"Bus {bus_count}", inspection_station, repair_station))
        interarrival_time = random.expovariate(1.0 / MEAN_INTERARRIVAL)
        yield env.timeout(interarrival_time)


def monitor_queues(env, inspection_station, repair_station, sample_interval=0.1):
    """
    Periodically samples the lengths of inspection and repair queues.
    :param env: The simulation environment.
    :param inspection_station: Instance of InspectionStation.
    :param repair_station: Instance of RepairStation.
    :param sample_interval: Time interval between samples.
    """
    while True:
        inspection_queue_lengths.append(len(inspection_station.resource.queue))
        repair_queue_lengths.append(len(repair_station.resource.queue))
        yield env.timeout(sample_interval)


def run_simulation():
    """
    Sets up and executes the simulation, then prints collected statistics.
    """
    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    # Create service stations
    inspection_station = InspectionStation(env)
    repair_station = RepairStation(env)

    # Initiate processes: bus arrivals and queue monitoring
    env.process(bus_generator(env, inspection_station, repair_station))
    env.process(monitor_queues(env, inspection_station, repair_station))
    env.run(until=SIMULATION_TIME)

    # Compute average waiting times
    avg_inspection_wait = (
        statistics.mean(inspection_wait_times) if inspection_wait_times else 0.0
    )
    avg_repair_wait = statistics.mean(repair_wait_times) if repair_wait_times else 0.0

    # Compute average queue lengths
    avg_inspection_queue = (
        statistics.mean(inspection_queue_lengths) if inspection_queue_lengths else 0.0
    )
    avg_repair_queue = (
        statistics.mean(repair_queue_lengths) if repair_queue_lengths else 0.0
    )

    # Calculate resource utilization
    utilization_inspection = inspection_station.busy_time / SIMULATION_TIME
    utilization_repair = repair_station.busy_time / (2 * SIMULATION_TIME)

    print("=== Simulation Results (160 hours) ===")
    print(f"Average wait time for inspection: {avg_inspection_wait:.3f} hours")
    print(f"Average wait time for repair: {avg_repair_wait:.3f} hours")
    print(f"Average queue length at inspection: {avg_inspection_queue:.3f}")
    print(f"Average queue length at repair: {avg_repair_queue:.3f}")
    print(f"Inspection station utilization: {utilization_inspection:.3f}")
    print(f"Repair station utilization: {utilization_repair:.3f}")


if __name__ == "__main__":
    run_simulation()

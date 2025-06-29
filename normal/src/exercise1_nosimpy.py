import random
import statistics
from typing import Any
import random
import statistics
import heapq
from typing import List, Dict, Any, Callable

# Simulation Parameters (Constants)
RANDOM_SEED: int = 42
SIMULATION_TIME: float = 160.0  # Total simulation time in hours
MEAN_INTERARRIVAL: float = 2.0  # Mean interarrival time (hours)
INSPECTION_CAPACITY: int = 1  # Capacity of the inspection station
INSPECTION_TIME_MIN: float = 0.25  # Minimum inspection duration (hours)
INSPECTION_TIME_MAX: float = 1.05  # Maximum inspection duration (hours)
REPAIR_CAPACITY: int = 2  # Capacity of the repair station
REPAIR_TIME_MIN: float = 2.1  # Minimum repair duration (hours)
REPAIR_TIME_MAX: float = 4.5  # Maximum repair duration (hours)
REPAIR_PROB: float = 0.3  # Probability that a bus requires repair


# Global statistics
inspection_wait_times: List[float] = []
repair_wait_times: List[float] = []
inspection_queue_lengths: List[int] = []
repair_queue_lengths: List[int] = []
inspection_queue: List[Dict[str, Any]] = []
repair_queue: List[Dict[str, Any]] = []
inspection_busy: int = 0
repair_busy: int = 0
total_inspection_service: float = 0.0
total_repair_service: float = 0.0


def convert_hours_to_hms(hours: float) -> str:
    total_seconds = int(hours * 3600)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h}h:{m}m:{s}s"


def schedule_event(
    event_list: List[Any], time: float, event_type: str, data: Dict[str, Any]
) -> None:
    heapq.heappush(event_list, (time, event_type, data))


# --- Modular event handlers and statistics ---
def handle_arrival(event_list: List[Any], current_time: float, bus_count: int) -> int:
    """Process a bus arrival event, schedule inspection or enqueue."""
    global inspection_busy, total_inspection_service
    bus_count += 1
    bus_id = f"Bus {bus_count}"
    # Schedule next arrival
    next_arrival = current_time + random.expovariate(1.0 / MEAN_INTERARRIVAL)
    schedule_event(event_list, next_arrival, "arrival", {})
    # Attempt inspection
    if inspection_busy < INSPECTION_CAPACITY:
        inspection_wait_times.append(0.0)
        service_time = random.uniform(INSPECTION_TIME_MIN, INSPECTION_TIME_MAX)
        total_inspection_service += service_time
        inspection_busy += 1
        schedule_event(
            event_list,
            current_time + service_time,
            "end_inspection",
            {"bus_id": bus_id},
        )
    else:
        inspection_queue.append({"bus_id": bus_id, "arrival_time": current_time})
    return bus_count


def handle_end_inspection(
    event_list: List[Any], current_time: float, data: Dict[str, Any]
) -> None:
    """Process end of inspection, possibly start repair or next inspection."""
    global inspection_busy, total_inspection_service, repair_busy, total_repair_service
    bus_id = data["bus_id"]
    inspection_busy -= 1
    # Start next inspection if queued
    if inspection_queue:
        nxt = inspection_queue.pop(0)
        wait = current_time - nxt["arrival_time"]
        inspection_wait_times.append(wait)
        service_time = random.uniform(INSPECTION_TIME_MIN, INSPECTION_TIME_MAX)
        total_inspection_service += service_time
        inspection_busy += 1
        schedule_event(
            event_list,
            current_time + service_time,
            "end_inspection",
            {"bus_id": nxt["bus_id"]},
        )
    # Decide on repair
    if random.random() < REPAIR_PROB:
        if repair_busy < REPAIR_CAPACITY:
            repair_wait_times.append(0.0)
            service_time = random.uniform(REPAIR_TIME_MIN, REPAIR_TIME_MAX)
            total_repair_service += service_time
            repair_busy += 1
            schedule_event(
                event_list,
                current_time + service_time,
                "end_repair",
                {"bus_id": bus_id},
            )
        else:
            repair_queue.append({"bus_id": bus_id, "arrival_time": current_time})


def handle_end_repair(
    event_list: List[Any], current_time: float, data: Dict[str, Any]
) -> None:
    """Process end of repair, start next repair if queued."""
    global repair_busy, total_repair_service
    repair_busy -= 1
    if repair_queue:
        nxt = repair_queue.pop(0)
        wait = current_time - nxt["arrival_time"]
        repair_wait_times.append(wait)
        service_time = random.uniform(REPAIR_TIME_MIN, REPAIR_TIME_MAX)
        total_repair_service += service_time
        repair_busy += 1
        schedule_event(
            event_list,
            current_time + service_time,
            "end_repair",
            {"bus_id": nxt["bus_id"]},
        )


def calculate_statistics() -> Dict[str, float]:
    """Compute averages and utilization metrics."""
    avg_inspection_wait = (
        statistics.mean(inspection_wait_times) if inspection_wait_times else 0.0
    )
    avg_repair_wait = statistics.mean(repair_wait_times) if repair_wait_times else 0.0
    avg_inspection_queue = (
        statistics.mean(inspection_queue_lengths) if inspection_queue_lengths else 0.0
    )
    avg_repair_queue = (
        statistics.mean(repair_queue_lengths) if repair_queue_lengths else 0.0
    )
    utilization_inspection = (
        total_inspection_service / (INSPECTION_CAPACITY * SIMULATION_TIME) * 100
    )
    utilization_repair = (
        total_repair_service / (REPAIR_CAPACITY * SIMULATION_TIME) * 100
    )
    return {
        "avg_inspection_wait": avg_inspection_wait,
        "avg_repair_wait": avg_repair_wait,
        "avg_inspection_queue": avg_inspection_queue,
        "avg_repair_queue": avg_repair_queue,
        "utilization_inspection": utilization_inspection,
        "utilization_repair": utilization_repair,
    }


def report(stats: Dict[str, float]) -> None:
    """Print the simulation report based on collected statistics."""
    print("=== Simulation Report ===")
    print(
        f"Average wait time for inspection: {convert_hours_to_hms(stats['avg_inspection_wait'])}"
    )
    print(
        f"Average wait time for repair: {convert_hours_to_hms(stats['avg_repair_wait'])}"
    )
    print(f"Average queue length at inspection: {stats['avg_inspection_queue']:.3f}")
    print(f"Average queue length at repair: {stats['avg_repair_queue']:.3f}")
    print(f"Inspection station utilization: {stats['utilization_inspection']:.3f} %")
    print(f"Repair station utilization: {stats['utilization_repair']:.3f} %")


# Mapping of event types to their handler functions (excluding 'sample')
EVENT_HANDLERS: Dict[str, Callable[..., Any]] = {
    "arrival": handle_arrival,
    "end_inspection": handle_end_inspection,
    "end_repair": handle_end_repair,
}


def run_simulation() -> None:
    global inspection_busy, repair_busy, total_inspection_service, total_repair_service
    random.seed(RANDOM_SEED)
    current_time: float = 0.0
    event_list: List[Any] = []
    # Schedule first arrival
    schedule_event(
        event_list, random.expovariate(1.0 / MEAN_INTERARRIVAL), "arrival", {}
    )

    bus_count: int = 0

    while event_list:
        time, event_type, data = heapq.heappop(event_list)
        if time > SIMULATION_TIME:
            break
        current_time = time

        # Record queue length metrics on every event
        inspection_queue_lengths.append(len(inspection_queue))
        repair_queue_lengths.append(len(repair_queue))

        if event_type == "arrival":
            bus_count = handle_arrival(event_list, current_time, bus_count)

        elif event_type == "end_inspection":
            handle_end_inspection(event_list, current_time, data)

        elif event_type == "end_repair":
            handle_end_repair(event_list, current_time, data)

    # Final reporting
    stats = calculate_statistics()
    report(stats)


if __name__ == "__main__":
    run_simulation()

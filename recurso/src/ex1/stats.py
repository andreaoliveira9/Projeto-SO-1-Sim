delays_type1 = []
delays_type2 = []
waiting_times_type1 = []
waiting_times_type2 = []
area_num_in_queue_type1 = 0.0
area_num_in_queue_type2 = 0.0
area_num_in_system_type1 = 0.0
area_num_in_system_type2 = 0.0
server_A_time_type1 = []
server_A_time_type2 = []
server_B_time_type1 = []
server_B_time_type2 = []


def format_time(minutes):
    """
    Converte um tempo em minutos para uma string formatada com horas, minutos e segundos.
    Inputs:
        minutes: tempo em minutos
    Returns:
        string formatada do tempo (por exemplo: "1h 2m 3s")
    """
    h = int(minutes // 60)
    m = int(minutes % 60)
    s = int((minutes - int(minutes)) * 60)
    return f"{h}h {m}m {s}s"


def report(print_stats=True):
    """
    Imprime um relatório com estatísticas da simulação.
    Inputs:
        print_stats: se True, imprime os resultados no terminal
    Returns: Nenhum
    """
    import config

    global area_num_in_queue_type1, area_num_in_queue_type2
    global delays_type1, delays_type2
    global waiting_times_type1, waiting_times_type2
    global area_num_in_system_type1, area_num_in_system_type2
    global server_A_time_type1, server_A_time_type2, server_B_time_type1, server_B_time_type2

    mean_delay_type1 = sum(delays_type1) / len(delays_type1) if delays_type1 else 0
    mean_delay_type2 = sum(delays_type2) / len(delays_type2) if delays_type2 else 0
    mean_waiting_time_type1 = (
        sum(waiting_times_type1) / len(waiting_times_type1)
        if waiting_times_type1
        else 0
    )
    mean_waiting_time_type2 = (
        sum(waiting_times_type2) / len(waiting_times_type2)
        if waiting_times_type2
        else 0
    )
    mean_area_num_in_queue_type1 = area_num_in_queue_type1 / config.SIM_TIME
    mean_area_num_in_queue_type2 = area_num_in_queue_type2 / config.SIM_TIME
    mean_num_in_system_type1 = area_num_in_system_type1 / config.SIM_TIME
    mean_num_in_system_type2 = area_num_in_system_type2 / config.SIM_TIME

    if print_stats == False:
        return

    print(
        "\n---------------------------- Simulation Report ----------------------------"
    )
    print(
        f"Steady-state average delay - Type 1: {format_time(mean_delay_type1)}, Type 2: {format_time(mean_delay_type2)}"
    )
    print(
        f"Steady-state average waiting time - Type 1: {format_time(mean_waiting_time_type1)}, Type 2: {format_time(mean_waiting_time_type2)}"
    )
    print(
        f"Steady-state average number in queue - Type 1: {mean_area_num_in_queue_type1:.2f}, Type 2: {mean_area_num_in_queue_type2:.2f}"
    )
    print(
        f"Steady-state average number in system - Type 1: {mean_num_in_system_type1:.2f}, Type 2: {mean_num_in_system_type2:.2f}"
    )

    print("\nServer utilization:")
    for i in range(len(server_A_time_type1)):
        perc1 = 100 * server_A_time_type1[i] / config.SIM_TIME
        perc2 = 100 * server_A_time_type2[i] / config.SIM_TIME
        print(f"\tServer A{i+1} - Type 1: {perc1:.2f}%, Type 2: {perc2:.2f}%")

    for i in range(len(server_B_time_type1)):
        perc1 = 100 * server_B_time_type1[i] / config.SIM_TIME
        perc2 = 100 * server_B_time_type2[i] / config.SIM_TIME
        print(f"\tServer B{i+1} - Type 1: {perc1:.2f}%, Type 2: {perc2:.2f}%")
    print(
        "---------------------------------------------------------------------------\n"
    )

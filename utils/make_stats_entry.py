# utils/make_stats_entry.py

def make_stats_entry(data, pid, arrival, burst, completion):
    """
    Create a statistics entry for a single process.

    Computes turnaround time, waiting time, and normalized turnaround time.

    Args:
        data (dict): Original process data in the format {pid: [arrival, burst, priority]}.
        pid (str): Process ID.
        arrival (float): Arrival time of the process.
        burst (float): CPU burst time of the process.
        completion (float): Completion time of the process.

    Returns:
        dict: A dictionary containing the following keys:
            - "arrival" (float): Arrival time.
            - "burst" (float): CPU burst time.
            - "priority" (int): Process priority (0 if not in `data`).
            - "completion" (float): Completion time.
            - "turnaround" (float): Turnaround time = completion - arrival.
            - "waiting" (float): Waiting time = turnaround - burst.
            - "norm_turnaround" (float): Normalized turnaround time = turnaround / burst.
    """
    
    turn_around_time = completion - arrival
    waiting_time = turn_around_time - burst
    norm_turn_around_time = turn_around_time / burst if burst > 0 else 0
    return {
        "arrival": arrival,
        "burst": burst,
        "priority": data[pid][2] if pid in data else 0,
        "completion": completion,
        "turnaround": turn_around_time,
        "waiting": waiting_time,
        "norm_turnaround": norm_turn_around_time
    }

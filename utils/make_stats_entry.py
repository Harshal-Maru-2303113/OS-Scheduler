# utils/make_stats_entry.py

def make_stats_entry(data, pid, arrival, burst, completion):

    
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

# algorithm/hpf.py

from utils.make_stats_entry import make_stats_entry

def hpf(data, context_switch=0.0):
    """
    Non-preemptive Highest Priority First (HPF) scheduling algorithm.
    
    Higher numeric priority is chosen first. If priorities tie, earlier arrival wins, 
    then lower PID breaks tie. 

    Args:
        data (dict): Dictionary of processes with structure {pid: (arrival, burst, priority)}
        context_switch (float, optional): Context switch duration between processes. Defaults to 0.0.

    Returns:
        tuple:
            timeline (list): List of dictionaries with CPU activity/idle/context switch events.
                Each dict contains:
                    - "start": float, start time of the block
                    - "duration": float, duration of the block
                    - "pid": str or None, process id or None for idle/context switch
                    - "type": "proc" | "idle" | "cs"
            stats (dict): Dictionary of per-process statistics with structure {pid: {...}}
                Each entry includes arrival, burst, completion, waiting, turnaround, norm_turnaround, priority.
    """
    
    # Sort processes by arrival time, then PID
    sorted_data = sorted(data.items(), key=lambda kv: (kv[1][0], int(kv[0])))
    
    timeline = []
    stats = {}
    current_time = sorted_data[0][1][0] if sorted_data else 0.0
    ready = []
    
    # if empty, return early
    if not sorted_data:
        return timeline, stats
    
    i = 0
    n = len(sorted_data)
    
    while i < n or ready:
        # Enqueue all processes that have arrived
        while i < n and sorted_data[i][1][0] <= current_time:
            ready.append(sorted_data[i])
            i += 1

        if not ready:
            # CPU idle until next arrival
            next_arrival = sorted_data[i][1][0]
            timeline.append({
                "start": current_time,
                "duration": next_arrival - current_time,
                "pid": None,
                "type": "idle"
            })
            current_time = next_arrival
            continue

        # Pick process with highest priority (larger numeric value)
        ready.sort(key=lambda kv: (-kv[1][2], kv[1][0], int(kv[0])))
        pid, (arrival, burst, _) = ready.pop(0)
        arrival, burst = float(arrival), float(burst)

        # Add idle time if process arrived after current time
        if arrival > current_time:
            timeline.append({
                "start": current_time,
                "duration": arrival - current_time,
                "pid": None,
                "type": "idle"
            })
            current_time = arrival

        # Schedule the process
        timeline.append({
            "start": current_time,
            "duration": burst,
            "pid": pid,
            "type": "proc"
        })
        current_time += burst

        # Record stats
        stats[pid] = make_stats_entry(data, pid, arrival, burst, current_time)

        # Context switch block
        if context_switch:
            timeline.append({
                "start": current_time,
                "duration": context_switch,
                "pid": None,
                "type": "cs"
            })
            current_time += context_switch

    return timeline, stats

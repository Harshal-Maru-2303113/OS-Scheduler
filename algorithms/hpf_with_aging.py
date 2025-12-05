#algorithm/hpf_with_aging.py
from utils.make_stats_entry import make_stats_entry

def hpf_with_aging(data, context_switch=0.0, aging_interval=3, aging_increment=0):
    
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

        # Apply aging to priorities
        aged_ready = [(pid, (arrival, burst, pr+int(aging_increment*((current_time - arrival)/aging_interval)))) for pid, (arrival, burst, pr) in ready]
        # Pick process with highest priority (larger numeric value)
        aged_ready.sort(key=lambda kv: (-kv[1][2], kv[1][0], int(kv[0])))
        pid, (arrival, burst, _) = aged_ready.pop(0)
        # Remove selected process from ready list
        ready = [proc for proc in ready if proc[0] != pid]
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
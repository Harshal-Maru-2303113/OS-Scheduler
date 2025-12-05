# algorithms/lottery.py
from utils.make_stats_entry import make_stats_entry
import random

def lottery(data, quantum, context_switch=0.0):

    # Sort by arrival time first, then PID
    sorted_data = sorted(data.items(), key=lambda kv: (kv[1][0], int(kv[0])))

    timeline = []
    stats = {}
    n = len(sorted_data)
    if n == 0:
        return timeline, stats

    ready = []
    current_time = sorted_data[0][1][0]
    i = 0

    while i < n or ready:
        # Add all processes that have arrived by current time
        while i < n and sorted_data[i][1][0] <= current_time:
            ready.append(sorted_data[i])
            i += 1

        # If no ready process, CPU idles until next arrival
        if not ready:
            if i < n:
                next_process = sorted_data[i][1][0]
                timeline.append({
                    "start": current_time,
                    "duration": next_process - current_time,
                    "pid": None,
                    "type": "idle"
                })
                current_time = next_process
                continue
            break

        # Lottery selection
        total_tickets = sum([pr for _, (_, _, pr) in ready])
        winning_ticket = random.randint(1, total_tickets)
        ticket_counter = 0
        for idx, (pid, (arrival, burst, pr)) in enumerate(ready):
            ticket_counter += pr
            if ticket_counter >= winning_ticket:
                selected_process = ready.pop(idx)
                break

        pid, (arrival, burst, pr) = selected_process
        step = min(burst, quantum)
        # Context switch time
        if context_switch > 0.0 and timeline and timeline[-1]['pid'] != pid:
            timeline.append({
                "start": current_time,
                "duration": context_switch,
                "pid": None,
                "type": "cs"
            })
            current_time += context_switch

        # Execute the selected process
        timeline.append({
            "start": current_time,
            "duration": step,
            "pid": pid,
            "type": "proc"
        })
        current_time += step
        
        if(burst > step):
            # Process not finished, re-add to ready queue with updated burst time
            ready.append((pid, (arrival, burst - step, pr)))

        # Record stats
        completion_time = current_time
        stats[pid] = make_stats_entry(data, pid, arrival, step, completion_time)

    return timeline, stats
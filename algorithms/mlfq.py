# algorithms/mlfq.py

from collections import deque
from utils.make_stats_entry import make_stats_entry

def mlfq(data, levels=3, quanta_list=None, context_switch=0.0, aging_threshold=10.0):


    if quanta_list is None:
        quanta_list = [1 * (2 ** i) for i in range(levels)]

    # Ensure quanta list matches levels
    while len(quanta_list) < levels:
        quanta_list.append(quanta_list[-1] * 2)

    # Sort input data: (arrival_time, burst_time, priority)
    sorted_data = sorted(data.items(), key=lambda kv: (kv[1][0], int(kv[0])))
    timeline, stats = [], {}
    if not sorted_data:
        return timeline, stats

    remaining = {pid: float(burst) for pid, (_, burst, _) in sorted_data}
    arrival = {pid: float(arr) for pid, (arr, _, _) in sorted_data}
    last_active = {pid: arrival[pid] for pid in remaining}

    queues = [deque() for _ in range(levels)]
    current_time = sorted_data[0][1][0]
    i, n = 0, len(sorted_data)

    # Enqueue initial arrivals
    while i < n and sorted_data[i][1][0] <= current_time:
        queues[0].append(sorted_data[i][0])
        i += 1

    while any(queues) or i < n:
        # Add new arrivals
        while i < n and sorted_data[i][1][0] <= current_time:
            queues[0].append(sorted_data[i][0])
            last_active[sorted_data[i][0]] = current_time
            i += 1

        # Apply aging: promote if waiting too long
        for lvl in range(1, levels):
            promoted = []
            for pid in list(queues[lvl]):
                if current_time - last_active[pid] >= aging_threshold:
                    queues[lvl].remove(pid)
                    queues[lvl - 1].append(pid)
                    promoted.append(pid)
                    last_active[pid] = current_time
            if promoted:
                print(f"Aged up: {promoted}")

        # Find first non-empty queue
        cur_level = next((L for L in range(levels) if queues[L]), None)
        if cur_level is None:
            if i < n:
                next_arr = sorted_data[i][1][0]
                timeline.append({"start": current_time, 
                                 "duration": next_arr - current_time, 
                                 "pid": None, 
                                 "type": "idle"})
                current_time = next_arr
                continue
            break

        # Choose process based on queue algorithm
        if cur_level == 0:
            # Round Robin
            pid = queues[cur_level].popleft()
        elif cur_level == 1:
            # Shortest Remaining Time Next (SRTN)
            pid = min(queues[cur_level], key=lambda p: remaining[p])
            queues[cur_level].remove(pid)
        else:
            # FCFS
            pid = queues[cur_level].popleft()

        quantum = quanta_list[cur_level]
        exec_time = min(remaining[pid], quantum)
        timeline.append({"start": current_time, 
                         "duration": exec_time, 
                         "pid": pid, 
                         "type": "proc", 
                         "level": cur_level})
        current_time += exec_time
        remaining[pid] -= exec_time

        # Track last activity for aging
        last_active[pid] = current_time

        # New arrivals during execution
        while i < n and sorted_data[i][1][0] <= current_time:
            queues[0].append(sorted_data[i][0])
            last_active[sorted_data[i][0]] = current_time
            i += 1

        # Process completion or demotion
        if remaining[pid] <= 1e-9:
            stats[pid] = make_stats_entry(data, pid, arrival[pid], float(data[pid][1]), current_time)
        else:
            new_level = min(levels - 1, cur_level + 1)
            queues[new_level].append(pid)

        # Context switch
        if context_switch and any(queues):
            timeline.append({"start": current_time, 
                             "duration": context_switch, 
                             "pid": None, 
                             "type": "cs"})
            current_time += context_switch

    return timeline, stats

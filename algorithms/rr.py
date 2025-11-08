# algorithms/rr.py

from collections import deque
from utils.make_stats_entry import make_stats_entry

def rr(data, quantum=1.0, context_switch=0.0):
    """
    Round Robin (RR) CPU scheduling algorithm (preemptive).

    Args:
        data (dict): Dictionary of processes with structure {pid: (arrival, burst, priority)}.
        quantum (float): Maximum CPU time a process can run per turn.
        context_switch (float): Time taken for context switching between processes.

    Returns:
        tuple: (timeline, stats)
            - timeline (list of dicts): Each dict contains {"start", "duration", "pid", "type"}.
              'type' is "proc" for running process, "idle" for CPU idle, "cs" for context switch.
            - stats (dict): Per-process statistics {pid: {"arrival", "burst", "priority", "completion",
              "turnaround", "waiting", "norm_turnaround"}}.
    """
    
    # Sort processes by arrival time (tie-break by PID)
    sorted_data = sorted(data.items(), key=lambda kv: (kv[1][0], int(kv[0])))
    
    timeline = []
    stats = {}
    
    # if empty, return early
    if not sorted_data:
        return timeline, stats

    # Remaining burst times and arrival mapping
    remaining = {pid: float(burst) for pid, (_, burst, _) in sorted_data}
    arrival_map = {pid: float(arr) for pid, (arr, _, _) in sorted_data}

    current_time = sorted_data[0][1][0]
    
    q = deque()
    i = 0
    n = len(sorted_data)

    # Seed initial arrivals
    while i < n and sorted_data[i][1][0] <= current_time:
        q.append(sorted_data[i][0])
        i += 1

    # If nothing arrived yet, jump to the first arrival
    if not q and i < n:
        current_time = sorted_data[i][1][0]
        q.append(sorted_data[i][0])
        i += 1

    # Main RR loop
    while q:
        pid = q.popleft()
        run_time = min(quantum, remaining[pid])

        # Handle CPU idle if process arrived in future
        if arrival_map[pid] > current_time:
            timeline.append({"start": current_time,
                             "duration": arrival_map[pid] - current_time,
                             "pid": None,
                             "type": "idle"})
            current_time = arrival_map[pid]

        # Run the process
        timeline.append({"start": current_time,
                         "duration": run_time,
                         "pid": pid,
                         "type": "proc"})
        
        current_time += run_time
        remaining[pid] -= run_time

        # Enqueue any new arrivals during this time slice
        while i < n and sorted_data[i][1][0] <= current_time:
            q.append(sorted_data[i][0])
            i += 1

        # If process not finished, requeue
        if remaining[pid] > 1e-12:
            q.append(pid)
        else:
            # Process finished: record stats
            stats[pid] = make_stats_entry(data, pid, arrival_map[pid], float(data[pid][1]), current_time)

        # Add context switch if needed and queue not empty
        if context_switch and q:
            timeline.append({"start": current_time, "duration": context_switch, "pid": None, "type": "cs"})
            current_time += context_switch

        # If queue empty but there are future arrivals, jump to next arrival
        if not q and i < n:
            current_time = sorted_data[i][1][0]
            q.append(sorted_data[i][0])
            i += 1

    return timeline, stats

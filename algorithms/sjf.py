# algorithms/sjf.py

from utils.make_stats_entry import make_stats_entry


def sjf(data, context_switch=0.0):
    """
    Implements the Shortest Job First (SJF) scheduling algorithm (non-preemptive).

    - Among the ready processes, the one with the smallest burst time is selected.
    - Once a process starts execution, it runs to completion (no preemption).
    - Ties are broken by PID for determinism.

    Args:
        data (dict): Process dictionary in the format:
                     {pid: (arrival_time, burst_time, priority)}
        context_switch (float, optional): Context switch overhead in time units. Defaults to 0.0.

    Returns:
        tuple: (timeline, stats)
            - timeline (list): List of execution/idle/context switch periods
            - stats (dict): Per-process statistics (waiting, turnaround, etc.)
    """

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
                next_arr = sorted_data[i][1][0]
                timeline.append({
                    "start": current_time,
                    "duration": next_arr - current_time,
                    "pid": None,
                    "type": "idle"
                })
                current_time = next_arr
                continue
            break

        # Pick the process with the shortest burst time
        ready.sort(key=lambda kv: (kv[1][1], int(kv[0])))
        pid, (arrival, burst, pr) = ready.pop(0)
        arrival = float(arrival)
        burst = float(burst)

        # Execute it
        if arrival > current_time:
            timeline.append({
                "start": current_time,
                "duration": arrival - current_time,
                "pid": None,
                "type": "idle"
            })
            current_time = arrival

        timeline.append({
            "start": current_time,
            "duration": burst,
            "pid": pid,
            "type": "proc"
        })
        current_time += burst

        # Record stats
        stats[pid] = make_stats_entry(data, pid, arrival, burst, current_time)

        # Optional context switch
        if context_switch and (ready or i < n):
            timeline.append({
                "start": current_time,
                "duration": context_switch,
                "pid": None,
                "type": "cs"
            })
            current_time += context_switch

    return timeline, stats

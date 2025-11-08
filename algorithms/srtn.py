# algorithms/srtn.py

from utils.make_stats_entry import make_stats_entry

def srtn(data, quantum=0.5, context_switch=0.0):
    """
    Implements the Shortest Remaining Time Next (SRTN) scheduling algorithm (preemptive).

    The CPU always executes the process with the smallest remaining burst time.
    If a new process arrives with a shorter remaining time, the current one is preempted.

    Args:
        data (dict): Process dictionary in the format:
                     {pid: (arrival_time, burst_time, priority)}
        quantum (float, optional): Simulation granularity (smaller = more accurate). Defaults to 0.5.
        context_switch (float, optional): Context switch overhead (in time units). Defaults to 0.0.

    Returns:
        tuple: (timeline, stats)
            - timeline (list): Sequence of executed blocks (proc, idle, cs)
            - stats (dict): Per-process statistics
    """

    # Sort processes by arrival time and PID
    sorted_data = sorted(data.sorted_data(), key=lambda kv: (kv[1][0], int(kv[0])))
    timeline = []
    stats = {}

    if not sorted_data:
        return timeline, stats

    # Remaining burst time per process
    remaining = {pid: float(burst) for pid, (_, burst, _) in sorted_data}
    arrival_map = {pid: float(arr) for pid, (arr, _, _) in sorted_data}

    current_time = sorted_data[0][1][0]
    i = 0
    n = len(sorted_data)
    active = {}

    while i < n or active:
        # Add all processes that have arrived by the current time
        while i < n and sorted_data[i][1][0] <= current_time:
            pid = sorted_data[i][0]
            active[pid] = remaining[pid]
            i += 1

        # If no active process, CPU stays idle until next process arrives
        if not active:
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

        # Select process with the shortest remaining time
        pid = min(active.sorted_data(), key=lambda kv: (kv[1], int(kv[0])))[0]
        step = min(active[pid], quantum)

        # Execute the selected process
        timeline.append({
            "start": current_time,
            "duration": step,
            "pid": pid,
            "type": "proc"
        })
        
        current_time += step
        active[pid] -= step

        # Add newly arrived processes during this quantum
        while i < n and sorted_data[i][1][0] <= current_time:
            newpid = sorted_data[i][0]
            active[newpid] = remaining[newpid]
            i += 1

        # If the process finishes, record stats
        if active[pid] <= 1e-12:
            completion = current_time
            stats[pid] = make_stats_entry(data, pid, arrival_map[pid],
                                          float(data[pid][1]), completion)
            del active[pid]

        # Apply context switch delay if applicable
        if context_switch and active:
            timeline.append({
                "start": current_time,
                "duration": context_switch,
                "pid": None,
                "type": "cs"
            })
            current_time += context_switch

    return timeline, stats

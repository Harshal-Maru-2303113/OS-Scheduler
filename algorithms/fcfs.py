# algorithms/fcfs.py

from utils.make_stats_entry import make_stats_entry

def fcfs(data, context_switch=0.0):
    """
    First-Come, First-Served (FCFS) scheduling algorithm.

    Processes are executed in the order of arrival times. If multiple
    processes have the same arrival time, the tie is broken by PID
    (ascending numerical order). Supports optional context switch time.

    Args:
        data (dict): Mapping of process ID -> [arrival(float), burst(float), priority(int)]
        context_switch (float, optional): Time taken for context switching between processes. Defaults to 0.0.

    Returns:
        tuple:
            timeline (list of dict): Execution segments with keys:
                - 'start': segment start time
                - 'duration': segment duration
                - 'pid': process ID (None for idle or context switch)
                - 'type': 'proc', 'idle', or 'cs'
            stats (dict): Process statistics mapping PID -> {
                'arrival', 'burst', 'priority', 'completion', 'turnaround', 'waiting', 'norm_turnaround'
            }
    """

    # Sort processes by arrival time, breaking ties by PID
    sorted_data = sorted(data.items(), key=lambda kv: (kv[1][0], int(kv[0])))

    timeline = []
    stats = {}
    current_time = 0.0

    # if empty, return early
    if not sorted_data:
        return timeline, stats

    for pid, (arrival, burst, _) in sorted_data:
        # Convert arrival and burst to float
        arrival = float(arrival)
        burst = float(burst)

        # If the CPU is idle until this process arrives
        if arrival > current_time:
            timeline.append({
                "start": current_time,
                "duration": arrival - current_time,
                "pid": None,
                "type": "idle"
            })
            current_time = arrival

        # Run the process
        timeline.append({
            "start": current_time,
            "duration": burst,
            "pid": pid,
            "type": "proc"
        })
        current_time += burst
        completion = current_time

        # Record process statistics
        stats[pid] = make_stats_entry(data, pid, arrival, burst, completion)

        # Context switch after process if specified
        if context_switch:
            timeline.append({
                "start": current_time,
                "duration": context_switch,
                "pid": None,
                "type": "cs"
            })
            current_time += context_switch

    return timeline, stats

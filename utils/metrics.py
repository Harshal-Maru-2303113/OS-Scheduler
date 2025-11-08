"""
Metrics computation and statistics display
"""
from tkinter import END
from datetime import datetime


def compute_metrics(stats):
    """Compute aggregate metrics from process statistics"""
    if not stats:
        return {}
    
    pcount = len(stats)
    earliest_arrival = min(v['arrival'] for v in stats.values())
    latest_completion = max(v['completion'] for v in stats.values())
    total_time = latest_completion - earliest_arrival if pcount > 0 else 0.0
    cpu_time = sum(v['burst'] for v in stats.values())
    cpu_util = (cpu_time / total_time * 100.0) if total_time > 0 else 0.0
    
    total_wait = sum(v['waiting'] for v in stats.values())
    total_turn = sum(v['turnaround'] for v in stats.values())
    avg_wait = total_wait / pcount if pcount > 0 else 0.0
    avg_turn = total_turn / pcount if pcount > 0 else 0.0
    throughput = pcount / total_time if total_time > 0 else 0.0
    
    return {
        'pcount': pcount,
        'total_time': total_time,
        'cpu_time': cpu_time,
        'cpu_util': cpu_util,
        'avg_wait': avg_wait,
        'avg_turn': avg_turn,
        'throughput': throughput
    }


def show_stats_summary(stats_text, last_stats, algo, context, quantum):
    """Display statistics summary in the text widget"""
    stats_text.delete("1.0", END)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stats_text.insert(END, f"Run at: {now}\n")
    stats_text.insert(END, f"Algorithm: {algo} | Quantum: {quantum} | Context switch: {context}\n")
    stats_text.insert(END, "-"*72 + "\n")
    
    if not last_stats:
        stats_text.insert(END, "No processes finished (empty stats)\n")
        return

    # compute aggregates
    metrics = compute_metrics(last_stats)

    # brief table header
    hdr = f"{'PID':>4} {'Arr':>7} {'Burst':>7} {'Pr':>4} {'Compl':>8} {'Wait':>7} {'Turn':>7} {'N-Turn':>8}\n"
    stats_text.insert(END, hdr)
    stats_text.insert(END, "-"*72 + "\n")
    
    for pid, v in sorted(last_stats.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else kv[0]):
        stats_text.insert(END, f"{str(pid):>4} {v['arrival']:7.2f} {v['burst']:7.2f} {v['priority']:4d} {v['completion']:8.2f} {v['waiting']:7.2f} {v['turnaround']:7.2f} {v['norm_turnaround']:8.2f}\n")
    
    stats_text.insert(END, "-"*72 + "\n")
    stats_text.insert(END, f"Processes: {metrics['pcount']}  Total time: {metrics['total_time']:.3f}  CPU time: {metrics['cpu_time']:.3f}\n")
    stats_text.insert(END, f"Avg waiting: {metrics['avg_wait']:.3f}  Avg turnaround: {metrics['avg_turn']:.3f}  CPU util: {metrics['cpu_util']:.1f}%  Throughput: {metrics['throughput']:.3f} per unit time\n")
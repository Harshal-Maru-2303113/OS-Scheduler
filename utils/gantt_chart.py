"""
Gantt chart plotting utilities
"""
import random


def plot_gantt(ax, canvas, timeline, stats):
    """Plot Gantt chart on the given matplotlib axis"""
    ax.clear()
    if not timeline:
        ax.set_title("No timeline to show")
        canvas.draw()
        return

    # Compute unique pid order for vertical placement (stable order: numeric ascending)
    pids = sorted({seg['pid'] for seg in timeline if seg['pid'] is not None and seg['type']=="proc"},
                  key=lambda x: int(x) if str(x).isdigit() else x)
    pid_to_y = {pid: idx * 10 for idx, pid in enumerate(pids)}  # row height spacing 10
    height = 6

    # Colors mapping for processes
    random.seed(0)
    color_map = {}
    for pid in pids:
        # deterministic color per pid
        color_map[pid] = (random.random()*0.7 + 0.15, random.random()*0.7 + 0.15, random.random()*0.7 + 0.15)

    # Plot each segment using broken_barh
    for seg in timeline:
        start = seg['start']
        dur = seg['duration']
        typ = seg['type']
        pid = seg['pid']
        if typ == "proc":
            y = pid_to_y[pid]
            color = color_map.get(pid, (0.2,0.6,0.8))
            ax.broken_barh([(start, dur)], (y, height), facecolors=color, edgecolor="black")
            # label the bar with pid if wide enough
            if dur > 0.5:
                ax.text(start + dur/2, y + height/2, str(pid), ha='center', va='center', fontsize=8, color='black')
        elif typ == "idle":
            # represent idle below the rows
            ax.broken_barh([(start, dur)], (-12, 2), facecolors=(0.9,0.9,0.9), edgecolor="none")
        elif typ == "cs":
            # context switch smaller bar between rows
            ax.broken_barh([(start, dur)], (-8, 2), facecolors=(0.7,0.7,0.7), edgecolor="none")

    # Y ticks
    yticks = [pid_to_y[pid] + height/2 for pid in pids]
    ylabels = [str(pid) for pid in pids]
    if yticks:
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    # set x-limits to cover timeline fully
    start_min = min(seg['start'] for seg in timeline)
    end_max = max(seg['start'] + seg['duration'] for seg in timeline)
    ax.set_xlim(left=max(0, start_min - 0.5), right=end_max + 0.5)
    canvas.draw()
"""
Event handlers for UI interactions
"""
from tkinter import *
from tkinter import messagebox, filedialog
from datetime import datetime
import time
import random

from utils.gantt_chart import plot_gantt
from utils.metrics import compute_metrics, show_stats_summary


class EventHandlers:
    def __init__(self, app):
        self.app = app

    def load_input_file(self):
        path = filedialog.askopenfilename(title="Select input file", filetypes=[("Text files","*.txt"), ("All files","*.*")])
        if not path:
            return
        self.app.path_var.set(path)
        loaded = {}
        try:
            with open(path, "r") as f:
                lines = [ln.strip() for ln in f.readlines() if ln.strip()]
            start = 0
            if lines and (lines[0].isdigit() or lines[0].lower().startswith("process")):
                start = 1
            for ln in lines[start:]:
                parts = ln.split()
                if len(parts) >= 3:
                    pid = str(parts[0])
                    arrival = float(parts[1])
                    burst = float(parts[2])
                    pr = int(parts[3]) if len(parts) >= 4 else 0
                    loaded[pid] = [arrival, burst, pr]
            self.app.data = loaded
            self.refresh_tree()
            messagebox.showinfo("Loaded", f"Loaded {len(self.app.data)} processes from file.")
        except Exception as e:
            messagebox.showerror("Load error", f"Failed to load file: {e}")

    def export_input(self):
        if not self.app.data:
            messagebox.showwarning("No data", "No processes to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if not path:
            return
        try:
            with open(path, "w") as f:
                f.write("Process Count : " + str(len(self.app.data)) + "\n")
                for pid in sorted(self.app.data.keys(), key=lambda x: int(x) if str(x).isdigit() else x):
                    arr,bus,pr = self.app.data[pid]
                    f.write(f"{pid}\t{arr}\t{bus}\t{pr}\n")
            messagebox.showinfo("Exported", f"Input exported to {path}")
        except Exception as e:
            messagebox.showerror("Export error", str(e))

    def load_sample_input(self):
        sample = {
            "1": [0.0, 4.0, 1],
            "2": [1.0, 3.0, 2],
            "3": [2.0, 1.0, 3],
            "4": [3.0, 2.0, 2]
        }
        self.app.data = sample
        self.refresh_tree()

    def refresh_tree(self):
        for r in self.app.tree.get_children():
            self.app.tree.delete(r)
        for pid in sorted(self.app.data.keys(), key=lambda x: int(x) if str(x).isdigit() else x):
            arr,bus,pr = self.app.data[pid]
            self.app.tree.insert("", "end", values=(str(pid), str(arr), str(bus), str(pr)))

    def add_process_from_entries(self):
        pid = self.app.controls_frame.pid_entry.get().strip()
        arr = self.app.controls_frame.arrival_entry.get().strip()
        burst = self.app.controls_frame.burst_entry.get().strip()
        pr = self.app.controls_frame.prio_entry.get().strip() or "0"


        if not pid or not arr or not burst:
            messagebox.showerror("Input Error", "Please fill PID, Arrival and Burst.")
            return

        try:
            arrival = float(arr)
            burst = float(burst)
            priority = int(pr)
        except Exception:
            messagebox.showerror("Type Error", "Arrival and Burst must be numbers; Priority must be an integer.")
            return

        # Check if PID exists
        if pid in self.app.data:
            if not messagebox.askyesno("Update PID?", f"PID {pid} exists. Update its values?"):
                return

        # Add/update process
        self.app.data[pid] = [arrival, burst, priority]

        # Refresh treeview
        self.refresh_tree()

        # Clear entry fields
        self.app.controls_frame.pid_entry.delete(0, END)
        self.app.controls_frame.arrival_entry.delete(0, END)
        self.app.controls_frame.burst_entry.delete(0, END)
        self.app.controls_frame.prio_entry.delete(0, END)
        self.app.controls_frame.pid_entry.focus_set()

        # Optional: focus on PID entry for convenience
        self.app.controls_frame.pid_entry.focus_set()

    def remove_selected(self):
        sel = self.app.tree.selection()
        if not sel:
            return
        for i in sel:
            pid = self.app.tree.item(i, "values")[0]
            self.app.data.pop(str(pid), None)
        self.refresh_tree()

    def reset_all(self):
        self.app.data.clear()
        self.app.last_stats = {}
        self.app.last_timeline = []
        self.refresh_tree()
        self.app.ax.clear()
        self.app.canvas.draw()
        self.app.stats_text.delete("1.0", END)
        self.app.path_var.set("No file selected")
        messagebox.showinfo("Reset", "Application state reset.")

    def generate_processes(self):
        controls = self.app.controls_frame
        try:
            n = int(controls.gen_n_var.get())
            arr_min, arr_max = map(float, controls.gen_arr_var.get().split(","))
            burst_min, burst_max = map(float, controls.gen_burst_var.get().split(","))
            pr_min, pr_max = map(int, controls.gen_prio_var.get().split(","))
            seed = controls.gen_seed_var.get()
            if seed:
                random.seed(int(seed))
            else:
                random.seed(time.time())
            generated = {}
            for i in range(1, n+1):
                pid = str(i)
                arrival = round(random.uniform(arr_min, arr_max), 2)
                burst = round(random.uniform(burst_min, burst_max), 2)
                prio = random.randint(pr_min, pr_max)
                generated[pid] = [arrival, burst, prio]
            self.app.data = generated
            self.refresh_tree()
            messagebox.showinfo("Generated", f"{n} processes generated successfully.")
        except Exception as e:
            messagebox.showerror("Generation error", f"Failed to generate processes:\n{e}")

    def run_and_plot(self):
        if not self.app.data:
            messagebox.showerror("No data", "Please load or add processes first.")
            return
        try:
            # Lazy import to break circular dependency
            from scheduler import Scheduler
        except ImportError as e:
            messagebox.showerror("Internal Error", f"Cannot load Scheduler:\n{e}")
            return

        algo = self.app.algorithm_var.get()
        if algo not in ("HPF","FCFS","RR","SRTN","MLFQ","SJF"):
            messagebox.showerror("Select algorithm", "Please select an algorithm.")
            return
        try:
            context = float(self.app.context_var.get())
        except Exception:
            context = 0.0
        try:
            quantum = float(self.app.quantum_var.get())
        except Exception:
            quantum = 1.0

        sched = Scheduler(self.app.data)
        timeline = []
        stats = {}
        try:
            if algo == "FCFS":
                timeline, stats = sched.fcfs(context_switch=context)
            elif algo == "HPF":
                timeline, stats = sched.hpf(context_switch=context)
            elif algo == "RR":
                timeline, stats = sched.rr(quantum=quantum, context_switch=context)
            elif algo == "SRTN":
                timeline, stats = sched.srtn(quantum=quantum, context_switch=context)
            elif algo == "SJF":
                timeline, stats = sched.sjf(context_switch=context)
            elif algo == "MLFQ":
                levels = max(1, int(self.app.mlfq_levels_var.get()) if self.app.mlfq_levels_var.get().isdigit() else 3)
                raw = self.app.mlfq_quanta_var.get().split(",")
                quanta = []
                for r in raw:
                    try:
                        quanta.append(float(r.strip()))
                    except Exception:
                        pass
                while len(quanta) < levels:
                    quanta.append(quanta[-1] if quanta else 1.0)
                timeline, stats = sched.mlfq(levels=levels, quanta_list=quanta, context_switch=context)
        except Exception as e:
            messagebox.showerror("Algorithm error", f"Error while running algorithm:\n{e}")
            return

        self.app.last_timeline = timeline
        self.app.last_stats = stats

        plot_gantt(self.app.ax, self.app.canvas, timeline, stats)
        show_stats_summary(self.app.stats_text, self.app.last_stats, algo, context, quantum)

    def write_report(self):
        if not self.app.last_stats:
            messagebox.showwarning("No run", "Please run a scheduling simulation first.")
            return
        path = self.app.output_path_var.get() or "Out.txt"
        try:
            with open(path, "w") as f:
                f.write("OS Scheduler Simulation Report\n")
                f.write("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                f.write(f"Algorithm: {self.app.algorithm_var.get()}\n")
                f.write(f"Quantum: {self.app.quantum_var.get()}  Context-switch: {self.app.context_var.get()}\n")
                f.write("-"*80 + "\n")
                f.write(f"{'PID':>4} {'Arrival':>8} {'Burst':>8} {'Pr':>4} {'Completion':>10} {'Waiting':>9} {'Turnaround':>11} {'N-Turn':>8}\n")
                f.write("-"*80 + "\n")
                pcount = len(self.app.last_stats)
                earliest_arrival = min(v['arrival'] for v in self.app.last_stats.values())
                latest_completion = max(v['completion'] for v in self.app.last_stats.values())
                total_time = latest_completion - earliest_arrival if pcount > 0 else 0.0
                cpu_time = sum(v['burst'] for v in self.app.last_stats.values())
                for pid, v in sorted(self.app.last_stats.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else kv[0]):
                    f.write(f"{str(pid):>4} {v['arrival']:8.2f} {v['burst']:8.2f} {v['priority']:4d} {v['completion']:10.2f} {v['waiting']:9.2f} {v['turnaround']:11.2f} {v['norm_turnaround']:8.2f}\n")
                f.write("-"*80 + "\n")
                total_wait = sum(v['waiting'] for v in self.app.last_stats.values())
                total_turn = sum(v['turnaround'] for v in self.app.last_stats.values())
                avg_wait = total_wait / pcount if pcount > 0 else 0.0
                avg_turn = total_turn / pcount if pcount > 0 else 0.0
                cpu_util = (cpu_time / total_time * 100.0) if total_time > 0 else 0.0
                throughput = pcount / total_time if total_time > 0 else 0.0
                f.write(f"Processes: {pcount}\n")
                f.write(f"Total time (makespan): {total_time:.4f}\n")
                f.write(f"CPU busy time: {cpu_time:.4f}\n")
                f.write(f"CPU utilization: {cpu_util:.2f}%\n")
                f.write(f"Avg waiting time: {avg_wait:.4f}\n")
                f.write(f"Avg turnaround time: {avg_turn:.4f}\n")
                f.write(f"Throughput: {throughput:.6f} processes/unit time\n")
            messagebox.showinfo("Saved", f"Report saved to {path}")
        except Exception as e:
            messagebox.showerror("Save error", f"Failed to write report:\n{e}")

from tkinter import Tk
from ui.main_window import SchedulerApp
from algorithms.fcfs import fcfs
from algorithms.hpf import hpf
from algorithms.rr import rr
from algorithms.srtn import srtn
from algorithms.mlfq import mlfq
from algorithms.sjf import sjf

class Scheduler:
    def __init__(self, processes):
        self.processes = processes

    def fcfs(self, context_switch=0):
        return fcfs(self.processes, context_switch)

    def hpf(self, context_switch=0):
        return hpf(self.processes, context_switch)

    def rr(self, quantum=1, context_switch=0):
        return rr(self.processes, quantum, context_switch)

    def srtn(self, quantum=1, context_switch=0):
        return srtn(self.processes, quantum, context_switch)

    def mlfq(self, levels=3, quanta_list=None, context_switch=0):
        if quanta_list is None:
            quanta_list = [1,2,4]
        return mlfq(self.processes, levels, quanta_list, context_switch)

    def sjf(self,context_switch=0):
        return sjf(self.processes,context_switch)

def main():
    root = Tk()
    app = SchedulerApp(root)  # UI only
    root.mainloop()

if __name__ == "__main__":
    main()

from tkinter import *
from tkinter import ttk
from ui.controls import ControlsFrame
from ui.events import EventHandlers
from utils.gantt_chart import plot_gantt
from utils.metrics import show_stats_summary
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SchedulerApp:
    def __init__(self, master):
        self.master = master
        master.title("OS Scheduler Visualizer — Refined UI")
        master.geometry("1600x1024")
        
        # Data
        self.data = {}
        self.last_timeline = []
        self.last_stats = {}
        
        # Left frame: controls
        left_frame = Frame(master)
        left_frame.pack(side=LEFT, fill=Y, padx=8, pady=8)
        self.controls_frame = ControlsFrame(left_frame, self)
        
        # Right frame: plots & stats
        right_frame = Frame(master)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=8, pady=8)
        
        # Figure & canvas
        self.figure = Figure(figsize=(7,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        plot_frame = ttk.LabelFrame(right_frame, text="Gantt Chart / Timeline", padding=6)
        plot_frame.pack(fill=BOTH, expand=True)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Stats text
        stats_frame = ttk.LabelFrame(right_frame, text="Last Run Statistics", padding=6)
        stats_frame.pack(fill=X, pady=(8,0))
        self.stats_text = Text(stats_frame, height=8, wrap="word", font=("Consolas",10))
        self.stats_text.pack(fill=BOTH, expand=True)
        
        # Event handlers
        self.event_handlers = EventHandlers(self)
        
        # Expose controls as attributes (so EventHandlers can access them directly)
        self.algorithm_var    = self.controls_frame.algorithm_var
        self.quantum_var      = self.controls_frame.quantum_var
        self.context_var      = self.controls_frame.context_var
        self.mlfq_levels_var  = self.controls_frame.mlfq_levels_var
        self.mlfq_quanta_var  = self.controls_frame.mlfq_quanta_var
        self.path_var         = self.controls_frame.path_var
        self.output_path_var  = self.controls_frame.output_path_var
        self.tree             = self.controls_frame.tree
    
    # Delegate actions to event handlers
    def load_input_file(self):
        self.event_handlers.load_input_file()
    
    def export_input(self):
        self.event_handlers.export_input()
    
    def load_sample_input(self):
        self.event_handlers.load_sample_input()
    
    def refresh_tree(self):
        self.event_handlers.refresh_tree()
    
    def add_process_from_entries(self):
        self.event_handlers.add_process_from_entries()
    
    def remove_selected(self):
        self.event_handlers.remove_selected()
    
    def reset_all(self):
        self.event_handlers.reset_all()
    
    def generate_processes(self):
        self.event_handlers.generate_processes()
    
    def run_and_plot(self):
        self.event_handlers.run_and_plot()
    
    def write_report(self):
        self.event_handlers.write_report()
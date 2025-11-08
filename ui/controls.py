from tkinter import *
from tkinter import ttk

class ControlsFrame:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # -------- Scheduling Settings --------
        sched_frame = ttk.LabelFrame(parent, text="Scheduling Settings", padding=10)
        sched_frame.pack(fill=X, pady=(0,10))

        ttk.Label(sched_frame, text="Algorithm:").grid(row=0, column=0, sticky="w")
        self.algorithm_var = StringVar(value="SELECT")
        ttk.OptionMenu(sched_frame, self.algorithm_var, "SELECT", "SJF", "HPF", "FCFS", "RR", "SRTN", "MLFQ").grid(row=0, column=1, sticky="w", padx=(6,12))

        ttk.Label(sched_frame, text="Quantum:").grid(row=1, column=0, sticky="w", pady=(4,0))
        self.quantum_var = StringVar(value="1")
        ttk.Entry(sched_frame, textvariable=self.quantum_var, width=8).grid(row=1, column=1, sticky="w", padx=(6,12), pady=(4,0))

        ttk.Label(sched_frame, text="Context Switch:").grid(row=2, column=0, sticky="w", pady=(4,0))
        self.context_var = StringVar(value="0")
        ttk.Entry(sched_frame, textvariable=self.context_var, width=8).grid(row=2, column=1, sticky="w", padx=(6,12), pady=(4,0))

        # -------- MLFQ Settings --------
        mlfq_frame = ttk.LabelFrame(parent, text="MLFQ Settings", padding=10)
        mlfq_frame.pack(fill=X, pady=(0,10))

        ttk.Label(mlfq_frame, text="Levels:").grid(row=0, column=0, sticky="w")
        self.mlfq_levels_var = StringVar(value="3")
        ttk.Entry(mlfq_frame, textvariable=self.mlfq_levels_var, width=6).grid(row=0, column=1, sticky="w", padx=(6,12))

        ttk.Label(mlfq_frame, text="Quanta (comma):").grid(row=1, column=0, sticky="w", pady=(4,0))
        self.mlfq_quanta_var = StringVar(value="1,2,4")
        ttk.Entry(mlfq_frame, textvariable=self.mlfq_quanta_var, width=16).grid(row=1, column=1, sticky="w", padx=(6,12), pady=(4,0))

        # -------- Input Generator --------
        gen_frame = ttk.LabelFrame(parent, text="Input Generator", padding=10)
        gen_frame.pack(fill=X, pady=(0,10))

        ttk.Label(gen_frame, text="# Processes:").grid(row=0, column=0, sticky="w")
        self.gen_n_var = StringVar(value="5")
        ttk.Entry(gen_frame, textvariable=self.gen_n_var, width=6).grid(row=0, column=1, sticky="w", padx=(6,12))

        ttk.Label(gen_frame, text="Arrival (min,max):").grid(row=1, column=0, sticky="w", pady=(2,0))
        self.gen_arr_var = StringVar(value="0,10")
        ttk.Entry(gen_frame, textvariable=self.gen_arr_var, width=12).grid(row=1, column=1, sticky="w", padx=(6,12))

        ttk.Label(gen_frame, text="Burst (min,max):").grid(row=2, column=0, sticky="w", pady=(2,0))
        self.gen_burst_var = StringVar(value="1,10")
        ttk.Entry(gen_frame, textvariable=self.gen_burst_var, width=12).grid(row=2, column=1, sticky="w", padx=(6,12))

        ttk.Label(gen_frame, text="Priority (min,max):").grid(row=3, column=0, sticky="w", pady=(2,0))
        self.gen_prio_var = StringVar(value="1,5")
        ttk.Entry(gen_frame, textvariable=self.gen_prio_var, width=12).grid(row=3, column=1, sticky="w", padx=(6,12))

        ttk.Label(gen_frame, text="Random Seed:").grid(row=4, column=0, sticky="w", pady=(2,0))
        self.gen_seed_var = StringVar(value="")
        ttk.Entry(gen_frame, textvariable=self.gen_seed_var, width=12).grid(row=4, column=1, sticky="w", padx=(6,12))

        ttk.Button(gen_frame, text="🞂 Generate Processes", command=lambda: app.generate_processes()).grid(row=5, column=0, columnspan=2, pady=(6,0))

        # -------- I/O and Actions --------
        io_frame = ttk.LabelFrame(parent, text="Input / Output & Actions", padding=10)
        io_frame.pack(fill=X, pady=(0,10))

        self.path_var = StringVar(value="No file selected")
        ttk.Button(io_frame, text="📂 Load Input File", command=lambda: app.load_input_file()).grid(row=0, column=0, sticky="w", padx=(0,8))
        ttk.Label(io_frame, textvariable=self.path_var).grid(row=0, column=1, sticky="w")

        ttk.Label(io_frame, text="Output path:").grid(row=1, column=0, sticky="w", pady=(4,0))
        self.output_path_var = StringVar(value="Out.txt")
        ttk.Entry(io_frame, textvariable=self.output_path_var, width=24).grid(row=1, column=1, sticky="w", pady=(4,0))
        ttk.Button(io_frame, text="💾 Save Report", command=lambda: app.write_report()).grid(row=1, column=2, padx=(6,0), pady=(4,0))

        ttk.Button(io_frame, text="▶ Run & Show Graph", command=lambda: app.run_and_plot()).grid(row=2, column=0, pady=(6,0))
        ttk.Button(io_frame, text="⟲ Reset", command=lambda: app.reset_all()).grid(row=2, column=1)
        ttk.Button(io_frame, text="📤 Export Input", command=lambda: app.export_input()).grid(row=3, column=0, pady=(6,0))
        ttk.Button(io_frame, text="📄 Load Sample", command=lambda: app.load_sample_input()).grid(row=3, column=1, pady=(6,0))

        # -------- Process Table --------
        proc_frame = ttk.LabelFrame(parent, text="Processes Table", padding=10)
        proc_frame.pack(fill=BOTH, expand=True, pady=(0,10))

        cols = ("pid", "arrival", "burst", "priority")
        self.tree = ttk.Treeview(proc_frame, columns=cols, show="headings", height=12, selectmode="extended")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=80, anchor="center")

        scrollbar = ttk.Scrollbar(proc_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True)

        # Process entry + buttons
        addfrm = Frame(proc_frame)
        addfrm.pack(fill=X, pady=(4,0))
        for lbl, var_width in [("PID",6),("Arrival",8),("Burst",8),("Prio",6)]:
            Label(addfrm, text=lbl).pack(side=LEFT, padx=(2,4))
            entry = Entry(addfrm, width=var_width)
            setattr(self, f"{lbl.lower()}_entry", entry)
            entry.pack(side=LEFT, padx=(0,8))

        ttk.Button(addfrm, text="➕ Add / Update", command=lambda: app.add_process_from_entries()).pack(side=LEFT, padx=(6,0))
        ttk.Button(addfrm, text="❌ Remove Selected", command=lambda: app.remove_selected()).pack(side=LEFT, padx=(6,0))
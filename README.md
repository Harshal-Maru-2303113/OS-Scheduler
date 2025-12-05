# OS Scheduler Simulator

A comprehensive Operating System CPU Scheduling Simulator built with **Python**, featuring a **Tkinter** GUI for user interaction and **Matplotlib** for generating Gantt charts and visual analytics.

##  Description

This application allows users to simulate various CPU scheduling algorithms to understand how processes are managed by an Operating System. It provides a visual representation of the scheduling process via Gantt charts and calculates detailed statistics (Turnaround Time, Waiting Time, Response Time) to compare algorithm efficiency.

## Key Features

* **Visualizations:** Generates dynamic Gantt charts using Matplotlib to visualize process execution.
* **Process Management:**
    * **Random Generation:** Generate a set of random processes with variable burst times and priorities.
    * **Manual Control:** Add or remove specific processes individually to test edge cases.
    * **Sample Data:** Load built-in sample data to quickly test the logic.
* **Configuration:**
    * Adjustable **Time Quantum** (for Round Robin and MLFQ).
    * Adjustable **Context Switch** time penalty.
* **Reporting:**
    * View statistics directly on the UI.
    * Export final statistics to a text file (`stats.txt`) for analysis.

##  Supported Algorithms

The simulator supports the following 8 scheduling algorithms:

1.  **FCFS** (First Come First Serve)
2.  **SJF** (Shortest Job First)
3.  **SRTN** (Shortest Remaining Time Next)
4.  **RR** (Round Robin)
5.  **HPF** (Highest Priority First - Non-Preemptive)
6.  **HPF with Aging** (Prevents starvation)
7.  **MLFQ** (Multi-Level Feedback Queue)
8.  **Lottery Scheduling** (Probabilistic scheduling)

## Installation & Requirements

### Prerequisites
* Python 3.x
* `pip` (Python package installer)

### Dependencies
Install the required libraries using pip:

```bash
pip install -r requirements.txt
# Tkinter is usually included with Python.
# If you are on Linux and get an error, run: sudo apt-get install python3-tk
```

## Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Harshal-Maru-2303113/OS-Scheduler
    cd os-scheduler-simulator
    ```

2.  **Run the application:**
    ```bash
    python scheduler.py
    ```

3.  **Using the GUI:**
    * Select your desired **Algorithm** from the dropdown.
    * Set the **Time Quantum** or **Context Switch** (if the algorithm requires it).
    * Click **Generate Random** to populate processes or **Load Sample** to use the default dataset or **Import** your own process file.
    * Use **Add/Remove** buttons to tweak the process queue.
    * Click **Simulate** to generate the Gantt chart and statistics.
    * Click **Export** to save the results to a file.

## Input Data Structure

The scheduler handles process data internally using the following dictionary format:

**Key:** Process ID (String)
**Value:** List containing `[Arrival Time, Burst Time, Priority]`

**Example:**
```python
{
    "1": [0.0, 4.0, 1],  # ID "1": Arrives at 0.0, Burst 4.0, Priority 1
    "2": [1.0, 3.0, 2],  # ID "2": Arrives at 1.0, Burst 3.0, Priority 2
    "3": [2.0, 1.0, 3],
    "4": [3.0, 2.0, 2]
}
```

##  Statistics Output

After simulation, the application calculates and displays:

* **AT:** Arrival Time
* **BT:** Burst Time
* **CT:** Completion Time
* **TAT:** Turnaround Time (CT - AT)
* **WT:** Waiting Time (TAT - BT)
* **RT:** Response Time


import json

def load_input_file(path):
    data = {}
    with open(path, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                pid, arr, burst, pr = line.split()
                data[pid] = [float(arr), float(burst), int(pr)]
    return data

def save_report(path, stats):
    with open(path, "w") as f:
        json.dump(stats, f, indent=2)

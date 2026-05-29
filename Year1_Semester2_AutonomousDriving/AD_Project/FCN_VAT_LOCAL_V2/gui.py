import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import os
import sys

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FCN/VAT Model Runner")
        self.root.geometry("800x600")
        
        self.process = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # 1. Main Control Frame
        frame_controls = ttk.LabelFrame(self.root, text="Configuration", padding="10")
        frame_controls.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Grid layout for inputs
        ttk.Label(frame_controls, text="Task:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.task_var = tk.StringVar(value="run_gtsrb_cnn_baseline")
        tasks = [
            "run_gtsrb_cnn_baseline", "run_gtsrb_cnn_vat",
            "run_gtsrb_fcn_baseline", "run_gtsrb_fcn_vat",
            "run_synthetic_cnn_baseline", "run_synthetic_cnn_vat",
            "run_synthetic_fcn_baseline", "run_synthetic_fcn_vat"
        ]
        self.task_cb = ttk.Combobox(frame_controls, textvariable=self.task_var, values=tasks, state="readonly", width=30)
        self.task_cb.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        
        ttk.Label(frame_controls, text="Dataset:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.dataset_var = tk.StringVar(value="gtsrb")
        self.dataset_cb = ttk.Combobox(frame_controls, textvariable=self.dataset_var, values=["gtsrb", "synthetic"], state="readonly", width=15)
        self.dataset_cb.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(frame_controls, text="Epochs:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=20)
        self.epochs_var = tk.StringVar(value="15")
        ttk.Entry(frame_controls, textvariable=self.epochs_var, width=10).grid(row=0, column=3, sticky=tk.W, pady=5)
        
        ttk.Label(frame_controls, text="Batch Size:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=20)
        self.batch_var = tk.StringVar(value="32")
        ttk.Entry(frame_controls, textvariable=self.batch_var, width=10).grid(row=1, column=3, sticky=tk.W, pady=5)
        
        ttk.Label(frame_controls, text="Learning Rate:").grid(row=2, column=2, sticky=tk.W, pady=5, padx=20)
        self.lr_var = tk.StringVar(value="1e-3")
        ttk.Entry(frame_controls, textvariable=self.lr_var, width=10).grid(row=2, column=3, sticky=tk.W, pady=5)
        
        # 2. Buttons Frame
        frame_btns = ttk.Frame(frame_controls)
        frame_btns.grid(row=3, column=0, columnspan=4, pady=10)
        
        # We use a bold style for the train button to make it stand out
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        
        self.btn_train = ttk.Button(frame_btns, text="▶ Run Train", command=lambda: self.run_script("train"), style="Accent.TButton", width=15)
        self.btn_train.pack(side=tk.LEFT, padx=10)
        
        self.btn_test = ttk.Button(frame_btns, text="🔍 Run Test", command=lambda: self.run_script("test"), width=15)
        self.btn_test.pack(side=tk.LEFT, padx=10)
        
        self.btn_stop = ttk.Button(frame_btns, text="🛑 Stop", command=self.stop_script, state=tk.DISABLED, width=15)
        self.btn_stop.pack(side=tk.LEFT, padx=10)
        
        self.btn_clear = ttk.Button(frame_btns, text="🗑️ Clear Console", command=self.clear_log, width=15)
        self.btn_clear.pack(side=tk.LEFT, padx=10)
        
        # 3. Log Frame
        frame_log = ttk.LabelFrame(self.root, text="Execution Log", padding="5")
        frame_log.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = ScrolledText(frame_log, wrap=tk.WORD, state=tk.DISABLED, bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Automatically select the correct dataset when task changes
        self.task_var.trace_add("write", self.on_task_change)
        
    def on_task_change(self, *args):
        task = self.task_var.get()
        if "gtsrb" in task:
            self.dataset_var.set("gtsrb")
        elif "synthetic" in task:
            self.dataset_var.set("synthetic")
            
    def append_log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def run_script(self, mode):
        if self.process is not None:
            self.append_log("A process is already running!\n")
            return
            
        self.clear_log()
        
        task = self.task_var.get()
        dataset = self.dataset_var.get()
        epochs = self.epochs_var.get()
        batch_size = self.batch_var.get()
        lr = self.lr_var.get()
        
        self.append_log(f"=== Starting {mode.upper()} for {task} ===\n")
        
        self.btn_train.config(state=tk.DISABLED)
        self.btn_test.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
        # Disable inputs
        self.task_cb.config(state=tk.DISABLED)
        self.dataset_cb.config(state=tk.DISABLED)
        
        # Launch using the wrapper script
        # PYTHONUNBUFFERED=1 forces Python to not buffer stdout
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        
        cmd = [sys.executable, "_gui_runner.py", task, epochs, batch_size, lr, dataset, mode]
        
        creationflags = 0
        if os.name == 'nt':
            creationflags = subprocess.CREATE_NO_WINDOW
            
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                env=env,
                creationflags=creationflags
            )
            
            threading.Thread(target=self.read_output, daemon=True).start()
        except Exception as e:
            self.append_log(f"Failed to start process: {e}\n")
            self.process_finished()
        
    def read_output(self):
        try:
            # readline blocks until a newline is found
            for line in iter(self.process.stdout.readline, ''):
                # tqdm progress bars use \r, so we parse that to show the final state
                if '\r' in line:
                    parts = line.split('\r')
                    valid_parts = [p for p in parts if p.strip()]
                    if valid_parts:
                        line = valid_parts[-1]
                        if not line.endswith('\n'):
                            line += '\n'
                self.root.after(0, self.append_log, line)
        except Exception as e:
            self.root.after(0, self.append_log, f"Error reading output: {e}\n")
            
        self.process.wait()
        self.root.after(0, self.process_finished)
        
    def process_finished(self):
        if self.process:
            rc = self.process.returncode
            if rc == 0:
                self.append_log("\n=== Process finished successfully ===\n")
            elif rc < 0:
                self.append_log("\n=== Process was stopped ===\n")
            else:
                self.append_log(f"\n=== Process exited with error code {rc} ===\n")
                
        self.process = None
        self.btn_train.config(state=tk.NORMAL)
        self.btn_test.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.task_cb.config(state="readonly")
        self.dataset_cb.config(state="readonly")
        
    def stop_script(self):
        if self.process:
            self.append_log("\nStopping process...\n")
            self.process.terminate()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from config import Config
from environment import Environment
from blackboard import Blackboard
from utils.metrics import Metrics
from models.internal_state import InternalState
from models.coordinates import Coordinate
from agents.detector_agent import DetectorAgent
from agents.collector_agent import CollectorAgent
from simulation import Simulation
import math

class MASGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MAS Plastic Collector Simulation")
        
        self.sim = None
        self.is_running = False
        self.current_step = 0
        self.after_id = None
        
        self.cell_size = 30
        
        self.setup_ui()
        self.reset_simulation()
        
    def setup_ui(self):
        # Main frames
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.grid(row=0, column=0, sticky="nsew")
        
        self.canvas_frame = ttk.Frame(self.root, padding="10")
        self.canvas_frame.grid(row=0, column=1, sticky="nsew")
        
        self.metrics_frame = ttk.Frame(self.root, padding="10")
        self.metrics_frame.grid(row=0, column=2, sticky="nsew")
        
        # --- Controls ---
        ttk.Label(self.control_frame, text="Simulation Settings", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Config inputs
        self.steps_var = tk.IntVar(value=Config.MAX_STEPS)
        ttk.Label(self.control_frame, text="Max Steps:").pack(anchor="w")
        ttk.Entry(self.control_frame, textvariable=self.steps_var).pack(fill="x", pady=2)
        
        self.detectors_var = tk.IntVar(value=Config.NUM_DETECTORS)
        ttk.Label(self.control_frame, text="Num Detectors:").pack(anchor="w")
        ttk.Entry(self.control_frame, textvariable=self.detectors_var).pack(fill="x", pady=2)
        
        self.collectors_var = tk.IntVar(value=Config.NUM_COLLECTORS)
        ttk.Label(self.control_frame, text="Num Collectors:").pack(anchor="w")
        ttk.Entry(self.control_frame, textvariable=self.collectors_var).pack(fill="x", pady=2)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        ttk.Label(self.control_frame, text="Speed (steps/sec):").pack(anchor="w")
        ttk.Scale(self.control_frame, from_=0.5, to=20.0, variable=self.speed_var, orient="horizontal").pack(fill="x", pady=2)
        
        # Buttons
        button_frame = ttk.Frame(self.control_frame)
        button_frame.pack(fill="x", pady=15)
        
        self.start_btn = ttk.Button(button_frame, text="Start", command=self.start_simulation)
        self.start_btn.grid(row=0, column=0, padx=2, pady=2)
        
        self.pause_btn = ttk.Button(button_frame, text="Pause", command=self.pause_simulation, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=2, pady=2)
        
        self.resume_btn = ttk.Button(button_frame, text="Resume", command=self.resume_simulation, state="disabled")
        self.resume_btn.grid(row=1, column=0, padx=2, pady=2)
        
        self.reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_simulation)
        self.reset_btn.grid(row=1, column=1, padx=2, pady=2)
        
        # --- Canvas ---
        canvas_width = Config.GRID_WIDTH * self.cell_size
        canvas_height = Config.GRID_HEIGHT * self.cell_size
        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()
        
        # --- Metrics ---
        ttk.Label(self.metrics_frame, text="Live Metrics", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.metric_vars = {
            "step": tk.StringVar(value="Step: 0"),
            "plastic": tk.StringVar(value="Total Harvested Plastic: 0"),
            "energy": tk.StringVar(value="Energy Consumed: 0"),
            "discovered": tk.StringVar(value="Discovered Zones: 0"),
            "harvested": tk.StringVar(value="Harvested Zones: 0"),
            "remaining": tk.StringVar(value="Remaining Waste: 0")
        }
        
        for var in self.metric_vars.values():
            ttk.Label(self.metrics_frame, textvariable=var).pack(anchor="w", pady=2)
            
    def update_config_from_ui(self):
        Config.MAX_STEPS = self.steps_var.get()
        Config.NUM_DETECTORS = self.detectors_var.get()
        Config.NUM_COLLECTORS = self.collectors_var.get()
        
    def reset_simulation(self):
        self.pause_simulation()
        self.update_config_from_ui()
        
        self.current_step = 0
        
        # Re-initialize MAS components
        self.env = Environment(Config.GRID_WIDTH, Config.GRID_HEIGHT)
        self.blackboard = Blackboard()
        self.metrics = Metrics()
        self.agents = []
        
        barge_pos = Coordinate(Config.BARGE_LOCATION[0], Config.BARGE_LOCATION[1])
        
        for i in range(Config.NUM_DETECTORS):
            state = InternalState(
                position=Coordinate(barge_pos.x, barge_pos.y),
                battery=Config.DETECTOR_ENERGY_CAP,
            )
            detector = DetectorAgent(f"Detector-{i}", state)
            detector.set_blackboard(self.blackboard)
            self.agents.append(detector)
            
        for i in range(Config.NUM_COLLECTORS):
            state = InternalState(
                position=Coordinate(barge_pos.x, barge_pos.y),
                battery=Config.COLLECTOR_ENERGY_CAP,
                storage_capacity=Config.COLLECTOR_STORAGE_CAP
            )
            collector = CollectorAgent(f"Collector-{i}", state)
            collector.set_references(self.env, self.blackboard)
            self.agents.append(collector)
            
        self.sim = Simulation(self.env, self.blackboard, self.agents, self.metrics)
        
        # Reset UI
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="disabled")
        
        self.draw_environment()
        self.update_metrics()
        
    def start_simulation(self):
        self.start_btn.config(state="disabled")
        self.resume_simulation()
        
    def pause_simulation(self):
        self.is_running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="normal")
        
    def resume_simulation(self):
        self.is_running = True
        self.pause_btn.config(state="normal")
        self.resume_btn.config(state="disabled")
        self.run_step()
        
    def run_step(self):
        if not self.is_running:
            return
            
        if self.current_step >= Config.MAX_STEPS:
            self.pause_simulation()
            self.start_btn.config(state="disabled")
            self.resume_btn.config(state="disabled")
            return
            
        # Execute one step
        continue_sim = self.sim.step(self.current_step)
        
        # Update metrics for zones manually as it was done at the end of sim previously
        self.metrics.discovered_zones_count = len(self.blackboard.zones)
        self.metrics.harvested_zones_count = len([z for z, status in self.blackboard.zones.items() if status == 'HARVESTED'])
        
        self.current_step += 1
        
        # Render
        self.draw_environment()
        self.update_metrics()
        
        if continue_sim and self.current_step < Config.MAX_STEPS:
            # Schedule next step
            delay_ms = int(1000 / self.speed_var.get())
            self.after_id = self.root.after(delay_ms, self.run_step)
        else:
            self.pause_simulation()
            self.start_btn.config(state="disabled")
            self.resume_btn.config(state="disabled")
            
    def update_metrics(self):
        self.metric_vars["step"].set(f"Step: {self.current_step} / {Config.MAX_STEPS}")
        self.metric_vars["plastic"].set(f"Total Harvested Plastic: {self.metrics.total_harvested_plastic}")
        self.metric_vars["energy"].set(f"Energy Consumed: {self.metrics.total_energy_consumed}")
        self.metric_vars["discovered"].set(f"Discovered Zones: {self.metrics.discovered_zones_count}")
        self.metric_vars["harvested"].set(f"Harvested Zones: {self.metrics.harvested_zones_count}")
        
        total_waste = sum(cell.density for row in self.env.grid for cell in row)
        self.metric_vars["remaining"].set(f"Remaining Waste: {total_waste}")
        
    def draw_environment(self):
        self.canvas.delete("all")
        
        # Draw grid
        for y in range(Config.GRID_HEIGHT):
            for x in range(Config.GRID_WIDTH):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell = self.env.get_cell(Coordinate(x, y))
                
                # Default colors
                bg_color = "#e0f7fa" # Light cyan for empty water
                outline_color = "#b2ebf2"
                
                if (x, y) == Config.BARGE_LOCATION:
                    bg_color = "#fff59d" # Yellow for barge
                elif cell.is_obstacle:
                    bg_color = "#424242" # Dark gray for obstacle
                elif cell.density > 0:
                    # Darker blue for higher density
                    intensity = min(255, 50 + cell.density * 20)
                    bg_color = f"#{255-intensity:02x}{255-intensity:02x}ff"
                    
                # Check zones in blackboard
                coord = Coordinate(x, y)
                if coord in self.blackboard.zones:
                    status = self.blackboard.zones[coord]
                    if status == 'UNHARVESTED':
                        outline_color = "red"
                    elif status == 'IN_PROGRESS':
                        outline_color = "orange"
                    elif status == 'HARVESTED':
                        outline_color = "green"
                
                # Draw cell rect
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline=outline_color, width=2 if outline_color != "#b2ebf2" else 1)
                
                # Draw text for density
                if cell.density > 0 and not cell.is_obstacle and (x, y) != Config.BARGE_LOCATION:
                    self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=str(cell.density), fill="white", font=("Arial", 8, "bold"))

        # Draw Agents
        for agent in self.agents:
            ax = agent.state.position.x
            ay = agent.state.position.y
            cx = ax * self.cell_size + self.cell_size / 2
            cy = ay * self.cell_size + self.cell_size / 2
            r = self.cell_size / 3
            
            if isinstance(agent, DetectorAgent):
                # Green triangle for detector
                self.canvas.create_polygon(cx, cy - r, cx - r, cy + r, cx + r, cy + r, fill="#00e676", outline="black")
            elif isinstance(agent, CollectorAgent):
                # Orange circle for collector
                self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#ff9800", outline="black")

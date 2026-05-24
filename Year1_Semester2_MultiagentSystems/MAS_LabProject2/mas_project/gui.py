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
from models.agent_config import DetectorConfig, CollectorConfig
import math
import copy

class MASGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MAS Plastic Collector Simulation")
        
        self.sim = None
        self.is_running = False
        self.current_step = 0
        self.after_id = None
        
        self.cell_size = 30
        
        self.detector_config = copy.deepcopy(Config.DEFAULT_DETECTOR_CONFIG)
        self.collector_config = copy.deepcopy(Config.DEFAULT_COLLECTOR_CONFIG)
        
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
        
        # Action Buttons
        button_frame = ttk.Frame(self.control_frame)
        button_frame.pack(fill="x", pady=5)
        
        self.start_btn = ttk.Button(button_frame, text="Start", command=self.start_simulation)
        self.start_btn.grid(row=0, column=0, padx=2, pady=2)
        
        self.pause_btn = ttk.Button(button_frame, text="Pause", command=self.pause_simulation, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=2, pady=2)
        
        self.resume_btn = ttk.Button(button_frame, text="Resume", command=self.resume_simulation, state="disabled")
        self.resume_btn.grid(row=1, column=0, padx=2, pady=2)
        
        self.reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_simulation)
        self.reset_btn.grid(row=1, column=1, padx=2, pady=2)
        
        # Configuration & Info Buttons
        config_frame = ttk.Frame(self.control_frame)
        config_frame.pack(fill="x", pady=5)
        
        ttk.Button(config_frame, text="Edit Detectors", command=self.open_detector_config).pack(fill="x", pady=2)
        ttk.Button(config_frame, text="Edit Collectors", command=self.open_collector_config).pack(fill="x", pady=2)
        ttk.Button(config_frame, text="Info", command=self.open_info).pack(fill="x", pady=2)

        # --- Canvas ---
        canvas_width = Config.GRID_WIDTH * self.cell_size
        canvas_height = Config.GRID_HEIGHT * self.cell_size
        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()
        
        # Tooltip
        self.tooltip = tk.Label(self.root, bg="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 9), justify="left")
        self.tooltip.place_forget()
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)

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

    def on_mouse_move(self, event):
        if not self.env:
            return
            
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        
        if x < 0 or x >= self.env.width or y < 0 or y >= self.env.height:
            self.tooltip.place_forget()
            return
            
        coord = Coordinate(x, y)
        cell = self.env.get_cell(coord)
        info_lines = [f"Coordinates: ({x}, {y})"]
        
        if (x, y) == Config.BARGE_LOCATION:
            info_lines.append("Terrain: Central Barge")
        elif cell.is_obstacle:
            info_lines.append("Terrain: Obstacle")
        else:
            info_lines.append("Terrain: Water")
            if cell.density > 0:
                info_lines.append(f"Waste Density: {cell.density}")
                
        if coord in self.blackboard.zones:
            info_lines.append(f"Zone Status: {self.blackboard.zones[coord]}")
            
        agents_here = [a for a in self.agents if a.state.position == coord]
        for a in agents_here:
            if isinstance(a, DetectorAgent):
                info_lines.append(f"--- Detector Agent ({a.id}) ---")
                info_lines.append(f"Battery: {a.state.battery}/{self.detector_config.battery_capacity}")
                info_lines.append(f"Speed: {self.detector_config.movement_speed}")
            elif isinstance(a, CollectorAgent):
                info_lines.append(f"--- Collector Agent ({a.id}) ---")
                info_lines.append(f"Battery: {a.state.battery}/{self.collector_config.battery_capacity}")
                info_lines.append(f"Storage: {a.state.current_storage}/{self.collector_config.storage_capacity}")
                target = a.state.current_target
                t_str = f"({target.x}, {target.y})" if target else "None"
                info_lines.append(f"Target: {t_str}")

        info_text = "\n".join(info_lines)
        self.tooltip.config(text=info_text)
        
        # Position the tooltip near the mouse
        tt_x = event.x_root - self.root.winfo_rootx() + 15
        tt_y = event.y_root - self.root.winfo_rooty() + 15
        self.tooltip.lift()
        self.tooltip.place(x=tt_x, y=tt_y)

    def on_mouse_leave(self, event):
        self.tooltip.place_forget()

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
                battery=self.detector_config.battery_capacity,
            )
            detector = DetectorAgent(f"Detector-{i}", state, copy.deepcopy(self.detector_config))
            detector.set_blackboard(self.blackboard)
            self.agents.append(detector)
            
        for i in range(Config.NUM_COLLECTORS):
            state = InternalState(
                position=Coordinate(barge_pos.x, barge_pos.y),
                battery=self.collector_config.battery_capacity,
                storage_capacity=self.collector_config.storage_capacity
            )
            collector = CollectorAgent(f"Collector-{i}", state, copy.deepcopy(self.collector_config))
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
        
        # Update metrics for zones manually
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
                        bg_color = "#e8f5e9" # pale green for harvested zone
                
                # Draw cell rect
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline=outline_color, width=2 if outline_color != "#b2ebf2" else 1)
                
                # Draw text for density or barge
                if (x, y) == Config.BARGE_LOCATION:
                    self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text="B", fill="blue", font=("Arial", 10, "bold"))
                elif cell.density > 0 and not cell.is_obstacle:
                    self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=str(cell.density), fill="white", font=("Arial", 8, "bold"))
                elif cell.is_obstacle:
                    self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text="X", fill="white", font=("Arial", 10, "bold"))

        # Draw Agents
        for agent in self.agents:
            ax = agent.state.position.x
            ay = agent.state.position.y
            cx = ax * self.cell_size + self.cell_size / 2
            cy = ay * self.cell_size + self.cell_size / 2
            r = self.cell_size / 3
            
            if isinstance(agent, DetectorAgent):
                # Green/Purple triangle for detector
                self.canvas.create_polygon(cx, cy - r, cx - r, cy + r, cx + r, cy + r, fill="#9c27b0", outline="black")
                self.canvas.create_text(cx, cy + 2, text="D", fill="white", font=("Arial", 7, "bold"))
            elif isinstance(agent, CollectorAgent):
                # Orange circle for collector
                self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#ff9800", outline="black")
                self.canvas.create_text(cx, cy, text="C", fill="white", font=("Arial", 7, "bold"))


    def _create_config_popup(self, title, config_obj, fields):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x400")
        popup.grab_set() # Modal
        
        entries = {}
        row = 0
        for field, (label_text, field_type) in fields.items():
            ttk.Label(popup, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="e")
            val = getattr(config_obj, field)
            var = tk.StringVar(value=str(val))
            ttk.Entry(popup, textvariable=var).grid(row=row, column=1, padx=10, pady=5)
            entries[field] = (var, field_type)
            row += 1
            
        def save():
            try:
                for field, (var, field_type) in entries.items():
                    setattr(config_obj, field, field_type(var.get()))
                popup.destroy()
            except ValueError:
                tk.messagebox.showerror("Invalid Input", "Please check your inputs.", parent=popup)

        btn_frame = ttk.Frame(popup)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Save", command=save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=5)


    def open_detector_config(self):
        fields = {
            "battery_capacity": ("Battery Capacity:", int),
            "movement_speed": ("Movement Speed:", int),
            "energy_cost_per_move": ("Energy Cost/Move:", int),
            "sensor_range": ("Sensor Range:", int),
            "waste_detection_threshold": ("Detection Threshold:", int),
            "exploration_strategy": ("Exploration Strategy:", str),
        }
        self._create_config_popup("Edit Detector Config", self.detector_config, fields)

    def open_collector_config(self):
        fields = {
            "battery_capacity": ("Battery Capacity:", int),
            "storage_capacity": ("Storage Capacity:", int),
            "movement_speed": ("Movement Speed:", int),
            "energy_cost_per_move": ("Energy Cost/Move:", int),
            "harvest_rate": ("Harvest Rate:", int),
            "unload_location": ("Unload Location:", str),
            "weight_waste_value": ("Weight - Waste Value:", float),
            "weight_distance_cost": ("Weight - Distance Cost:", float),
            "weight_energy_cost": ("Weight - Energy Cost:", float),
        }
        self._create_config_popup("Edit Collector Config", self.collector_config, fields)

    def open_info(self):
        popup = tk.Toplevel(self.root)
        popup.title("Information & Legend")
        popup.geometry("450x450")
        
        info_text = """
        MAS Plastic Collector Simulation
        
        Visual Legend:
        - Light blue: Water / Empty cell
        - Dark gray 'X': Obstacle
        - Numbered blue/green cell: Plastic waste (density value)
        - Green border: Discovered waste zone
        - Blue 'B': Central Barge (Unload point)
        - Purple Triangle 'D': Detector Agent
        - Orange Circle 'C': Collector Agent
        - Pale/neutral cell: Harvested Zone
        
        Workflow Overview:
        1. Detectors explore the environment based on their strategy.
        2. When a Detector finds waste above a threshold, it writes 
           the zone's coordinates to the shared Blackboard.
        3. Collectors read the Blackboard and compute the utility of
           available unharvested zones.
        4. Collectors travel to the optimal zone, harvest waste until
           full, and then return it to the central barge.
        """
        
        lbl = tk.Label(popup, text=info_text, justify="left", font=("Arial", 10))
        lbl.pack(padx=20, pady=20, fill="both", expand=True)
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

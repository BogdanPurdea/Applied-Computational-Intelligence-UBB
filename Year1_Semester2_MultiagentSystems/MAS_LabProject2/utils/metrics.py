class Metrics:
    def __init__(self):
        self.total_harvested_plastic = 0
        self.total_energy_consumed = 0
        self.simulation_time = 0
        self.discovered_zones_count = 0
        self.harvested_zones_count = 0

    def add_harvested(self, amount: int):
        self.total_harvested_plastic += amount

    def add_energy(self, amount: int):
        self.total_energy_consumed += amount

    def record_discovered_zone(self):
        self.discovered_zones_count += 1

    def record_harvested_zone(self):
        self.harvested_zones_count += 1

    def increment_time(self):
        self.simulation_time += 1

    def display(self):
        print("\n--- Simulation Metrics ---")
        print(f"Total Harvested Plastic: {self.total_harvested_plastic}")
        print(f"Total Energy Consumed: {self.total_energy_consumed}")
        print(f"Simulation Time (steps): {self.simulation_time}")
        print(f"Discovered Zones: {self.discovered_zones_count}")
        print(f"Harvested Zones: {self.harvested_zones_count}")
        print("--------------------------\n")

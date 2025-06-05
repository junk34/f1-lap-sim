class RaceStrategy:
    def __init__(self, simulator, all_tracks):
        self.simulator = simulator
        self.all_tracks = all_tracks
    
    def analyze_all_tracks(self, n=200):
        """Analyze performance across all tracks"""
        results = {}
        
        for track_name, track_data in self.all_tracks.items():
            # Update simulator with current track
            self.simulator.track = track_data
            
            # Run simulations for this track
            laps = []
            for _ in range(n):
                laps.append(self.simulator.calculate_lap_time(
                    tire_wear=10,  # Fixed wear for comparison
                    fuel_load=30   # Fixed fuel for comparison
                ))
            
            # Store results
            results[track_name] = {
                "avg_lap": sum(laps)/len(laps),
                "best_lap": min(laps),
                "consistency": (sum((x - (sum(laps)/len(laps)))**2 for x in laps)/len(laps))**0.5,
                "full_data": laps
            }
        
        return results
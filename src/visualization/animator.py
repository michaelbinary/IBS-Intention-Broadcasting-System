from dataclasses import dataclass
from typing import Dict, List, Set
import numpy as np
from .intention import Intention

@dataclass
class DroneState:
    position: np.ndarray
    velocity: np.ndarray
    goal: np.ndarray
    current_intention: Intention
    received_intentions: Dict[str, Intention]
    mesh_connections: Set[str]
    communication_range: float
    path_history: List[np.ndarray]
    status: str
    metrics: Dict[str, List[float]]

    def update_position(self, new_position: np.ndarray, dt: float):
        """Update drone position and record history"""
        self.position = new_position
        self.path_history.append(new_position.copy())
        if len(self.path_history) > 50:  # Keep last 50 positions
            self.path_history.pop(0)

    def update_velocity(self, new_velocity: np.ndarray):
        """Update drone velocity"""
        self.velocity = new_velocity

    def update_status(self, new_status: str):
        """Update drone status"""
        self.status = new_status

    def receive_intention(self, drone_id: str, intention: Intention):
        """Receive and store intention from another drone"""
        self.received_intentions[drone_id] = intention

    def update_mesh_connections(self, new_connections: Set[str]):
        """Update mesh network connections"""
        self.mesh_connections = new_connections

    def record_metric(self, metric_name: str, value: float):
        """Record a metric value"""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)
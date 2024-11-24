from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class Intention:
    waypoints: List[np.ndarray]
    confidence: float
    priority: int
    timestamp: float
    emergency_routes: List[List[np.ndarray]]
    path_risk: float

    @classmethod
    def create_initial(cls, start: np.ndarray, goal: np.ndarray, priority: int,
                       waypoint_generator, emergency_route_generator):
        """Create initial intention for a new drone"""
        waypoints = waypoint_generator(start, goal)
        emergency_routes = emergency_route_generator(start)

        return cls(
            waypoints=waypoints,
            confidence=1.0,
            priority=priority,
            timestamp=0.0,
            emergency_routes=emergency_routes,
            path_risk=0.0
        )

    def update_confidence(self, new_confidence: float):
        """Update intention confidence"""
        self.confidence = new_confidence

    def update_emergency_routes(self, new_routes: List[List[np.ndarray]]):
        """Update emergency escape routes"""
        self.emergency_routes = new_routes

    def calculate_path_length(self) -> float:
        """Calculate total path length"""
        total_length = 0
        for i in range(len(self.waypoints) - 1):
            total_length += np.linalg.norm(self.waypoints[i + 1] - self.waypoints[i])
        return total_length
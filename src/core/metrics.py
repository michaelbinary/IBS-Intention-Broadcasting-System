from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime


@dataclass
class SimulationMetrics:
    timestamp: float
    network_connectivity: float
    active_conflicts: int
    average_confidence: float
    total_path_adjustments: int
    mesh_density: float
    average_path_length: float
    emergency_route_activations: int
    collision_risks: List[float]
    priority_distribution: Dict[str, int]

    @classmethod
    def create_from_network(cls, network: 'IntentionBroadcastNetwork', time: float):
        """Factory method to create metrics from current network state"""
        active_conflicts = sum(1 for d in network.drones.values() if d.status == 'adjusting')

        confidences = [d.current_intention.confidence for d in network.drones.values()]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        num_nodes = len(network.drones)
        num_edges = len(network.mesh_network.edges())
        mesh_density = (2 * num_edges) / (num_nodes * (num_nodes - 1)) if num_nodes > 1 else 0

        # Calculate remaining metrics...

        return cls(
            timestamp=time,
            network_connectivity=network.calculate_connectivity(),
            active_conflicts=active_conflicts,
            average_confidence=avg_confidence,
            total_path_adjustments=sum(network.network_metrics['path_adjustments']),
            mesh_density=mesh_density,
            average_path_length=network.calculate_average_path_length(),
            emergency_route_activations=sum(1 for d in network.drones.values() if d.status == 'emergency'),
            collision_risks=[d.current_intention.path_risk for d in network.drones.values()],
            priority_distribution=network.calculate_priority_distribution()
        )
#!/usr/bin/env python3
"""
Basic demonstration of the Intention Broadcasting System.
Creates a scenario with crossing traffic flows and different priority levels.
"""

from ibs.network.broadcast import IntentionBroadcastNetwork
from ibs.visualization.animator import SimulationAnimator
from rich.console import Console
import numpy as np
import random

console = Console()


def create_crossing_traffic_flows(network, space_size):
    """Create intentionally crossing traffic flows"""
    # Define flow patterns from corners to opposite corners
    flow_patterns = [
        ((0, 0, 0), (space_size[0], space_size[1], space_size[2])),
        ((space_size[0], 0, 0), (0, space_size[1], space_size[2])),
        ((0, space_size[1], 0), (space_size[0], 0, space_size[2])),
        ((space_size[0], space_size[1], 0), (0, 0, space_size[2]))
    ]

    # Priority scenarios with timing to create conflicts
    priority_scenarios = [
        ('emergency', 4),
        ('medical', 4),
        ('express', 5),
        ('standard', 4),
        ('flexible', 3)
    ]

    console.print("\n[bold blue]Creating drone traffic flows...[/bold blue]")

    drone_count = 0
    flow_idx = 0

    for priority, count in priority_scenarios:
        console.print(f"\n[yellow]Adding {count} {priority} priority drones[/yellow]")

        for i in range(count):
            # Select base flow pattern and add randomness
            base_start, base_goal = flow_patterns[flow_idx % len(flow_patterns)]

            # Add randomness but maintain general flow direction
            random_offset = np.array([
                random.uniform(-5, 5),
                random.uniform(-5, 5),
                random.uniform(-5, 5)
            ])

            start = np.array(base_start) + random_offset
            goal = np.array(base_goal) + random_offset

            # Ensure within bounds
            start = np.clip(start, 0, np.array(space_size))
            goal = np.clip(goal, 0, np.array(space_size))

            drone_id = f"{priority}_{i}"
            network.add_drone(drone_id, start, goal, priority)

            console.print(f"  [green]Added {drone_id}[/green]")
            console.print(f"    Start: {start.round(2)}")
            console.print(f"    Goal: {goal.round(2)}")

            drone_count += 1
            flow_idx += 1

    console.print(f"\n[bold green]Successfully initialized {drone_count} drones[/bold green]")


def run_simulation(space_size=(50, 50, 30), num_frames=300):
    """Run the complete simulation"""
    console.print("[bold blue]Initializing Intention Broadcasting System Simulation[/bold blue]")
    console.print("=" * 60)

    # Create network and initialize scenario
    network = IntentionBroadcastNetwork(space_size)
    console.print(f"[cyan]Space dimensions: {space_size}[/cyan]")

    # Create traffic flows
    create_crossing_traffic_flows(network, space_size)

    # Initialize animator
    animator = SimulationAnimator(network)
    console.print("\n[bold green]Visualization initialized[/bold green]")

    # Run simulation
    console.print("\n[bold yellow]Running simulation...[/bold yellow]")
    try:
        for frame in range(num_frames):
            if frame % 10 == 0:  # Progress update every 10 frames
                console.print(f"Processing frame {frame}/{num_frames}")

            # Update simulation
            network.update(0.1, frame * 0.1)

            # Update visualization
            animator.update(frame)
            animator.save_frame()

        # Save final results
        console.print("\n[bold green]Simulation completed successfully![/bold green]")

        # Save animation
        console.print("\n[yellow]Saving animation...[/yellow]")
        animator.save_animation()

        # Save metrics
        console.print("[yellow]Saving metrics...[/yellow]")
        network.save_metrics(f"simulation_{network.simulation_id}")

        # Print final statistics
        metrics = network.metrics_history[-1]
        console.print("\n[bold blue]Final Simulation Statistics:[/bold blue]")
        console.print(f"Network Connectivity: {metrics.network_connectivity:.2f}")
        console.print(f"Active Conflicts: {metrics.active_conflicts}")
        console.print(f"Average Confidence: {metrics.average_confidence:.2f}")
        console.print(f"Emergency Route Activations: {metrics.emergency_route_activations}")

        for priority, count in metrics.priority_distribution.items():
            console.print(f"{priority.capitalize()} Drones: {count}")

    except Exception as e:
        console.print(f"[bold red]Error during simulation: {str(e)}[/bold red]")
        raise


if __name__ == "__main__":
    run_simulation()
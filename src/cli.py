#!/usr/bin/env python3
"""
Command Line Interface for the Intention Broadcasting System.
Provides commands for running simulations with various configurations.
"""

import click
from rich.console import Console
import numpy as np
from .network.broadcast import IntentionBroadcastNetwork
from .visualization.animator import SimulationAnimator

console = Console()


@click.group()
def cli():
    """Intention Broadcasting System (IBS) Command Line Interface"""
    pass


@cli.command()
@click.option('--space-x', default=50, help='X dimension of the space')
@click.option('--space-y', default=50, help='Y dimension of the space')
@click.option('--space-z', default=30, help='Z dimension of the space')
@click.option('--frames', default=300, help='Number of simulation frames')
@click.option('--mesh-range', default=15.0, help='Mesh network connection range')
@click.option('--collision-threshold', default=5.0, help='Collision detection threshold')
@click.option('--output-dir', default=None, help='Directory for output files')
@click.option('--emergency-count', default=4, help='Number of emergency drones')
@click.option('--medical-count', default=4, help='Number of medical drones')
@click.option('--express-count', default=5, help='Number of express delivery drones')
@click.option('--standard-count', default=4, help='Number of standard drones')
@click.option('--flexible-count', default=3, help='Number of flexible priority drones')
def run(space_x, space_y, space_z, frames, mesh_range, collision_threshold,
        output_dir, emergency_count, medical_count, express_count,
        standard_count, flexible_count):
    """Run a simulation with specified parameters"""
    try:
        console.print("[bold blue]Starting IBS Simulation[/bold blue]")

        # Configure space
        space_size = (space_x, space_y, space_z)
        console.print(f"Space dimensions: {space_size}")

        # Initialize network
        network = IntentionBroadcastNetwork(space_size)
        network.mesh_range = mesh_range
        network.collision_threshold = collision_threshold

        # Set up drone counts
        drone_configs = {
            'emergency': emergency_count,
            'medical': medical_count,
            'express': express_count,
            'standard': standard_count,
            'flexible': flexible_count
        }

        # Initialize traffic flows
        console.print("\n[yellow]Initializing drone traffic...[/yellow]")
        flow_patterns = [
            ((0, 0, 0), (space_x, space_y, space_z)),
            ((space_x, 0, 0), (0, space_y, space_z)),
            ((0, space_y, 0), (space_x, 0, space_z)),
            ((space_x, space_y, 0), (0, 0, space_z))
        ]

        pattern_idx = 0
        for priority, count in drone_configs.items():
            console.print(f"\nAdding {count} {priority} priority drones...")

            for i in range(count):
                base_start, base_goal = flow_patterns[pattern_idx % len(flow_patterns)]
                random_offset = (np.random.rand(3) - 0.5) * 10

                start = np.clip(np.array(base_start) + random_offset, 0, space_size)
                goal = np.clip(np.array(base_goal) + random_offset, 0, space_size)

                drone_id = f"{priority}_{i}"
                network.add_drone(drone_id, start, goal, priority)
                console.print(f"  Added {drone_id}")

                pattern_idx += 1

        # Initialize visualizer
        animator = SimulationAnimator(network, output_dir)
        console.print("\n[bold green]Starting simulation...[/bold green]")

        # Run simulation
        for frame in range(frames):
            if frame % 10 == 0:
                console.print(f"Frame {frame}/{frames}")

            network.update(0.1, frame * 0.1)
            animator.update(frame)
            animator.save_frame()

        # Save results
        animator.save_animation()
        network.save_metrics(f"simulation_{network.simulation_id}")

        console.print("\n[bold green]Simulation completed successfully![/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        raise


@cli.command()
def info():
    """Display information about the simulation system"""
    console.print("""
[bold blue]Intention Broadcasting System (IBS)[/bold blue]

[yellow]Priority Levels:[/yellow]
- Emergency: Highest priority, emergency response
- Medical: High priority medical deliveries
- Express: Express delivery services
- Standard: Regular operation priority
- Flexible: Lowest priority, flexible timing

[yellow]Key Parameters:[/yellow]
- Space Dimensions: 3D space size (X, Y, Z)
- Mesh Range: Maximum connection distance between drones
- Collision Threshold: Minimum safe distance between drones
- Frames: Number of simulation steps

[yellow]Example Usage:[/yellow]
  # Run basic simulation
  ibs run

  # Run with custom space size
  ibs run --space-x 60 --space-y 60 --space-z 40

  # Adjust drone counts
  ibs run --emergency-count 6 --express-count 8

  # Modify network parameters
  ibs run --mesh-range 20 --collision-threshold 4
    """)


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == '__main__':
    main()
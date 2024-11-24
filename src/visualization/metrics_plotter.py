import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List
from ..core.metrics import SimulationMetrics

class MetricsPlotter:
    def __init__(self, output_dir: str = 'data/analytics'):
        self.output_dir = output_dir
        plt.style.use('default')

    def plot_network_metrics(self, df: pd.DataFrame, base_path: str):
        """Generate network connectivity and mesh density plots"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        df.plot(x='timestamp', y='network_connectivity', ax=ax1)
        ax1.set_title('Network Connectivity Over Time')
        df.plot(x='timestamp', y='mesh_density', ax=ax2)
        ax2.set_title('Mesh Density Over Time')
        plt.tight_layout()
        plt.savefig(f'{base_path}_network_metrics.png')
        plt.close()

    def plot_conflicts(self, df: pd.DataFrame, base_path: str):
        """Generate conflicts and adjustments plot"""
        fig, ax = plt.subplots(figsize=(12, 6))
        df.plot(x='timestamp', y=['active_conflicts', 'total_path_adjustments'], ax=ax)
        ax.set_title('Conflicts and Path Adjustments Over Time')
        plt.savefig(f'{base_path}_conflicts.png')
        plt.close()

    def plot_priority_distribution(self, df: pd.DataFrame, base_path: str):
        """Generate priority distribution heatmap"""
        priority_cols = [col for col in df.columns if col.startswith('priority_')]
        priority_data = df[priority_cols].T
        plt.figure(figsize=(12, 6))
        plt.imshow(priority_data, aspect='auto', cmap='YlOrRd')
        plt.colorbar()
        plt.title('Priority Distribution Over Time')
        plt.savefig(f'{base_path}_priority_distribution.png')
        plt.close()
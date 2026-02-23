import matplotlib.pyplot as plt
import numpy as np

def plot_strategy(strategy_results, stats: dict = None, percentiles: list = [90]):
    """
    Plots a histogram of total race times from a Monte Carlo simulation.

    Parameters:
    - strategy_results (list or array-like): Total race times to visualize
    - stats (dict, optional): Dictionary with keys like 'best', 'avg', 'p90', 'worst'
    - percentiles (list, optional): Percentiles to mark on the histogram
    """
    strategy_results = np.array(strategy_results)
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram
    bins = min(50, max(10, len(strategy_results) // 20))
    ax.hist(strategy_results, bins=bins, alpha=0.75, color='#FF4C4C', edgecolor='black')

    # Overlay percentiles
    for p in percentiles:
        val = np.percentile(strategy_results, p)
        ax.axvline(val, color='navy', linestyle='--', linewidth=1.5, label=f"{p}th percentile")

    # Overlay stats if provided
    if stats:
        ax.axvline(stats.get("avg", 0), color='green', linestyle='-', linewidth=2, label="Average")
        ax.axvline(stats.get("best", 0), color='gold', linestyle=':', linewidth=2, label="Best")
        ax.axvline(stats.get("worst", 0), color='red', linestyle=':', linewidth=2, label="Worst")

    # Labels and styling
    ax.set_xlabel("Total Race Time (seconds)")
    ax.set_ylabel("Frequency")
    ax.set_title("Monte Carlo Race Strategy Simulation")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend()
    plt.tight_layout()
    plt.show()


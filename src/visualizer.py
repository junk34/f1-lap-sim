import matplotlib.pyplot as plt

def plot_strategy(strategy_results):
    """
    Plots a histogram of total race times from a Monte Carlo simulation.

    Parameters:
    - strategy_results (list or array-like): Total race times to visualize
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(strategy_results, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    ax.set_xlabel("Total Race Time (seconds)")
    ax.set_ylabel("Frequency")
    ax.set_title("Monte Carlo Strategy Simulation Results")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

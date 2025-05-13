import matplotlib.pyplot as plt

def plot_strategy(strategy_results):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(strategy_results, bins=50, alpha=0.7)
    ax.set_xlabel("Total Race Time (s)")
    ax.set_ylabel("Frequency")
    ax.set_title("Monte Carlo Strategy Simulation")
    plt.show()
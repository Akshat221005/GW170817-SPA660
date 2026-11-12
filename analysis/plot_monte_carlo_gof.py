import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

data = np.genfromtxt(
    "analysis/monte_carlo_gof_results.csv",
    delimiter=",",
    skip_header=1
)

stats = data[:, 1]
observed = 268.52581545138463

p_value = (np.count_nonzero(stats >= observed) + 1) / (len(stats) + 1)

plt.figure(figsize=(9, 5.5))

plt.hist(stats, bins=30, edgecolor="black", alpha=0.75)

plt.axvline(
    observed,
    linestyle="--",
    linewidth=2,
    label=f"Observed W-statistic = {observed:.2f}"
)

plt.xlabel("W-statistic")
plt.ylabel("Number of simulations")
plt.title("Monte Carlo Goodness-of-Fit Test: TBabs × PowerLaw")
plt.legend()

plt.text(
    0.97, 0.95,
    f"Simulations = {len(stats)}\np-value = {p_value:.4f}",
    transform=plt.gca().transAxes,
    ha="right",
    va="top"
)

plt.tight_layout()
plt.savefig(
    "report/plots/monte_carlo_gof.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Plot saved: report/plots/monte_carlo_gof.png")

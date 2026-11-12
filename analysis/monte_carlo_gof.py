import csv
import numpy as np

from sherpa.astro.ui import *
from sherpa.astro.xspec import XSTBabs, XSpowerlaw

# Reproducibility.
rng = np.random.default_rng(20261112)

N_SIM = 500
OBSERVED_STAT = 268.52581545138463

SOURCE_FILE = "analysis/spectra/gw170817_05_7.pi"
BACKGROUND_FILE = "analysis/spectra/gw170817_05_7_bkg.pi"

# --------------------------------------------------
# Load and fit the observed spectrum.
# --------------------------------------------------

load_pha(SOURCE_FILE)
set_analysis("energy")
notice(0.5, 7.0)
set_stat("wstat")
set_xsabund("wilm")

absorption = XSTBabs()
powerlaw = XSpowerlaw()
observed_model = absorption * powerlaw

absorption.nH = 0.5582944636
powerlaw.PhoIndex = 2.0476213938
powerlaw.norm = 5.331252122e-6

set_model(observed_model)
fit()

# Instrument response and observation information.
arf = get_arf()
rmf = get_rmf()
exposure = get_exposure()
source_backscal = get_backscal()

original_background = get_bkg()
original_background_counts = original_background.counts.copy()

print("\nObserved W-statistic:", OBSERVED_STAT)
print("Starting", N_SIM, "Monte Carlo simulations...\n")

simulated_statistics = []
failed = 0

# --------------------------------------------------
# Monte Carlo loop.
# --------------------------------------------------

for i in range(N_SIM):

    try:
        # Load fresh source and background PHA objects.
        sim_source = unpack_pha(SOURCE_FILE)
        sim_background = unpack_pha(BACKGROUND_FILE)

        # Independently Poisson-resample background.
        sim_background.counts = rng.poisson(
            original_background_counts
        )

        # Register the simulated dataset.
        set_data("sim", sim_source)
        set_bkg("sim", sim_background)

        # Apply the same energy range.
        set_default_id("sim")
        set_analysis("sim", "energy")
        notice(0.5, 7.0)

        # Create a fresh model for this realization.
        sim_absorption = XSTBabs()
        sim_powerlaw = XSpowerlaw()
        sim_model = sim_absorption * sim_powerlaw

        sim_absorption.nH = 0.5582944636
        sim_powerlaw.PhoIndex = 2.0476213938
        sim_powerlaw.norm = 5.331252122e-6

        sim_absorption.nH.min = 0.0
        sim_absorption.nH.max = 10.0

        sim_powerlaw.PhoIndex.min = 0.0
        sim_powerlaw.PhoIndex.max = 5.0

        sim_powerlaw.norm.min = 1e-12
        sim_powerlaw.norm.max = 1.0

        set_model("sim", sim_model)

        # Generate simulated source counts, including background.
        fake_pha(
            "sim",
            arf=arf,
            rmf=rmf,
            exposure=exposure,
            backscal=source_backscal,
            bkg=sim_background
        )

        # Refit the simulated spectrum.
        fit("sim")

        # Extract the statistic belonging specifically to sim.
        infos = get_stat_info()

        sim_info = next(
            info for info in infos
            if info.ids == ("sim",)
        )

        simulated_statistics.append(float(sim_info.statval))

    except Exception as exc:
        failed += 1
        print(f"\nSimulation {i + 1} failed: {exc}")

    if (i + 1) % 25 == 0:
        print(
            f"Completed {i + 1}/{N_SIM} | "
            f"Successful: {len(simulated_statistics)} | "
            f"Failed: {failed}"
        )

# --------------------------------------------------
# Calculate Monte Carlo goodness-of-fit probability.
# --------------------------------------------------

stats = np.asarray(simulated_statistics)

if len(stats) == 0:
    raise RuntimeError("All simulations failed.")

n_greater = np.count_nonzero(stats >= OBSERVED_STAT)

# Finite-simulation corrected Monte Carlo p-value.
p_value = (n_greater + 1) / (len(stats) + 1)

print("\n========== MONTE CARLO RESULTS ==========")
print("Requested simulations:", N_SIM)
print("Successful simulations:", len(stats))
print("Failed simulations:", failed)
print("Observed W-statistic:", OBSERVED_STAT)
print("Mean simulated W-statistic:", np.mean(stats))
print("Median simulated W-statistic:", np.median(stats))
print("Standard deviation:", np.std(stats, ddof=1))
print("5th percentile:", np.percentile(stats, 5))
print("95th percentile:", np.percentile(stats, 95))
print("Simulations >= observed:", n_greater)
print("Monte Carlo goodness-of-fit p-value:", p_value)

# Save individual statistics.
with open("analysis/monte_carlo_gof_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["simulation", "wstatistic"])

    for i, value in enumerate(stats, start=1):
        writer.writerow([i, value])

# Save summary.
with open("report/notes/monte_carlo_gof_summary.txt", "w") as f:
    f.write("Monte Carlo goodness-of-fit test\n")
    f.write(f"Requested simulations: {N_SIM}\n")
    f.write(f"Successful simulations: {len(stats)}\n")
    f.write(f"Failed simulations: {failed}\n")
    f.write(f"Observed W-statistic: {OBSERVED_STAT:.6f}\n")
    f.write(f"Mean simulated W-statistic: {np.mean(stats):.6f}\n")
    f.write(f"Median simulated W-statistic: {np.median(stats):.6f}\n")
    f.write(f"Standard deviation: {np.std(stats, ddof=1):.6f}\n")
    f.write(f"5th percentile: {np.percentile(stats, 5):.6f}\n")
    f.write(f"95th percentile: {np.percentile(stats, 95):.6f}\n")
    f.write(f"Simulations >= observed: {n_greater}\n")
    f.write(f"Monte Carlo p-value: {p_value:.6f}\n")

print("\nResults saved:")
print("analysis/monte_carlo_gof_results.csv")
print("report/notes/monte_carlo_gof_summary.txt")

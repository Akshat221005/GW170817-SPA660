import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from sherpa.astro.ui import *
from sherpa.astro.xspec import XSTBabs, XSpowerlaw

# Load source spectrum, background, ARF and RMF
load_pha("analysis/spectra/gw170817_05_7.pi")

# Work in keV
set_analysis("energy")

# Use Poisson statistics with background subtraction
set_stat("wstat")

# Select the analysis energy range
notice(0.5, 7.0)
set_xsabund("wilm")
# Construct absorbed power-law model
absorption = XSTBabs()
powerlaw = XSpowerlaw()

model = absorption * powerlaw

# Initial parameter estimates
absorption.nH = 0.078
powerlaw.PhoIndex = 2.0
powerlaw.norm = 1e-5

# Set physically sensible fitting bounds
absorption.nH.min = 0.0
absorption.nH.max = 10.0

powerlaw.PhoIndex.min = 0.0
powerlaw.PhoIndex.max = 5.0

powerlaw.norm.min = 1e-12
powerlaw.norm.max = 1.0

# Assign model and fit
set_model(model)

print("\nStarting spectral fit...")
fit()

# Display best-fit results
print("\n========== FIT RESULTS ==========")
show_fit()
print("\n========== BEST-FIT PARAMETERS ==========")
print("NH =", absorption.nH.val, "10^22 atoms/cm^2")
print("Photon index =", powerlaw.PhoIndex.val)
print("Normalization =", powerlaw.norm.val)

# Plot observed spectrum and fitted model
plot_fit()

plt.xlim(0.5, 7.0)
plt.xlabel("Energy (keV)")
plt.ylabel("Counts/sec/keV")
plt.title("GW170817: Absorbed Power-Law Fit")

plt.savefig(
    "analysis/gw170817_powerlaw_fit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("\nFit plot saved: analysis/gw170817_powerlaw_fit.png")

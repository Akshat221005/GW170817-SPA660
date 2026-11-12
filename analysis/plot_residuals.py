import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from sherpa.astro.ui import *
from sherpa.astro.xspec import XSTBabs, XSpowerlaw

# Load spectrum and response files
load_pha("analysis/spectra/gw170817_05_7.pi")

set_analysis("energy")
set_stat("wstat")
notice(0.5, 7.0)

# Set Wilms abundances
set_xsabund("wilm")

# Reconstruct best-fit model
absorption = XSTBabs()
powerlaw = XSpowerlaw()

absorption.nH = 0.55829446
powerlaw.PhoIndex = 2.04762139
powerlaw.norm = 5.33125212e-6

set_model(absorption * powerlaw)

# Refit
fit()

# Plot ordinary residuals (not delta-chi residuals)
plot_fit_resid()

plt.savefig(
    "analysis/gw170817_residuals.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Residual plot saved successfully.")

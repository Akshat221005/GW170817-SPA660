import numpy as np
from sherpa.astro.ui import *
from sherpa.astro.xspec import XSTBabs, XSpowerlaw

rng = np.random.default_rng(42)

# Load original spectrum.
load_pha("analysis/spectra/gw170817_05_7.pi")
set_analysis("energy")
notice(0.5, 7.0)
set_stat("wstat")
set_xsabund("wilm")

# Best-fit model.
absorption = XSTBabs()
powerlaw = XSpowerlaw()
model = absorption * powerlaw

absorption.nH = 0.5582944636
powerlaw.PhoIndex = 2.0476213938
powerlaw.norm = 5.331252122e-6

set_model(model)
fit()

arf = get_arf()
rmf = get_rmf()
exposure = get_exposure()
source_backscal = get_backscal()

original_bkg = get_bkg()
original_bkg_counts = original_bkg.counts.copy()

print("\nOriginal W-statistic:", get_stat_info()[0].statval)

# Create independent source and background PHA datasets.
sim_source = unpack_pha("analysis/spectra/gw170817_05_7.pi")
sim_background = unpack_pha(
    "analysis/spectra/gw170817_05_7_bkg.pi"
)

# Independently Poisson-resample the background.
sim_background.counts = rng.poisson(original_bkg_counts)

print("Original background total:", original_bkg_counts.sum())
print("Simulated background total:", sim_background.counts.sum())
print(
    "Background channels changed:",
    np.count_nonzero(sim_background.counts != original_bkg_counts)
)

# Register simulated datasets.
set_data("sim", sim_source)
set_bkg("sim", sim_background)
set_analysis("sim", "energy")
set_default_id("sim")
notice(0.5, 7.0)
set_model("sim", model)

# Simulate source counts, including the resampled background.
fake_pha(
    "sim",
    arf=arf,
    rmf=rmf,
    exposure=exposure,
    backscal=source_backscal,
    bkg=sim_background
)

print("\nSimulated source counts:", get_data("sim").counts.sum())
print("Simulated background counts:", get_bkg("sim").counts.sum())

# Fit the simulated spectrum.
fit("sim")
print("\nSimulated fit data points:", get_data().get_filter_expr())
print("Simulated fit statistic:", get_stat_info()[0].statval)
# get_stat_info() takes no dataset argument.
for info in get_stat_info():
    print("\nDataset:", info.ids if hasattr(info, "ids") else info)
    print("Statistic:", info.statval)

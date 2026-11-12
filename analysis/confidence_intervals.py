from sherpa.astro.ui import *
from sherpa.astro.xspec import XSTBabs, XSpowerlaw

# Load source spectrum and associated responses
load_pha("analysis/spectra/gw170817_05_7.pi")

set_analysis("energy")
set_stat("wstat")
notice(0.5, 7.0)

# Set Wilms abundances
set_xsabund("wilm")

# Construct model
absorption = XSTBabs()
powerlaw = XSpowerlaw()
model = absorption * powerlaw

# Set initial parameters
absorption.nH = 0.55829446
powerlaw.PhoIndex = 2.04762139
powerlaw.norm = 5.33125212e-6

set_model(model)

# Refit
fit()

# Calculate 90% confidence intervals
print("\nCalculating 90% confidence intervals...")
set_conf_opt("sigma", 1.64485362695)

conf()

print("\n========== 90% CONFIDENCE INTERVALS ==========")
show_conf()

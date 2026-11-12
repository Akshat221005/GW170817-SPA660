import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from sherpa.astro.ui import *

load_pha("analysis/spectra/gw170817_05_7.pi")

set_analysis("energy")
set_stat("wstat")

group_counts(5)
notice(0.5, 7.0)

plot_data()

# Explicitly restrict the displayed energy range
plt.xlim(0.5, 7.0)
plt.xlabel("Energy (keV)")
plt.ylabel("Counts/sec/keV")
plt.title("GW170817 X-ray Spectrum (0.5–7 keV)")

plt.savefig(
    "analysis/gw170817_spectrum_grouped.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("Updated spectrum saved successfully.")

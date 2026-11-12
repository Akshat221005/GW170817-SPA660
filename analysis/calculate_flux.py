from sherpa.astro.ui import *
from sherpa.astro.xspec import XSTBabs, XSpowerlaw

# Load source spectrum and response files
load_pha("analysis/spectra/gw170817_05_7.pi")

set_analysis("energy")
set_stat("wstat")
notice(0.5, 7.0)

# Use Wilms abundances
set_xsabund("wilm")

# Reconstruct the best-fit model
absorption = XSTBabs()
powerlaw = XSpowerlaw()

absorption.nH = 0.55829446
powerlaw.PhoIndex = 2.04762139
powerlaw.norm = 5.33125212e-6

model = absorption * powerlaw
set_model(model)

# Calculate absorbed and unabsorbed energy flux
absorbed_flux = calc_energy_flux(0.5, 7.0)
unabsorbed_flux = calc_energy_flux(0.5, 7.0, model=powerlaw)

# Display results
print("\n========== GW170817 X-RAY FLUX ==========")
print("Energy range: 0.5-7.0 keV")
print(f"Absorbed flux   = {absorbed_flux:.6e} erg/cm^2/s")
print(f"Unabsorbed flux = {unabsorbed_flux:.6e} erg/cm^2/s")

# Save results
with open("report/notes/xray_flux_results.txt", "w") as f:
    f.write("GW170817 X-ray Flux Results\n")
    f.write("Observation ID: 20860\n")
    f.write("Model: TBabs * PowerLaw\n")
    f.write("Abundances: Wilms et al. (2000)\n")
    f.write("Energy range: 0.5-7.0 keV\n\n")
    f.write(f"Absorbed flux: {absorbed_flux:.8e} erg/cm^2/s\n")
    f.write(f"Unabsorbed flux: {unabsorbed_flux:.8e} erg/cm^2/s\n")

print("\nResults saved to report/notes/xray_flux_results.txt")

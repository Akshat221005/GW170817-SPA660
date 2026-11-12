import math

# Fluxes from the spectral fit (erg/cm^2/s)
absorbed_flux = 1.429842e-14
unabsorbed_flux = 2.189401e-14

# Adopted luminosity distance
distance_mpc = 40.0

# Unit conversions
mpc_to_cm = 3.085677581e24
distance_cm = distance_mpc * mpc_to_cm

# Calculate luminosities
absorbed_luminosity = (
    4 * math.pi * distance_cm**2 * absorbed_flux
)

unabsorbed_luminosity = (
    4 * math.pi * distance_cm**2 * unabsorbed_flux
)

print("\n========== GW170817 X-RAY LUMINOSITY ==========")
print(f"Adopted distance = {distance_mpc} Mpc")
print(f"Absorbed luminosity = {absorbed_luminosity:.6e} erg/s")
print(f"Unabsorbed luminosity = {unabsorbed_luminosity:.6e} erg/s")

with open("report/notes/xray_luminosity_results.txt", "w") as f:
    f.write("GW170817 X-ray Luminosity\n")
    f.write(f"Adopted distance: {distance_mpc} Mpc\n")
    f.write("Energy range: 0.5-7 keV\n")
    f.write(f"Absorbed luminosity: {absorbed_luminosity:.8e} erg/s\n")
    f.write(f"Unabsorbed luminosity: {unabsorbed_luminosity:.8e} erg/s\n")

print("\nResults saved successfully.")

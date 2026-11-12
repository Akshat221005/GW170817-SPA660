"""Proper motion, apparent speed and jet geometry of GW170817.

Input: published VLBI centroid positions (Mooley et al. 2018b, Nature 561, 355)
at mean epochs of 75 and 230 days after the merger. Geometry follows
Mooley et al. (2018a, ApJL 868, L11): Gamma(t_peak) ~ 1/(theta_obs - theta_j)
and theta_obs >~ 6 theta_j.
"""
import math

# Centroid positions (RA seconds of 13h09m, Dec arcsec of -23d22m)
ra1, dec1 = 48.068638, 53.3909   # day 75
ra2, dec2 = 48.068831, 53.3907   # day 230
dec_deg = 23.381484
dt_days = 230 - 75
sigma_theta = 0.3                # mas, total uncertainty (Mooley et al. 2018b)

d_ra = (ra2 - ra1) * 15 * math.cos(math.radians(dec_deg)) * 1e3   # mas
d_dec = abs(dec2 - dec1) * 1e3                                    # mas
theta = math.hypot(d_ra, d_dec)
dt_yr = dt_days / 365.25
mu = theta / dt_yr
print(f"Displacement: dRA cos(dec) = {d_ra:.2f} mas, dDec = {d_dec:.1f} mas, total = {theta:.2f} mas")
print(f"Proper motion: mu = {mu:.2f} +/- {mu * sigma_theta / 2.7:.2f} mas/yr")

MPC_CM, C_CM_S, YR_S = 3.0857e24, 2.99792458e10, 3.15576e7
for d_mpc, d_err in [(41.0, 3.0), (40.0, 0.0)]:
    beta = mu / 1e3 / 206264.806 * d_mpc * MPC_CM / (C_CM_S * YR_S)
    err = beta * math.hypot(sigma_theta / 2.7, d_err / d_mpc)
    print(f"Apparent speed at {d_mpc:.0f} Mpc: beta_app = {beta:.2f} +/- {err:.2f}")

beta_app = 4.1
gamma_min = math.sqrt(1 + beta_app ** 2)
theta_max = 2 * math.degrees(math.atan(1 / beta_app))
diff = math.degrees(1 / beta_app)          # theta_obs - theta_j
theta_j = diff / 5                          # from theta_obs >= 6 theta_j
print(f"Minimum Lorentz factor: {gamma_min:.2f}")
print(f"Upper limit on viewing angle (beta -> 1): {theta_max:.1f} deg")
print(f"theta_obs - theta_j = {diff:.1f} deg  ->  theta_j <~ {theta_j:.1f} deg, "
      f"theta_obs ~ {diff:.0f}-{diff + theta_j:.0f} deg")

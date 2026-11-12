"""Smoothly broken power-law fits to the GW170817 afterglow (3 GHz radio and 1 keV X-ray).

Usage:
    python fit_broken_powerlaw.py gw170817_afterglow_data_v17Apr2025.txt

Fits F(t) = Fb * [0.5 * ((t/tb)^(-s*a1) + (t/tb)^(-s*a2))]^(-1/s)
by weighted least squares in log10(F), using detections only (FluxDErr != -9).
"""
import sys
import numpy as np
from scipy.optimize import curve_fit


def load(path):
    rows = [[x.strip(",") for x in line.split()] for line in open(path)
            if line.strip() and not line.startswith("#")][1:]
    t = np.array([float(r[1]) for r in rows])
    freq = np.array([float(r[3]) for r in rows])
    flux = np.array([float(r[4]) for r in rows])
    err = np.array([float(r[5]) for r in rows])
    return t, freq, flux, err


def sbpl(t, Fb, tb, a1, a2, s):
    return Fb * (0.5 * ((t / tb) ** (-s * a1) + (t / tb) ** (-s * a2))) ** (-1.0 / s)


def fit(t, f, e):
    p0 = [f.max(), 150.0, 0.8, -2.0, 2.0]
    popt, pcov = curve_fit(lambda t, *p: np.log10(sbpl(t, *p)), t, np.log10(f), p0=p0,
                           sigma=e / (f * np.log(10)), absolute_sigma=True, maxfev=50000)
    return popt, np.sqrt(np.diag(pcov))


t, freq, flux, err = load(sys.argv[1] if len(sys.argv) > 1 else "gw170817_afterglow_data_v17Apr2025.txt")
det = err != -9
for name, sel in [("Radio 3 GHz", freq == 3e9), ("X-ray 1 keV", freq > 1e16)]:
    m = sel & det
    p, pe = fit(t[m], flux[m], err[m])
    print(f"{name}  ({m.sum()} detections)")
    for lab, v, ve in zip(["Fb (uJy)", "tb (days)", "alpha1", "alpha2", "s"], p, pe):
        print(f"  {lab:10s} = {v:.4g} +/- {ve:.2g}")

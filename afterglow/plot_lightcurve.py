"""Multi-wavelength light curve in plain default matplotlib style (matches results/Analysis output 1.png).
Usage: python plot_lc_default.py <data.txt> <out.png>"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = [[x.strip(",") for x in l.split()] for l in open(sys.argv[1])
        if l.strip() and not l.startswith("#")][1:]
t = np.array([float(r[1]) for r in rows])
freq = np.array([float(r[3]) for r in rows])
flux = np.array([float(r[4]) for r in rows])
err = np.array([float(r[5]) for r in rows])
is_ul = err == -9

bands = [
    ("VLA 3 GHz", freq == 3e9, "o"),
    ("Other radio", (freq < 1e12) & (freq != 3e9), "s"),
    ("Optical/NIR (HST)", (freq > 1e13) & (freq < 1e16), "^"),
    ("X-ray (1 keV)", freq > 1e16, "D"),
]

fig, ax = plt.subplots(figsize=(8, 5.5))
for i, (name, sel, marker) in enumerate(bands):
    c = f"C{i}"
    d = sel & ~is_ul
    ax.errorbar(t[d], flux[d], yerr=err[d], fmt=marker, ms=5, capsize=2, color=c, label=name)
    u = sel & is_ul
    ax.scatter(t[u], flux[u], marker="v", s=25, facecolors="none", edgecolors=c, alpha=0.6)
ax.scatter([], [], marker="v", s=25, facecolors="none", edgecolors="gray", label="Upper limits (3σ)")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Time since merger (days)")
ax.set_ylabel("Flux density (μJy)")
ax.set_title("GW170817 multi-wavelength afterglow light curve")
ax.grid(True, which="both", alpha=0.3)
ax.set_ylim(1e-6, 2e5)
ax.legend(loc="lower left", ncol=2)
plt.tight_layout()
plt.savefig(sys.argv[2], dpi=150)
print("saved")

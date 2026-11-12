# GW170817 – SPA660 Project (IIT Kanpur)

Chandra X-ray spectral analysis, multi-wavelength afterglow modelling and relativistic jet analysis of the binary neutron star merger **GW170817**.

**Group 1:** Oshita Bongade, Unnati Gangurde, Akshat Dhote

The full report is in [`final_report/`](final_report/).

## Results

| Part | Quantity | This work | Published |
|---|---|---|---|
| 1. Chandra ObsID 20860 | Photon index Γ | 2.06 (90%: 1.46–2.73) | – |
| | Unabsorbed flux, 0.3–10 keV | 2.98 × 10⁻¹⁴ erg cm⁻² s⁻¹ | (2.68 ± 0.26) × 10⁻¹⁴ (Katira et al. 2025, Table 2) |
| 2. Afterglow (3 GHz) | α₁ / α₂ / t_b | 0.84 ± 0.06 / −1.94 ± 0.13 / 156 ± 5 d | – |
| 2. Afterglow (1 keV) | α₁ / α₂ / t_b | 0.72 ± 0.11 / −1.47 ± 0.12 / 147 ± 13 d | – |
| 3. Jet | Proper motion | 6.3 ± 0.7 mas yr⁻¹ | 2.7 ± 0.3 mas in 155 d (Mooley et al. 2018b) |
| | Apparent speed β_app | 4.1 ± 0.5 | 4.1 ± 0.5 (Mooley et al. 2018b) |
| | Half-opening angle θ_j | ≲ 3° | < 5° (Mooley et al. 2018b) |
| | Observing angle θ_obs | ≈ 14–17° | 14–28° (Mooley et al. 2018b) |

## Repository layout

```
final_report/   Final report (.docx and .pdf)
analysis/       Chandra analysis: region files, Sherpa scripts, extracted spectra + responses, XSPEC sessions
report/         Notes with numerical results, spectral plots, DS9 screenshots
afterglow/      Multi-wavelength dataset, broken power-law fit and light-curve plot
jet/            Proper motion, apparent speed and jet-geometry calculation
```

## Reproducing the analysis

**Part 1 – Chandra (CIAO 4.18, CALDB 4.12.4, XSPEC 13).** Download ObsID 20860 from the [Chandra Data Archive](https://cda.harvard.edu/chaser/) into `data/20860`, then:

```bash
chandra_repro indir=data/20860 outdir=analysis/repro
specextract infile="analysis/repro/acisf20860_repro_evt2.fits[energy=500:7000][sky=region(analysis/source.reg)]" \
    bkgfile="analysis/repro/acisf20860_repro_evt2.fits[energy=500:7000][sky=region(analysis/background.reg)]" \
    outroot=analysis/spectra/gw170817_05_7 correctpsf=no weight=yes clobber=yes
cd analysis/spectra
xspec - gw170817_final_fit.xcm     # then: fit; error 2.706 1 2 3; flux 0.3 10.0
```

The extracted spectra and responses are already included in `analysis/spectra/`, so the XSPEC step can be run directly. The raw event files are not included because of their size.

**Part 2 – Afterglow.**

```bash
cd afterglow
python fit_broken_powerlaw.py gw170817_afterglow_data_v17Apr2025.txt
python plot_lightcurve.py gw170817_afterglow_data_v17Apr2025.txt multiwavelength_lightcurve.png
```

**Part 3 – Jet.**

```bash
cd jet
python jet_kinematics.py
```

Requires Python 3 with `numpy`, `scipy` and `matplotlib` (plus CIAO/Sherpa for the scripts in `analysis/`).

## Data and references

- Chandra ObsID 20860, Chandra Data Archive.
- Afterglow dataset: `gw170817_afterglow_data_v17Apr2025.txt` (Makhathini et al. 2021, ApJ 922, 154, with later updates incl. Katira et al. 2025).
- Katira, Mooley & Hotokezaka (2025), MNRAS 539, 2654.
- Mooley et al. (2018a), ApJL 868, L11; Mooley et al. (2018b), Nature 561, 355.

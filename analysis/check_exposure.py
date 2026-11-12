import numpy as np
from astropy.io import fits

filename = "analysis/gw170817_fine_0.5-7_thresh.expmap"

with fits.open(filename) as hdul:
    data = hdul[0].data

    if data is None:
        for hdu in hdul:
            if hdu.data is not None:
                data = hdu.data
                break

    data = np.squeeze(data)

# Exposure map coordinate transformation from dmlist:
# SKY(X) = 2083 + (image_x - 1)
# SKY(Y) = 2808 + (image_y - 1)

y, x = np.indices(data.shape)

sky_x = 2083 + x
sky_y = 2808 + y

cx, cy = 4108.63, 4101.88

distance = np.sqrt((sky_x-cx)**2 + (sky_y-cy)**2)

source = distance <= 4
background = (distance >= 10) & (distance <= 30)

def report(name, mask):
    values = data[mask]
    valid = values > 0

    print(f"\n{name}")
    print(f"Total pixels: {len(values)}")
    print(f"Zero-exposure pixels: {np.sum(~valid)}")
    print(f"Mean exposure (all pixels): {np.mean(values):.2f} cm^2 s")
    print(f"Mean exposure (positive pixels): {np.mean(values[valid]):.2f} cm^2 s")
    print(f"Median exposure (positive pixels): {np.median(values[valid]):.2f} cm^2 s")

report("SOURCE REGION", source)
report("BACKGROUND REGION", background)

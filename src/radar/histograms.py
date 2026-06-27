from pathlib import Path
from spectral import open_image
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]

cpr = open_image(
    str(ROOT / "data" / "cpr" / "cpr.bin.hdr")
).load()

dop = open_image(
    str(ROOT / "data" / "dop" / "dop.bin.hdr")
).load()

cpr = np.squeeze(cpr)
dop = np.squeeze(dop)

cpr = cpr[np.isfinite(cpr)]
dop = dop[np.isfinite(dop)]

# remove extreme outliers
cpr = cpr[cpr < 10]

plt.figure(figsize=(10,5))
plt.hist(cpr, bins=200)
plt.title("CPR Histogram")
plt.xlabel("CPR")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(10,5))
plt.hist(dop, bins=200)
plt.title("DOP Histogram")
plt.xlabel("DOP")
plt.ylabel("Frequency")
plt.show()
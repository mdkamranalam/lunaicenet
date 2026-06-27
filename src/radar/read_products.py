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

# remove channel dimension
cpr = np.squeeze(cpr)
dop = np.squeeze(dop)

# replace NaNs
cpr = np.nan_to_num(cpr)
dop = np.nan_to_num(dop)

print("CPR")
print("shape:", cpr.shape)
print("min:", np.min(cpr))
print("max:", np.max(cpr))

print()

print("DOP")
print("shape:", dop.shape)
print("min:", np.min(dop))
print("max:", np.max(dop))

plt.figure(figsize=(10,6))
plt.imshow(cpr, cmap='gray')
plt.title("CPR")
plt.colorbar()
plt.show()

plt.figure(figsize=(10,6))
plt.imshow(dop, cmap='gray')
plt.title("DOP")
plt.colorbar()
plt.show()
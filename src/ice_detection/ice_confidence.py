from pathlib import Path
from spectral import open_image
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]

print("Loading CPR...")
cpr = open_image(
    str(ROOT / "data/cpr/cpr.bin.hdr")
).load()

print("Loading DOP...")
dop = open_image(
    str(ROOT / "data/dop/dop.bin.hdr")
).load()

# Remove singleton dimensions
cpr = np.squeeze(cpr)
dop = np.squeeze(dop)

# Replace NaNs
cpr = np.nan_to_num(cpr)
dop = np.nan_to_num(dop)

print("\nInput Statistics")
print("----------------")
print("CPR shape:", cpr.shape)
print("DOP shape:", dop.shape)
print("CPR range:", np.min(cpr), "->", np.max(cpr))
print("DOP range:", np.min(dop), "->", np.max(dop))

# ----------------------------------------------------
# Ice confidence map
# 0 = no evidence
# 1 = low confidence
# 2 = medium confidence
# 3 = high confidence
# ----------------------------------------------------
ice = np.zeros(cpr.shape, dtype=np.uint8)

# Low confidence
ice[cpr > 0.7] = 1

# Medium confidence
ice[(cpr > 1.0) & (dop < 0.30)] = 2

# High confidence
ice[(cpr > 1.5) & (dop < 0.13)] = 3

# ----------------------------------------------------
# Statistics
# ----------------------------------------------------
print("\nIce Statistics")
print("----------------")

print(
    "Low confidence:",
    np.sum(ice == 1)
)

print(
    "Medium confidence:",
    np.sum(ice == 2)
)

print(
    "High confidence:",
    np.sum(ice == 3)
)

print(
    "Total pixels:",
    ice.size
)

# ----------------------------------------------------
# Save
# ----------------------------------------------------
ICE_DIR = ROOT / "data" / "ice"
ICE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT = ICE_DIR / "ice_confidence.npy"

np.save(
    OUTPUT,
    ice
)

print("\nSaved:")
print(OUTPUT)

# ----------------------------------------------------
# Visualization
# ----------------------------------------------------
display = ice[::20, ::20]

plt.figure(figsize=(8, 12))

im = plt.imshow(
    display,
    cmap="viridis",
    aspect="auto",
    interpolation="nearest"
)

cbar = plt.colorbar(im)
cbar.set_ticks([0, 1, 2, 3])
cbar.set_ticklabels([
    "None",
    "Low",
    "Medium",
    "High"
])

plt.title("Lunar Ice Confidence Map")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.tight_layout()
plt.show()
from pathlib import Path
from spectral import open_image
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]

print("Loading CPR...")
cpr = open_image(
    str(ROOT/"data/cpr/cpr.bin.hdr")
).load()

print("Loading DOP...")
dop = open_image(
    str(ROOT/"data/dop/dop.bin.hdr")
).load()

cpr = np.squeeze(cpr)
dop = np.squeeze(dop)

# remove invalid values
cpr = np.nan_to_num(cpr)
dop = np.nan_to_num(dop)

ice = np.zeros(cpr.shape)

# low confidence
ice[(cpr > 0.7)] = 1

# medium confidence
ice[(cpr > 1.0) & (dop < 0.30)] = 2

# high confidence
ice[(cpr > 1.5) & (dop < 0.13)] = 3

print()
print("Low confidence:",
      np.sum(ice==1))

print("Medium confidence:",
      np.sum(ice==2))

print("High confidence:",
      np.sum(ice==3))

plt.figure(figsize=(8,12))

plt.imshow(
    ice,
    aspect='auto',
    interpolation='nearest'
)

plt.title("Ice Confidence Map")
plt.colorbar()

plt.show()
import numpy as np
import matplotlib.pyplot as plt

print("Loading hazard map...")

hazard = np.load("data/dem/hazard.npy")

# -------------------------------------------------
# Normalize hazard map
# -------------------------------------------------
hazard = hazard.astype(np.float32)
hazard = hazard / np.nanmax(hazard)

# -------------------------------------------------
# Much stricter lunar safety threshold
# -------------------------------------------------
SAFE_THRESHOLD = 0.06

print()
print("Using hazard threshold:", SAFE_THRESHOLD)

# safe terrain mask
safe = hazard < SAFE_THRESHOLD

# save
np.save(
    "data/dem/safe_zones.npy",
    safe
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------
safe_pixels = np.sum(safe)
total_pixels = safe.size

print("\nSafe Zone Statistics")
print("--------------------")
print("Total pixels :", total_pixels)
print("Safe pixels  :", safe_pixels)
print(
    "Safe percent :",
    round(
        100 * safe_pixels / total_pixels,
        2
    ),
    "%"
)

# -------------------------------------------------
# Visualization
# -------------------------------------------------
display = safe[::20, ::20]

plt.figure(figsize=(10,6))

plt.imshow(
    display,
    cmap="gray",
    interpolation="nearest"
)

plt.title(
    f"Lunar Safe Zones (threshold={SAFE_THRESHOLD})"
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.tight_layout()
plt.show()
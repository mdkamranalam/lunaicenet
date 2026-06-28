import numpy as np
import matplotlib.pyplot as plt

print("Loading hazard map...")

hazard = np.load("data/dem/hazard.npy")

# normalize
hazard = hazard / np.nanmax(hazard)

# threshold
SAFE_THRESHOLD = 0.15

safe = hazard < SAFE_THRESHOLD

np.save(
    "data/dem/safe_zones.npy",
    safe
)

print("\nSafe Zone Statistics")
print("-------------------")
print("Total pixels:", safe.size)
print("Safe pixels :", np.sum(safe))
print(
    "Safe %",
    100*np.sum(safe)/safe.size
)

display = safe[::20, ::20]

plt.figure(figsize=(10,6))
plt.imshow(display, cmap="gray")
plt.title("Lunar Safe Zones")
plt.tight_layout()
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

print("Loading products...")

# -------------------------
# Load products
# -------------------------
ice = np.load("data/ice/ice_confidence.npy")
hazard = np.load("data/dem/hazard.npy")
safe = np.load("data/dem/safe_zones.npy")

print("Ice:", ice.shape)
print("Hazard:", hazard.shape)
print("Safe:", safe.shape)

# -------------------------
# Match resolutions
# -------------------------
target_shape = safe.shape

if ice.shape != target_shape:
    scale_y = target_shape[0] / ice.shape[0]
    scale_x = target_shape[1] / ice.shape[1]

    print(
        f"Resampling ice by "
        f"({scale_y:.4f}, {scale_x:.4f})"
    )

    ice = zoom(
        ice,
        (scale_y, scale_x),
        order=0      # nearest neighbour
    )

    ice = ice[:target_shape[0], :target_shape[1]]

if hazard.shape != target_shape:
    scale_y = target_shape[0] / hazard.shape[0]
    scale_x = target_shape[1] / hazard.shape[1]

    print(
        f"Resampling hazard by "
        f"({scale_y:.4f}, {scale_x:.4f})"
    )

    hazard = zoom(
        hazard,
        (scale_y, scale_x),
        order=1
    )

    hazard = hazard[:target_shape[0], :target_shape[1]]

# -------------------------
# Normalize hazard
# -------------------------
hazard = hazard / np.nanmax(hazard)

# -------------------------
# Convert ice confidence
# -------------------------
ice_score = np.zeros_like(
    ice,
    dtype=np.float32
)

ice_score[ice == 1] = 0.20
ice_score[ice == 2] = 0.60
ice_score[ice == 3] = 1.00

# -------------------------
# Landing suitability
# -------------------------
landing = (
    0.55 * safe +
    0.30 * ice_score +
    0.15 * (1 - hazard)
)

# Normalize
landing = (
    landing - landing.min()
) / (
    landing.max() - landing.min()
)

# -------------------------
# Save
# -------------------------
np.save(
    "data/landing_score.npy",
    landing
)

# -------------------------
# Statistics
# -------------------------
print()
print("Landing Statistics")
print("------------------")
print("Min:", np.min(landing))
print("Max:", np.max(landing))
print("Mean:", np.mean(landing))

print()
print(
    "Excellent sites:",
    np.sum(landing > 0.8)
)

print(
    "Good sites:",
    np.sum(
        (landing > 0.6) &
        (landing <= 0.8)
    )
)

print(
    "Poor sites:",
    np.sum(landing <= 0.6)
)

# -------------------------
# Visualization
# -------------------------
display = landing[::20, ::20]

plt.figure(figsize=(10,6))

plt.imshow(
    display,
    cmap="viridis",
    vmin=np.percentile(display, 5),
    vmax=np.percentile(display, 95)
)

plt.colorbar(
    label="Landing Suitability"
)

plt.title(
    "Lunar Landing Suitability Map"
)

plt.tight_layout()
plt.show()
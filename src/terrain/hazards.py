import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

print("Loading terrain products...")

slope = np.load("data/dem/slope.npy")
roughness = np.load("data/dem/roughness.npy")

print("Slope shape:", slope.shape)
print("Roughness shape:", roughness.shape)

# Normalize
slope_n = slope / np.nanmax(slope)
rough_n = roughness / np.nanmax(roughness)

# Resample roughness to match slope resolution
if slope_n.shape != rough_n.shape:
    scale_y = slope_n.shape[0] / rough_n.shape[0]
    scale_x = slope_n.shape[1] / rough_n.shape[1]

    print(f"Resampling roughness by factors ({scale_y:.2f}, {scale_x:.2f})")

    rough_n = zoom(
        rough_n,
        (scale_y, scale_x),
        order=1  # bilinear interpolation
    )

    # Ensure exact shape match
    rough_n = rough_n[:slope_n.shape[0], :slope_n.shape[1]]

# Compute hazard map
hazard = (
    0.4*slope_n +
    0.6*rough_n
)

# Save
np.save("data/dem/hazard.npy", hazard)

print("\nHazard Statistics")
print("------------------")
print("Min:", np.nanmin(hazard))
print("Max:", np.nanmax(hazard))
print("Mean:", np.nanmean(hazard))

# Display downsampled image for visualization
display = hazard[::20, ::20]

plt.figure(figsize=(10, 6))
plt.imshow(
    display,
    cmap="inferno",
    vmin=np.percentile(display, 5),
    vmax=np.percentile(display, 99)
)
plt.colorbar(label="Hazard")
plt.title("Lunar Hazard Map")
plt.tight_layout()
plt.show()
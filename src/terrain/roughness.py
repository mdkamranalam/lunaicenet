import rasterio
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import generic_filter

DEM_PATH = "data/dem/lola_dem.tif"

print("Loading DEM...")

with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)

# Downsample first
print("Downsampling DEM...")
dem = dem[::20, ::20]

print("DEM shape:", dem.shape)

print("Computing roughness...")

roughness = generic_filter(
    dem,
    np.std,
    size=5
)

print("\nRoughness Statistics")
print("-------------------")
print("Min:", np.nanmin(roughness))
print("Max:", np.nanmax(roughness))
print("Mean:", np.nanmean(roughness))

np.save("data/dem/roughness.npy", roughness)

plt.figure(figsize=(10,6))
plt.imshow(
    roughness,
    cmap="viridis",
    vmin=np.percentile(roughness,5),
    vmax=np.percentile(roughness,99)
)

plt.colorbar(label="Terrain Roughness")
plt.title("Lunar Terrain Roughness")
plt.tight_layout()
plt.show()
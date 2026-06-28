import rasterio
import numpy as np
import matplotlib.pyplot as plt

DEM_PATH = "data/dem/lola_dem.tif"

with rasterio.open(DEM_PATH) as src:
    dem = src.read(1)

dy, dx = np.gradient(dem)
slope = np.sqrt(dx**2 + dy**2)

print("Slope")
print("Min:", np.nanmin(slope))
print("Max:", np.nanmax(slope))
print("Mean:", np.nanmean(slope))

np.save("data/dem/slope.npy", slope)

display = slope[::20, ::20]

plt.figure(figsize=(10,6))
plt.imshow(display, cmap="inferno")
plt.colorbar(label="Slope")
plt.title("Lunar Slope Map")
plt.show()
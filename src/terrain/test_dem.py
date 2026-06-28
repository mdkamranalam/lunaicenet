import rasterio
import matplotlib.pyplot as plt

DEM_PATH = r"data/dem/SLDEM2015_128_60S_60N_000_360_FLOAT.IMG"

print("Opening DEM...")

with rasterio.open(DEM_PATH) as src:
    print()
    print("Driver:", src.driver)
    print("Width:", src.width)
    print("Height:", src.height)
    print("Bands:", src.count)
    print("CRS:", src.crs)

    dem = src.read(1)

print()
print("DEM Statistics")
print("----------------")
print("Shape:", dem.shape)
print("Min:", dem.min())
print("Max:", dem.max())

plt.figure(figsize=(10,6))
plt.imshow(dem)
plt.colorbar()
plt.title("SLDEM2015")
plt.show()
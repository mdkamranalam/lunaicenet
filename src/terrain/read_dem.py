import rasterio
import matplotlib.pyplot as plt

def load_dem(path):
    with rasterio.open(path) as src:
        dem = src.read(1)
        transform = src.transform
        resolution = src.res

    return dem, transform, resolution

if __name__ == "__main__":
    DEM_PATH = "data/dem/lola_dem.tif"

    dem, transform, resolution = load_dem(DEM_PATH)

    print()
    print("DEM loaded")
    print("Shape:", dem.shape)
    print("Resolution:", resolution)
    print("Min:", dem.min())
    print("Max:", dem.max())

    plt.figure(figsize=(8,8))
    plt.imshow(dem)
    plt.colorbar()
    plt.title("Lunar DEM")
    plt.show()
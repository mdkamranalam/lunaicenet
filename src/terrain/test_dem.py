import rasterio

with rasterio.open("data/dem/lola_dem.tif") as src:
    print("Driver:", src.driver)
    print("Width:", src.width)
    print("Height:", src.height)
    print("Bands:", src.count)

    dem = src.read(1)

print("Shape:", dem.shape)
print("Min:", dem.min())
print("Max:", dem.max())
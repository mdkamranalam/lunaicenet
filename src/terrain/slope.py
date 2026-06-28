import numpy as np
import matplotlib.pyplot as plt
from read_dem import load_dem

def calculate_slope(dem):
    dx = np.gradient(dem, axis=1)
    dy = np.gradient(dem, axis=0)
    slope = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))
    return slope


if __name__ == "__main__":
    dem, _, _ = load_dem("data/dem/lola_dem.tif")
    slope = calculate_slope(dem)

    print()
    print("Slope statistics")
    print("Min:", slope.min())
    print("Max:", slope.max())
    print("Mean:", slope.mean())

    plt.figure(figsize=(8,8))
    plt.imshow(slope)
    plt.colorbar()
    plt.title("Slope Map")
    plt.show()
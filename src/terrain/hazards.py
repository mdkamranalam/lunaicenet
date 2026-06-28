import numpy as np
import matplotlib.pyplot as plt

from read_dem import load_dem
from slope import calculate_slope
from roughness import calculate_roughness

if __name__ == "__main__":
    dem, _, _ = load_dem("data/dem/lola_dem.tif")
    slope = calculate_slope(dem)
    roughness = calculate_roughness(dem)
    hazard = np.zeros(dem.shape)
    hazard += (slope > 15)
    hazard += (roughness > np.percentile(roughness, 90))

    plt.figure(figsize=(8,8))
    plt.imshow(hazard)
    plt.colorbar()
    plt.title("Terrain Hazard Map")
    plt.show()
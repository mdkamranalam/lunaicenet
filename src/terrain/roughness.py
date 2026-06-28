import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import generic_filter
from read_dem import load_dem

def calculate_roughness(dem):
    roughness = generic_filter(dem, np.std, size=5)
    return roughness

if __name__ == "__main__":
    dem, _, _ = load_dem("data/dem/lola_dem.tif")
    roughness = calculate_roughness(dem)

    print()
    print("Roughness statistics")
    print("Min:", roughness.min())
    print("Max:", roughness.max())
    print("Mean:", roughness.mean())

    plt.figure(figsize=(8,8))
    plt.imshow(roughness)
    plt.colorbar()
    plt.title("Terrain Roughness")
    plt.show()
import numpy as np

def compute_slope(dem, resolution_m=2.0):
    """Compute slope in degrees from a DEM."""
    dy, dx = np.gradient(dem, resolution_m)
    slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
    slope_deg = np.degrees(slope_rad)
    return slope_deg

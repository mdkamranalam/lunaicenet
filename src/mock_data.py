import numpy as np
from scipy.ndimage import gaussian_filter

def generate_mock_dem(size=(200, 200)):
    """Generate a synthetic Digital Elevation Model with a crater."""
    # Base terrain
    dem = np.random.normal(0, 0.5, size)
    
    # Create a crater (Gaussian depression)
    center = (size[0] // 2, size[1] // 2)
    y, x = np.ogrid[-center[0]:size[0]-center[0], -center[1]:size[1]-center[1]]
    distance = np.sqrt(x*x + y*y)
    
    # Crater parameters
    radius = 40
    depth = 20
    rim_height = 5
    
    # Crater depression
    crater_profile = np.exp(-(distance**2) / (2 * (radius/2)**2)) * -depth
    # Crater rim (donut shape)
    rim_profile = np.exp(-((distance - radius)**2) / (2 * 10**2)) * rim_height
    
    dem += crater_profile + rim_profile
    return gaussian_filter(dem, sigma=2)

def generate_mock_radar(dem_shape=(200, 200)):
    """Generate synthetic HH, HV, VV radar data."""
    # Base speckle noise
    hh = np.random.exponential(scale=1.0, size=dem_shape)
    hv = np.random.exponential(scale=0.2, size=dem_shape)
    vv = np.random.exponential(scale=1.0, size=dem_shape)
    
    # Add high backscatter (rocks) around the rim
    # Recreate distance map
    center = (dem_shape[0] // 2, dem_shape[1] // 2)
    y, x = np.ogrid[-center[0]:dem_shape[0]-center[0], -center[1]:dem_shape[1]-center[1]]
    distance = np.sqrt(x*x + y*y)
    
    radius = 40
    rim_mask = (distance > radius - 5) & (distance < radius + 15)
    
    # Simulate high cross-pol (HV) and high like-pol for rocks
    hh[rim_mask] += np.random.normal(2.0, 0.5, size=hh[rim_mask].shape)
    hv[rim_mask] += np.random.normal(1.0, 0.2, size=hv[rim_mask].shape)
    vv[rim_mask] += np.random.normal(2.0, 0.5, size=vv[rim_mask].shape)
    
    # Inside the crater floor (simulating ice: high CPR, low DOP)
    floor_mask = distance < radius - 15
    hh[floor_mask] += np.random.normal(1.5, 0.2, size=hh[floor_mask].shape)
    vv[floor_mask] += np.random.normal(1.5, 0.2, size=vv[floor_mask].shape)
    hv[floor_mask] += np.random.normal(1.2, 0.2, size=hv[floor_mask].shape) # Ice has high cross-pol too
    
    return hh, hv, vv

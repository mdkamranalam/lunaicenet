import numpy as np
from scipy.ndimage import median_filter

def apply_speckle_filter(band, size=3):
    """Simple median filter as a placeholder for Refined Lee."""
    return median_filter(band, size=size)

def compute_cpr_dop(hh, hv, vv):
    """Compute CPR and DOP from HH, HV, VV channels."""
    # Filter bands
    hh_f = apply_speckle_filter(hh)
    hv_f = apply_speckle_filter(hv)
    vv_f = apply_speckle_filter(vv)
    
    # Power
    P_hh = hh_f ** 2
    P_vv = vv_f ** 2
    P_hv = hv_f ** 2
    
    # CPR = Same Sense / Opposite Sense
    # Using a simplified heuristic for the MVP:
    SC = P_hh + P_vv
    OC = 2 * P_hv
    # Prevent division by zero
    cpr = np.divide(SC, OC, out=np.zeros_like(SC), where=OC!=0)
    
    # DOP
    I = P_hh + P_vv + 1e-6
    Q = P_hh - P_vv
    U = 2 * hh_f * vv_f # approximation
    dop = np.sqrt(Q**2 + U**2) / I
    
    # Clip for clean visualization
    cpr = np.clip(cpr, 0, 3)
    dop = np.clip(dop, 0, 1)
    
    return cpr, dop

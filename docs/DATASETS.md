# Datasets and Data Sources

LunaIceNet relies on a multi-modal fusion of radar, optical, and topographical datasets. This document details the datasets used in the pipeline, their sources, and their specific roles.

## 1. Chandrayaan-2 Dual-Frequency SAR (DFSAR)
The primary instrument for subsurface analysis. DFSAR provides fully polarimetric radar data capable of penetrating the lunar regolith.
- **Source**: ISRO PDS (PRADAN / Bhuvan)
- **Bands**: L-band (1.25 GHz, ~5m penetration) and S-band (2.5 GHz, ~2m penetration).
- **Resolution**: High-resolution mode up to ~2 m slant-range.
- **Channels**: HH, HV, VH, VV.
- **Role in Pipeline**: 
  - Converted to calibrated backscatter (σ⁰).
  - Used to compute Stokes parameters, leading to Circular Polarization Ratio (CPR) and Degree of Polarization (DOP) maps.

## 2. Chandrayaan-2 Orbiter High Resolution Camera (OHRC)
The highest resolution optical camera currently orbiting the Moon.
- **Source**: ISRO PDS / Kaggle datasets
- **Resolution**: 0.25 m/pixel GSD (Ground Sample Distance).
- **Role in Pipeline**:
  - Boulder counting and hazard detection for landing site safety scoring.
  - Verification of surface morphology in illuminated regions adjacent to PSRs.

## 3. LRO Lunar Orbiter Laser Altimeter (LOLA) DEM
Digital Elevation Models generated from laser altimetry provide critical topographical context.
- **Source**: NASA / USGS (Global), NASA PGDA (Polar Targeted).
- **Resolution**: 118 m (Global) and 5 m (Targeted Polar regions).
- **Role in Pipeline**:
  - **Slope Map Generation**: Essential for filtering out rough, steep crater walls (false positives for ice) and for landing site safety and rover path planning.
  - **Roughness Computation**: Measures terrain ruggedness.
  - **Elevation Context**: Defines the boundaries of craters and PSRs.

## 4. LROC Polar Illumination Maps
Maps detailing the percentage of time a specific pixel receives solar illumination over a lunar cycle/year.
- **Source**: ASU / LROC (Lunar Reconnaissance Orbiter Camera).
- **Role in Pipeline**:
  - Delineating true Permanently Shadowed Regions (PSRs) where illumination is strictly 0%.
  - Calculating solar power availability for lander and rover operations during the traverse.

## 5. KPLO ShadowCam & LROC NAC Images (Optional/Ancillary)
ShadowCam is specifically designed to image within PSRs using secondary scattered light.
- **Source**: ASU / NASA.
- **Role in Pipeline**:
  - Ground-truthing radar-bright areas to visually confirm if they are rocky outcrops or smooth ice-bearing regolith.
  - Enhancing the explainability of the ML model outputs.

## Data Preprocessing Requirements
1. **Co-registration**: All datasets must be reprojected and co-registered to a common lunar polar stereographic CRS (Coordinate Reference System) to ensure pixel-to-pixel alignment across radar, DEM, and optical layers.
2. **Calibration**: Raw DFSAR Digital Numbers (DN) must be radiometrically calibrated to sigma-nought (σ⁰) values using ISRO-provided calibration coefficients.

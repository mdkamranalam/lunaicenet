<p align="center">
  <img src="https://img.shields.io/badge/Mission-Chandrayaan--2-blue?style=for-the-badge" alt="Mission Badge"/>
  <img src="https://img.shields.io/badge/Hackathon-ISRO Bharatiya Antariksh Hackathon 2026-orange?style=for-the-badge" alt="Problem Statement Badge"/>
  <img src="https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License Badge"/>
</p>

# 🌙 LunaIceNet

> **Subsurface Ice Detection in Doubly-Shadowed Lunar Craters using Polarimetric SAR & Machine Learning**

LunaIceNet is an end-to-end pipeline for detecting and quantifying subsurface water-ice deposits within **Permanently Shadowed Regions (PSRs)** of the Moon's south pole. It leverages **Chandrayaan-2 DFSAR** full-polarimetric radar data, high-resolution **OHRC** imagery, and **LRO-LOLA** digital elevation models — combined with machine learning — to produce ice-probability maps, safe landing-site recommendations, optimized rover traverse paths, and volumetric ice estimates.

---

## 📋 Table of Contents

- [Scientific Background](#-scientific-background)
- [Key Features](#-key-features)
- [Architecture & Pipeline](#-architecture--pipeline)
- [Tech Stack](#-tech-stack)
- [Datasets](#-datasets)
- [Installation](#-installation)
- [Usage](#-usage)
- [Deliverables](#-deliverables)
- [Team & Timeline](#-team--timeline)
- [References](#-references)
- [License](#-license)

---

## 🔬 Scientific Background

### Permanently Shadowed Regions (PSRs)

Lunar polar PSRs are terrain formations that never receive direct sunlight, maintaining extremely cold temperatures (often **< 100 K**) and acting as natural cold traps for volatiles. **Doubly-shadowed craters** — small craters nested inside larger PSRs whose raised rims block even scattered light — reach floor temperatures as low as **~25 K**, making them the highest-priority targets for water-ice exploration.

### Radar Scattering Physics

Fully polarimetric SAR transmits and receives both horizontal (H) and vertical (V) polarizations, enabling computation of key polarimetric invariants:

| Metric | Definition | Ice Signature |
|--------|-----------|---------------|
| **CPR** (Circular Polarization Ratio) | Ratio of same-sense to opposite-sense circular-polarized echoes | **CPR > 1.0** (multiple internal scattering) |
| **DOP** (Degree of Polarization) | Fraction of reflected wave retaining original polarization | **DOP < 0.13** (volumetric scatter depolarizes signal) |

Prior work suggested CPR > 1 & DOP < 0.35 as ice indicators; Chandrayaan-2 analysis refined the DOP threshold to **< 0.13** for higher confidence.

### The False-Positive Challenge

Elevated CPR can also arise from rough, blocky terrain (crater walls, ejecta fields). For example, Shackleton crater's walls are radar-bright yet lack ice evidence, and Faustini crater's radar-bright PSR areas correspond to rock exposures. LunaIceNet addresses this through **multi-feature ML classification** combining radar metrics with terrain context.

---

## ✨ Key Features

- **🛰️ Polarimetric Radar Processing** — Full-pipeline DFSAR calibration, speckle filtering (Refined Lee), and CPR/DOP map generation
- **🤖 ML-Based Ice Classification** — Random Forest / XGBoost classifier using multi-dimensional features (CPR, DOP, σ⁰, slope, roughness, illumination) to suppress false positives
- **🗺️ Ice-Probability Mapping** — Per-pixel probability maps (0–1) of ice presence across the crater floor
- **🏔️ Terrain & Safety Analysis** — Slope, roughness, boulder detection, and illumination scoring for landing-site selection
- **🚀 Landing-Site Recommendation** — Composite safety scoring with weighted slope, illumination, and boulder-density criteria
- **🛤️ Rover Path Planning** — A*/D* pathfinding on cost grids weighted by terrain difficulty, energy cost, and hazard avoidance
- **📊 Ice Volume Estimation** — Quantitative ice volume calculation with uncertainty bounds using backscatter-to-dielectric mixing models

---

## 🏗️ Architecture & Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LunaIceNet Pipeline                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │  DFSAR Data   │    │  OHRC Images │    │  LOLA DEM + Illum.  │   │
│  │ (L/S-band)    │    │  (0.25m GSD) │    │  Maps               │   │
│  └──────┬───────┘    └──────┬───────┘    └──────────┬───────────┘   │
│         │                   │                       │               │
│         ▼                   ▼                       ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │ Calibration   │    │   Boulder    │    │  Slope / Roughness  │   │
│  │ + Speckle     │    │  Detection   │    │  + Illumination     │   │
│  │   Filter      │    │              │    │    Analysis         │   │
│  └──────┬───────┘    └──────┬───────┘    └──────────┬───────────┘   │
│         │                   │                       │               │
│         ▼                   │                       │               │
│  ┌──────────────┐           │                       │               │
│  │  CPR / DOP   │           │                       │               │
│  │  Computation  │           │                       │               │
│  └──────┬───────┘           │                       │               │
│         │                   │                       │               │
│         └───────────────────┼───────────────────────┘               │
│                             │                                       │
│                             ▼                                       │
│                  ┌────────────────────┐                              │
│                  │  ML Classifier     │                              │
│                  │ (RF / XGBoost)     │                              │
│                  │  Features: CPR,    │                              │
│                  │  DOP, σ⁰, slope,  │                              │
│                  │  roughness, illum. │                              │
│                  └────────┬───────────┘                              │
│                           │                                         │
│              ┌────────────┼────────────┐                            │
│              ▼            ▼            ▼                            │
│     ┌──────────────┐ ┌─────────┐ ┌──────────────┐                  │
│     │ Ice-Prob Map │ │ Landing │ │ Rover Path   │                  │
│     │ + Volume Est.│ │  Site   │ │ Planning     │                  │
│     │              │ │ Scoring │ │ (A* / D*)    │                  │
│     └──────────────┘ └─────────┘ └──────────────┘                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Pipeline Stages

1. **Data Ingestion** — Load DFSAR full-polarization image stack (HH, HV, VH, VV channels) in GeoTIFF/PDS4 format
2. **Calibration** — Convert raw DN to calibrated backscatter (σ⁰) using MIDAS coefficients
3. **Speckle Filtering** — Apply Refined Lee polarimetric filter to reduce noise while preserving edges
4. **CPR/DOP Computation** — Derive Circular Polarization Ratio and Degree of Polarization via Stokes parameters
5. **Co-registration & Masking** — Align SAR maps with DEM/OHRC; mask non-PSR and low-SNR regions
6. **Feature Engineering** — Assemble per-pixel feature vectors (CPR, DOP, σ⁰, slope, roughness, illumination)
7. **ML Classification** — Train Random Forest/XGBoost to separate ice from rock; output ice-probability map
8. **Terrain & Safety Scoring** — Score candidate landing sites using composite criteria
9. **Path Planning** — Run A*/D* on cost grid from landing site to ice target
10. **Volume Estimation** — Calculate ice volume with uncertainty: `V = A × depth × f`

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| **SAR Processing** | ISRO MIDAS, PolSARPro/SNAP |
| **Geospatial I/O** | `rasterio`, `GDAL`, QGIS/ArcGIS |
| **Numerical Computing** | `NumPy`, `SciPy` |
| **Machine Learning** | `scikit-learn` (Random Forest), `XGBoost` |
| **Visualization** | `matplotlib`, QGIS |
| **Image Analysis** | ENVI/IDL, MATLAB (optional) |
| **Notebooks & VCS** | Jupyter, Git |
| **Language** | Python 3.9+ |

---

## 📡 Datasets

| Dataset | Source | Resolution | Purpose |
|---------|--------|------------|---------|
| **Chandrayaan-2 DFSAR** (full-pol) | ISRO PDS (PRADAN/Bhuvan) | ~2 m slant-range | Compute σ⁰, CPR, DOP |
| **Chandrayaan-2 OHRC** | ISRO PDS / Kaggle | 0.25 m GSD | Boulder/shadow mapping |
| **LOLA DEM** (global) | NASA/USGS | 118 m | Slope, terrain context |
| **LOLA DEM** (polar, targeted) | NASA PGDA | 5 m | Detailed topography |
| **LROC/WAC Illumination Map** | ASU/LROC | – | Solar power analysis |
| **LROC NAC Images** | NASA PDS | ~0.5 m | Rock detection (optional) |
| **KPLO ShadowCam Mosaics** | ASU/NASA | – | Interpret radar-bright regions |

---

## ⚙️ Installation

### Prerequisites

- Python 3.9+
- GDAL libraries installed on your system
- (Optional) ISRO MIDAS software for DFSAR validation

### Setup

```bash
# Clone the repository
git clone https://github.com/mdkamranalam/lunaicenet
cd LunaIceNet

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
rasterio
GDAL
numpy
scipy
scikit-learn
xgboost
matplotlib
networkx
jupyter
```

---

## 🚀 Usage

### 1. Radar Data Processing

```python
import rasterio
import numpy as np
import scipy.ndimage as nd

# Load DFSAR full-pol channels
hh = rasterio.open('data/dfsar_L_HH.tif').read(1)
vv = rasterio.open('data/dfsar_L_VV.tif').read(1)
hv = rasterio.open('data/dfsar_L_HV.tif').read(1)

# Speckle filtering (Refined Lee recommended; median as fallback)
hh_filt = nd.median_filter(hh, size=3)
hv_filt = nd.median_filter(hv, size=3)
vv_filt = nd.median_filter(vv, size=3)

# Compute CPR and DOP via Stokes parameters
sc = hh_filt + vv_filt
oc = 2 * hv_filt
cpr = sc / oc

I = hh_filt + vv_filt
Q = hh_filt - vv_filt
U = 2 * hv_filt
dop = np.sqrt(Q**2 + U**2) / I
```

### 2. Ice Detection Criteria

```python
# Flag candidate ice pixels (CPR > 1.0 and DOP < 0.13)
ice_mask = (cpr > 1.0) & (dop < 0.13)
```

### 3. ML Classification

```python
from sklearn.ensemble import RandomForestClassifier

# Assemble feature matrix: [CPR, DOP, sigma0, slope, roughness, illumination]
X = np.column_stack([cpr.ravel(), dop.ravel(), sigma0.ravel(),
                     slope.ravel(), roughness.ravel(), illum.ravel()])

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
ice_prob = clf.predict_proba(X)[:, 1].reshape(cpr.shape)
```

### 4. Landing-Site Safety Scoring

```python
# Composite safety score
score = (0.5 * (1 - slope / 15.0)
       + 0.3 * illumination_pct
       + 0.2 * (1 - boulder_density / boulder_density.max()))
```

### 5. Rover Path Planning (A*)

```python
# Cost function per grid cell
distance = 1.0
slope_factor = (slope / 15.0) ** 2
illum_penalty = 1 - illum_fraction
cost_cell = distance + 10 * slope_factor + 5 * illum_penalty

# Run A* on cost grid (using networkx or custom implementation)
```

### 6. Ice Volume Estimation

```python
# Parameters
pixel_area = 2.0 * 2.0       # m² (2m DFSAR resolution)
ice_area = ice_mask.sum() * pixel_area  # total ice-suspect area
depth = 5.0                   # meters (S-band penetration depth)
f_low, f_mid, f_high = 0.1, 0.3, 0.5  # ice volume fraction range

# Volume estimates
V_mid = ice_area * depth * f_mid
V_low = ice_area * depth * f_low
V_high = ice_area * depth * f_high
print(f"Ice Volume Estimate: {V_mid:.2e} m³ (range: {V_low:.2e} – {V_high:.2e} m³)")
```

---

## 📦 Deliverables

| Deliverable | Description |
|-------------|-------------|
| **CPR/DOP GeoTIFF** | Calibrated CPR and DOP maps over crater interior |
| **Ice-Probability Map** | Per-pixel ML-based probability of ice presence (0–1) |
| **Landing-Site Score Map** | Composite safety map highlighting optimal landing zones |
| **Rover Path Overlay** | Optimal traverse from lander to ice target on hazard map |
| **Ice Volume Estimate** | Numeric volume + uncertainty bounds table/chart |
| **Code Repository & Notebooks** | Full pipeline scripts and Jupyter notebooks |
| **Final Report/Presentation** | Summary slides, charts, and documentation |

---

## 👥 Team & Timeline

### Role Assignments

| Role | Responsibilities |
|------|-----------------|
| **Member 1** — Radar Specialist | Data acquisition, preprocessing, calibration, CPR/DOP computation, ice volume calculation |
| **Member 2** — Terrain Analyst | DEM/slope analysis, illumination mapping, boulder detection, landing-site scoring |
| **Member 3** — ML Engineer | Feature engineering, classifier training (RF/XGB), ice-probability map, path planning |
| **Member 4** — Integration Lead | Visualization, dashboard/notebook assembly, final integration & QA |

### 30-Hour Hackathon Schedule

| Hour | Phase | Task |
|------|-------|------|
| 0–1 | 🟦 Setup | Team kickoff, role assignment, environment setup |
| 1–3 | 🟦 Data | Download DFSAR, OHRC, DEM datasets |
| 3–5 | 🟩 SAR | Calibrate SAR (σ⁰), speckle filtering, compute CPR/DOP |
| 5–6 | 🟩 SAR | Identify high-CPR regions (initial mask) |
| 6–8 | 🟨 Terrain | Compute slope/roughness, detect boulders, score landing sites |
| 9–11 | 🟪 ML | Assemble features, train/test classifier, produce ice-probability map |
| 12–13 | 🟫 Path | Define cost function, run A*/D* pathfinding |
| 14–16 | 🟧 Output | Calculate ice volume, generate visualizations, build dashboard |
| 20–25 | 🔵 Review | Integrate results, QA, prepare report & slides |
| 25–28 | 🔵 Review | Dry run presentation, final fixes |
| 28–30 | 🔵 Delivery | Submit solution package |

---

## 📚 References

1. **Tarun et al., 2022** — *A software tool (MIDAS) for processing Chandrayaan-2 DFSAR* — Polarimetric processing and CPR computation methodology
2. **Sinha et al., 2026** — *Subsurface ice in doubly shadowed craters* (Nature npj Space) — CPR/DOP analysis in lunar PSRs with refined DOP < 0.13 threshold
3. **ISRO Chandrayaan-2 Factsheet** — DFSAR (L/S bands, 2–75 m SAR) and OHRC (0.25 m GSD) specifications
4. **LRO-LOLA DEM Documentation** — Lunar global DEM (118 m) and high-resolution polar DEMs
5. **LROC Polar Illumination Maps** — Time-weighted sunlight maps for PSR identification
6. **UCLA Diviner/ShadowCam Studies** — Faustini crater PSR characteristics (rock vs. ice discrimination)
7. **MIDAS Software (SAC/ISRO)** — Refined Lee filter and CPR routines for DFSAR
8. **NASA ShadowCam** — Shackleton crater imagery for hazard detection validation

---

## 📄 License

This project is developed as part of a hackathon challenge. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <i>Built with 🔭 for lunar exploration — LunaIceNet Team</i>
</p>

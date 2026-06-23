# Implementation Plan

## 1. Project Goal
Develop an end-to-end mission planning system capable of detecting lunar subsurface ice, evaluating landing safety, and planning rover traverses, culminating in an interactive Streamlit dashboard.

## 2. Phase Breakdown (30-Hour Hackathon Schedule)

### Phase 1: Ingestion & Infrastructure (Hours 0-4)
- **Objective**: Set up environment and preprocess datasets.
- **Tasks**:
  - Initialize Git repo and Python `venv`.
  - Download Chandrayaan-2 DFSAR, OHRC, and LOLA DEM sample data.
  - Write ingestion scripts using `rasterio` to read and co-register data to Lunar Polar Stereographic projection.
- **Deliverable**: A unified data matrix ready for processing.

### Phase 2: Radar Processing Engine (Hours 4-10)
- **Objective**: Extract polarimetric signatures from raw data.
- **Tasks**:
  - Calibrate DFSAR data to $\sigma^0$.
  - Implement and apply the Refined Lee speckle filter (`scipy.ndimage`).
  - Calculate Stokes parameters ($I, Q, U, V$).
  - Generate Circular Polarization Ratio (CPR) and Degree of Polarization (DOP) maps.
- **Deliverable**: Clean GeoTIFFs of CPR and DOP parameters.

### Phase 3: Terrain Analysis & Feature Engineering (Hours 10-15)
- **Objective**: Build the contextual terrain layers to eliminate false positives.
- **Tasks**:
  - Derive Slope and Roughness maps from the LOLA DEM.
  - Mask out regions with illumination $> 0\%$ to isolate PSRs.
  - Stack features into a 6D matrix: `[CPR, DOP, Sigma0, Slope, Roughness, Illumination]`.
- **Deliverable**: A fully assembled feature space matrix.

### Phase 4: Machine Learning Classification (Hours 15-20)
- **Objective**: Train and deploy the ice probability model.
- **Tasks**:
  - Define proxy training labels (e.g., thermally stable flat crater floors vs. steep rocky rims).
  - Train Random Forest and XGBoost classifiers.
  - Extract feature importance (to prove scientific validity).
  - Generate the final Ice Probability Map (continuous values 0.0–1.0).
- **Deliverable**: Model weights and the Ice Probability GeoTIFF.

### Phase 5: Mission Planning Modules (Hours 20-25)
- **Objective**: Translate science into actionable mission data.
- **Tasks**:
  - Develop the Composite Safety Scorer for landing sites.
  - Implement the A* pathfinding algorithm using `NetworkX` on the cost-grid to route the rover.
  - Write the volume estimation script factoring in depth and uncertainty limits.
- **Deliverable**: Landing coordinates, Rover path array, and Volume estimates.

### Phase 6: UI Dashboard & Presentation (Hours 25-30)
- **Objective**: Wrap the pipeline in a user-friendly interface.
- **Tasks**:
  - Build the Streamlit dashboard (`app.py`) integrating all maps and findings.
  - Finalize documentation (`RESEARCH.md`, `SYSTEM_ARCHITECTURE.md`, etc.).
  - Assemble the slide deck and rehearse the 5-minute pitch.
- **Deliverable**: Deployed Streamlit app and finalized presentation.

## 3. Team Responsibilities

| Role | Key Tasks |
|------|-----------|
| **Radar/Remote Sensing Specialist** | DFSAR calibration, Stokes params, CPR/DOP, Volume Estimation. |
| **Data Scientist (ML)** | Feature engineering, proxy labeling, RF/XGBoost training, Evaluation metrics. |
| **Geospatial/Mission Engineer** | DEM analysis (Slope/Roughness), A* Pathfinding, Safety scoring. |
| **Full Stack / UI Lead** | Streamlit dashboard development, map visualization (`folium`), Documentation. |

## 4. Risk Mitigation

- **Risk**: Difficulty aligning disparate datasets (DFSAR vs DEM).
  - **Mitigation**: Use GDAL/Rasterio to force all outputs to a master projection grid early in Phase 1.
- **Risk**: ML model overfits or predicts ice on steep walls.
  - **Mitigation**: Implement strict physical sanity checks; heavily penalize slopes $> 20^\circ$ in the final probability output regardless of CPR.
- **Risk**: Dashboard crashes during demo due to large raster sizes.
  - **Mitigation**: Downsample rasters dynamically within Streamlit or pre-calculate low-res viewing tiers.
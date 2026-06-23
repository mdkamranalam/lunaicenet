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

- [Documentation Hub](#-documentation-hub)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start / Usage](#-quick-start--usage)
- [Deliverables](#-deliverables)
- [License](#-license)

---

## 📚 Documentation Hub

We have separated our comprehensive project details into dedicated markdown files for better readability. Please refer to the `docs/` directory:

| Document | Description |
|----------|-------------|
| 🔬 **[Scientific Research](docs/RESEARCH.md)** | Physics of radar scattering, CPR/DOP, and overcoming the false-positive challenge. |
| 📡 **[Datasets](docs/DATASETS.md)** | Specs for Chandrayaan-2 DFSAR, OHRC, LOLA DEMs, and illumination maps. |
| 🏗️ **[System Architecture](docs/SYSTEM_ARCHITECTURE.md)** | Modular diagrams mapping data ingestion to the interactive dashboard. |
| 🧮 **[Algorithms](docs/ALGORITHMS.md)** | Math behind the Refined Lee filter, Stokes parameters, ML, and A* pathfinding. |
| 📊 **[Evaluation Strategy](docs/EVALUATION.md)** | Metrics, sanity checks, and volume uncertainty analysis. |
| 🛠️ **[Tech Stack](docs/TECH_STACK.md)** | In-depth look at our Python-centric geospatial and machine learning stack. |
| ⏱️ **[Implementation Plan](docs/IMPLEMENTATION_PLAN.md)** | Phase-by-phase execution strategy and task breakdown. |
| 🎤 **[Presentation Plan](docs/PRESENTATION_PLAN.md)** | Pitch outline, slide breakdown, and demo strategy. |

---

## ✨ Key Features

- **🛰️ Polarimetric Radar Processing**: Full-pipeline DFSAR calibration, Refined Lee speckle filtering, and calculation of CPR & DOP invariants.
- **🤖 ML-Based Ice Classification**: Random Forest/XGBoost classification fusing radar signatures with terrain context (slope, roughness) to drastically reduce rocky false-positives.
- **🗺️ Ice-Probability Mapping**: Continuous probability mapping (0–1) over targeted PSRs.
- **🏔️ Terrain Intelligence**: Automated landing site safety scoring using slope, illumination, and boulder hazard data.
- **🛤️ Rover Path Planning**: A* pathfinding across a customized cost-grid from landing site to the subsurface ice deposit.
- **📊 Volumetric Estimations**: Quantitative ice volume calculations with strict confidence bounds.
- **🖥️ Mission Dashboard**: Interactive Streamlit interface to visualize all layers and engineering paths.

---

## ⚙️ Installation

### Prerequisites
- Python 3.9+
- System-level GDAL libraries
- (Optional) ISRO MIDAS software for independent DFSAR validation

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

---

## 🚀 Quick Start / Usage

The pipeline is fully accessible via our interactive Streamlit dashboard or through modular Python scripts.

**To launch the Mission Dashboard:**
```bash
streamlit run dashboard/app.py
```

**To run individual processing stages programmatically:**
```python
# Example: Running the Radar Processing Engine
from src.radar import polarimetry

# Compute Stokes parameters and invariants
cpr_map, dop_map = polarimetry.process_dfsar('data/dfsar_stack.tif', filter='refined_lee')
```

*(See [ALGORITHMS.md](docs/ALGORITHMS.md) for deeper programmatic details).*

---

## 📦 Deliverables

1. **Processed GeoTIFFs**: Calibrated CPR and DOP maps.
2. **Ice-Probability Map**: The final ML-driven predictive layer.
3. **Mission Overlays**: Landing-site hazard maps and optimized rover traverse lines.
4. **Volume Report**: Quantitative ice volume estimates.
5. **Source Code**: Full reproducible pipeline and dashboard.

---

## 📄 License

This project is developed as part of the ISRO Bharatiya Antariksh Hackathon 2026. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <i>Built with 🔭 for lunar exploration — LunaIceNet Team</i>
</p>

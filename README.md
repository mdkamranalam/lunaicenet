<p align="center">
  <img src="https://img.shields.io/badge/Mission-Chandrayaan--2-blue?style=for-the-badge" alt="Mission Badge"/>
  <img src="https://img.shields.io/badge/Hackathon-ISRO%20Bharatiya%20Antariksh%20Hackathon%202026-orange?style=for-the-badge" alt="Hackathon Badge"/>
  <img src="https://img.shields.io/badge/Python-3.9%2B-green?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License Badge"/>
</p>

# 🌙 LunaIceNet

> Prototype geospatial analysis pipeline for lunar south-pole landing assessment and subsurface-ice evidence mapping.

LunaIceNet is a Python-based research and demo project for evaluating candidate landing regions near the Moon's south pole. The repository combines terrain analysis, radar-derived confidence layers, landing-site scoring, and a Streamlit dashboard to support rapid exploration of mission-relevant factors such as terrain hazard, safe-zone suitability, and ice-confidence signals.

## What this repository contains

The current codebase is a working prototype built around precomputed mission data in the [data](data) folder. It includes:

- terrain processing modules for slope, roughness, hazard, and safe-zone analysis
- radar product ingestion for CPR and DOP-based ice confidence mapping
- landing-site candidate generation and final ranking logic
- an interactive dashboard for visualizing hazard maps and ranked sites

This is best understood as a hackathon-style geospatial analysis workflow rather than a fully productionized mission-planning system.

---

## Project structure

- [dashboard/app.py](dashboard/app.py) — Streamlit application for visualizing hazard maps, ranked sites, and mission assessment views
- [src/terrain](src/terrain) — terrain metrics and hazard/safe-zone generation scripts
- [src/radar](src/radar) — radar product readers and visualization helpers
- [src/ice_detection](src/ice_detection) — ice-confidence map generation based on radar indicators
- [src/landing](src/landing) — candidate-site detection and final mission ranking
- [data](data) — sample data products, derived arrays, and CSV reports
- [docs](docs) — scientific and engineering documentation

---

## Core workflow

The pipeline currently follows this flow:

1. Compute terrain descriptors from the DEM
   - slope
   - roughness
   - hazard score
   - safe-zone mask
2. Load radar products and derive confidence-based ice indicators from CPR and DOP data
3. Generate landing-site candidates from the suitability surface
4. Rank sites using hazard, safe-zone, and ice-confidence factors
5. Visualize the results through the Streamlit dashboard

---

## Installation

### Prerequisites

- Python 3.9+
- pip
- Optional: GDAL-related system libraries depending on your environment

### Setup

```bash
git clone https://github.com/mdkamranalam/lunaicenet
cd lunaicenet

python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the project

### Launch the dashboard

From the repository root:

```bash
streamlit run dashboard/app.py
```

### Rebuild analysis products

The repository includes standalone scripts for each processing stage. These can be run from the repository root:

```bash
python src/terrain/slope.py
python src/terrain/roughness.py
python src/terrain/hazards.py
python src/terrain/safe_zones.py
python src/ice_detection/ice_confidence.py
python src/landing/candidate_sites.py
python src/landing/final_ranking.py
```

These scripts read from the data directory and write generated arrays and reports back to the same location.

---

## Documentation

Additional project documentation is available in the [docs](docs) directory:

- [docs/RESEARCH.md](docs/RESEARCH.md) — background and scientific motivation
- [docs/DATASETS.md](docs/DATASETS.md) — data sources and product descriptions
- [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md) — module and pipeline architecture
- [docs/ALGORITHMS.md](docs/ALGORITHMS.md) — algorithmic and geospatial processing notes
- [docs/EVALUATION.md](docs/EVALUATION.md) — evaluation approach and checks
- [docs/TECH_STACK.md](docs/TECH_STACK.md) — technology choices and dependencies
- [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) — project plan and milestone structure

---

## License

This project is developed as part of the ISRO Bharatiya Antariksh Hackathon 2026. See [LICENSE](LICENSE) for details.

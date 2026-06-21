# TECH_STACK.md

# PS-8: Lunar Subsurface Ice Detection & Mission Planning System

## Overview

This project aims to identify and characterize potential subsurface ice deposits in Lunar South Polar Doubly Shadowed Craters using Chandrayaan-2 DFSAR radar data, OHRC imagery, and terrain information.

The system is designed as a complete lunar mission-planning platform rather than a simple ice detection tool.

Core capabilities:

* Radar-based ice detection
* Terrain intelligence
* Landing site recommendation
* Rover traverse planning
* Ice volume estimation
* Interactive mission dashboard

---

# Technology Philosophy

The project follows three principles:

### 1. Scientific First

The primary objective is scientific analysis.

All technology choices should improve:

* Ice detection quality
* Terrain analysis
* Mission planning

---

### 2. Python-Centric Workflow

The problem statement recommends a Python-based workflow.

Keeping the entire project inside Python reduces complexity and development time.

---

### 3. Explainability

The solution must be explainable to judges.

Every output should be traceable back to:

* Radar observations
* Terrain characteristics
* Engineering constraints

---

# Final Technology Stack

| Category              | Technology     |
| --------------------- | -------------- |
| Programming Language  | Python         |
| Scientific Computing  | NumPy, SciPy   |
| Geospatial Processing | GDAL, Rasterio |
| GIS Platform          | QGIS           |
| Remote Sensing Tools  | MIDAS, ENVI    |
| Terrain Analysis      | DEM Tools      |
| Path Planning         | A* Algorithm   |
| Visualization         | Matplotlib     |
| Dashboard             | Streamlit      |

---

# System Architecture

```text id="lyexgm"
                 Streamlit Dashboard
                          │
                          ▼
                Mission Analysis Engine
                          │
 ┌─────────────────────────────────────────┐
 │ Radar Processing                        │
 │ Ice Detection                           │
 │ Terrain Analysis                        │
 │ Landing Site Selection                  │
 │ Rover Traverse Planning                 │
 │ Ice Volume Estimation                   │
 └─────────────────────────────────────────┘
                          │
                          ▼
                    GIS Outputs
```

---

# 1. Python

## What is Python?

Python is the primary programming language used throughout the project.

---

## Why Are We Using Python?

Python is the industry standard for:

* Remote sensing
* Geospatial computing
* Scientific research
* Planetary science

Most lunar and Earth observation workflows are already Python-based.

---

## Responsibilities

Python controls:

```text id="hnz5n7"
Data Loading

Radar Processing

CPR Computation

DOP Computation

Terrain Analysis

Landing Site Selection

Path Planning

Volume Estimation

Dashboard Integration
```

---

## Installation

```bash id="brf6gs"
python -m venv venv

source venv/bin/activate
```

Windows:

```bash id="8jkxtf"
venv\Scripts\activate
```

---

# 2. NumPy

## What is NumPy?

NumPy provides efficient numerical computing.

Satellite images are processed as large matrices.

---

## Why Are We Using NumPy?

Radar and terrain data are fundamentally arrays.

NumPy enables:

```text id="ikjic7"
Pixel Operations

CPR Calculation

DOP Calculation

Statistical Analysis
```

---

## Example Usage

```text id="x6igsh"
Radar Matrix
      ↓
Numerical Operations
      ↓
Radar Products
```

---

# 3. SciPy

## What is SciPy?

SciPy extends NumPy with scientific algorithms.

---

## Why Are We Using SciPy?

Needed for:

```text id="6yl71f"
Filtering

Interpolation

Optimization

Signal Processing
```

---

## Usage

### Speckle Reduction

Radar images contain speckle noise.

SciPy helps reduce it.

---

### Optimization

Used during rover path planning.

---

# 4. GDAL

## What is GDAL?

GDAL stands for:

```text id="z0g50l"
Geospatial Data Abstraction Library
```

It is the foundation of most GIS systems.

---

## Why Are We Using GDAL?

DFSAR, OHRC, and DEM datasets are geospatial rasters.

GDAL allows:

```text id="tq1h6d"
Reading

Writing

Transforming

Reprojecting
```

these datasets.

---

## Usage

### Data Conversion

Different sources may use different coordinate systems.

GDAL standardizes them.

---

# 5. Rasterio

## What is Rasterio?

Rasterio is a Python interface built on top of GDAL.

---

## Why Are We Using Rasterio?

Rasterio makes raster processing significantly easier.

---

## Usage

### Loading Data

```text id="onp5y2"
DFSAR

OHRC

DEM
```

### Exporting Results

```text id="sfxhzy"
CPR Maps

DOP Maps

Ice Maps
```

---

# 6. MIDAS

## What is MIDAS?

Microwave Data Analysis Software.

A specialized radar processing environment.

---

## Why Are We Using MIDAS?

The challenge specifically references DFSAR radar products.

MIDAS supports:

```text id="g08is4"
SAR Processing

Polarimetric Analysis

Radar Feature Extraction
```

---

## Usage

### Radar Processing

Generate:

```text id="9z8vzx"
CPR

DOP

Backscatter Products
```

---

## Note

If the supplied dataset already contains processed products, MIDAS may only be used for validation.

---

# 7. ENVI

## What is ENVI?

A professional remote sensing platform.

---

## Why Are We Using ENVI?

Useful for:

```text id="uk67xb"
Image Enhancement

Feature Interpretation

Visual Validation
```

---

## Usage

Primarily used for:

* OHRC imagery inspection
* Feature verification

---

## Note

The project should remain functional even if ENVI is unavailable.

---

# 8. QGIS

## What is QGIS?

Open-source Geographic Information System.

---

## Why Are We Using QGIS?

QGIS is ideal for:

```text id="r01u8g"
Spatial Analysis

Map Validation

Visualization
```

---

## Usage

### Terrain Analysis

Generate:

```text id="utx95q"
Slope Maps

Elevation Maps

Hillshade Maps
```

---

### Final Presentation

Display:

```text id="afom5q"
Ice Regions

Landing Sites

Rover Routes
```

---

# 9. DEM Tools

## What is a DEM?

DEM stands for:

```text id="6lsvry"
Digital Elevation Model
```

It represents terrain elevation.

---

## Why Are We Using DEMs?

Terrain affects:

```text id="5cltib"
Landing Safety

Rover Mobility

Mission Risk
```

---

## Derived Products

Generate:

```text id="wz2suv"
Slope

Roughness

Elevation

Hazard Zones
```

---

# 10. A* Path Planning

## What is A*?

A graph-search algorithm.

Widely used in:

* Robotics
* Navigation
* Autonomous systems

---

## Why Are We Using A*?

The problem requires:

```text id="lvnz7m"
Landing Site
      ↓
Ice Deposit
```

navigation.

---

## Usage

Input:

```text id="esl2jn"
Slope

Hazards

Distance
```

Output:

```text id="8s0i8j"
Optimal Rover Route
```

---

# 11. Matplotlib

## What is Matplotlib?

Scientific plotting library.

---

## Why Are We Using It?

Generate:

```text id="3s37y7"
CPR Maps

DOP Maps

Slope Maps

Statistics
```

---

## Usage

Used both for:

* Development
* Dashboard visualizations

---

# 12. Streamlit

## What is Streamlit?

Streamlit is a Python framework for building interactive scientific applications.

---

## Why Are We Using Streamlit?

This project is a scientific computing application rather than a traditional web application.

Streamlit allows us to:

* Stay entirely in Python
* Build dashboards rapidly
* Focus on science rather than frontend engineering

---

## Responsibilities

### Data Exploration

Display:

```text id="c7g4si"
Dataset Metadata

Input Layers
```

---

### Radar Analysis

Display:

```text id="m0h8lk"
CPR Maps

DOP Maps
```

---

### Ice Detection

Display:

```text id="c85h1n"
Ice Confidence Maps

Candidate Regions
```

---

### Terrain Analysis

Display:

```text id="d3l8vk"
Slope

Hazards

Roughness
```

---

### Landing Site Selection

Display:

```text id="o8q6wn"
Ranked Landing Sites
```

---

### Rover Planning

Display:

```text id="h5z7g7"
Optimal Traverse Route
```

---

### Resource Estimation

Display:

```text id="r49ewz"
Estimated Ice Volume
```

---

## Installation

```bash id="ajz0pf"
pip install streamlit
```

---

## Run

```bash id="2vg1hj"
streamlit run dashboard/app.py
```

---

# Complete Technology Flow

```text id="jgx8ig"
DFSAR
OHRC
DEM
      │
      ▼
MIDAS / Rasterio
      │
      ▼
CPR + DOP Generation
      │
      ▼
Ice Detection
      │
      ▼
Terrain Analysis
      │
      ▼
Landing Site Selection
      │
      ▼
Rover Traverse Planning
      │
      ▼
Ice Volume Estimation
      │
      ▼
Streamlit Dashboard
      │
      ▼
Mission Planning Outputs
```

---

# Final Justification

This stack was selected because:

1. It aligns directly with the technologies suggested in the problem statement.
2. It minimizes unnecessary complexity.
3. It supports the entire mission-planning workflow.
4. It is achievable within a 30-hour hackathon.
5. It remains scientifically rigorous and explainable.
6. It allows the team to spend time on research and analysis rather than frontend development.

The final result is an AI-assisted Lunar Resource Intelligence and Mission Planning System built entirely around remote sensing, geospatial analysis, and mission planning principles.

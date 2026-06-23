# Technology Stack

## Overview

The LunaIceNet platform is built entirely on a **Python-centric scientific workflow**. This ensures seamless interoperability between heavy geospatial processing, machine learning models, and the final interactive user interface. We prioritize scientific rigor, computational efficiency, and explainability.

## 1. Core Language & Environment
- **Python 3.9+**: The industry standard for data science, remote sensing, and planetary geology. It provides the glue for all underlying C/C++ libraries.
- **Virtual Environments (`venv` / `conda`)**: Ensures dependency isolation and reproducibility across different operating systems.

## 2. Geospatial Processing & I/O
Handling satellite data formats (like PDS4 and complex GeoTIFFs) requires robust low-level tools.
- **GDAL (Geospatial Data Abstraction Library)**: The fundamental C++ library for reading, writing, and projecting raster and vector geospatial data formats.
- **Rasterio**: A more Pythonic wrapper around GDAL. Used for reading DFSAR bands and DEMs as NumPy arrays and writing the resulting CPR/DOP and Ice Probability maps back to disk with proper georeferencing.
- **PyProj**: Handles coordinate reference system (CRS) transformations (e.g., mapping pixels to Lunar Polar Stereographic projections).

## 3. Scientific & Numerical Computing
- **NumPy**: Powers all matrix operations. Used for calculating pixel-wise radar parameters (e.g., Stokes vectors, total power).
- **SciPy**: Utilized for image processing (e.g., implementing the Refined Lee speckle filter through `scipy.ndimage`) and optimization algorithms.

## 4. Machine Learning & Modeling
To overcome the false-positive challenges of radar-bright rocks, we employ supervised machine learning.
- **Scikit-Learn**: Used for data splitting, preprocessing (scaling features if necessary), and implementing the baseline **Random Forest Classifier**. Random Forest is chosen for its robustness to outliers and highly interpretable feature importance.
- **XGBoost**: Employed as an advanced, gradient-boosted alternative for higher classification accuracy on edge cases (e.g., distinguishing highly rugged but ice-free craters).

## 5. Mission Planning & Optimization
- **NetworkX**: Used to represent the lunar surface as a graph. It provides the infrastructure to run the **A* (A-Star) search algorithm** over our custom terrain-cost grid to find the optimal rover traverse path.
- **OpenCV (`cv2`)**: Used for computer vision tasks, specifically detecting and counting boulders in high-resolution OHRC imagery to define hazard zones.

## 6. Remote Sensing Analysis Tools
While our pipeline is automated in Python, we use established tools for validation.
- **MIDAS (Microwave Data Analysis Software)**: ISRO's proprietary software used to validate our Python-based DFSAR calibration and polarimetric decomposition.
- **QGIS**: Open-source GIS platform used for visual inspection of our output GeoTIFFs, confirming co-registration of DEMs and radar maps.

## 7. Visualization & UI
- **Matplotlib & Seaborn**: Generates static plots, histograms of radar backscatter, and feature importance charts for the presentation.
- **Streamlit**: The backbone of our Mission Dashboard. Streamlit allows us to rapidly build a web application using only Python, avoiding the need for complex frontend frameworks (React/Vue) while providing an interactive experience for mission scientists.
- **Folium / Leafmap**: Used within Streamlit to render interactive map overlays of the lunar surface, allowing users to zoom into specific craters and toggle between radar and ice-probability layers.

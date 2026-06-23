# Hackathon Presentation Plan

This document outlines the strategy for presenting LunaIceNet, strictly aligned with the required **ISRO BAH 2026 Idea Submission Template**.

## Presentation Structure (10 Slides)

### Slide 1: Cover Page
- **Team Name**: [Your Team Name]
- **Problem Statement**: PS-8: Subsurface Ice Detection in Doubly-Shadowed Lunar Craters
- **Team Leader Name**: [Leader Name]

### Slide 2: Team Members
- **Team Leader**: [Name, College]
- **Team Member-1**: [Name, College]
- **Team Member-2**: [Name, College]
- **Team Member-3**: [Name, College]

### Slide 3: Opportunity & USP
- **How is it different?** Most existing approaches rely purely on a single radar threshold (CPR > 1) which creates false positives. LunaIceNet fuses radar physics (CPR & DOP) with topographical context (Slope/Roughness) using an AI model.
- **How does it solve the problem?** It effectively eliminates false positives (e.g., radar-bright rocks on crater rims) and identifies stable subsurface ice inside thermally stable, doubly-shadowed regions.
- **Unique Selling Proposition (USP)**: We don't just output a raw radar map. We provide an end-to-end mission planning platform that includes safe landing site selection, rover path optimization, and volumetric resource estimates.

### Slide 4: Features Offered
*Note: Include visual representations/icons for each feature.*
- **Polarimetric Engine**: Refined Lee speckle filtering and CPR/DOP derivation from DFSAR data.
- **Terrain Intelligence**: Slope, roughness, and illumination extraction from LOLA DEMs.
- **ML Classifier**: High-confidence subsurface ice probability mapping.
- **Safe-Landing Scorer**: Optimization function finding hazard-free landing zones.
- **Rover Traverse Planner**: A* pathfinding to avoid steep slopes and deep shadows.
- **Dashboard Interface**: Interactive Streamlit application for mission scientists.

### Slide 5: Process Flow / Use-case Diagram
- **Content**: A high-level flowchart depicting the data and user journey.
- **Visual**: Data Ingestion (DFSAR/DEM) $\rightarrow$ Processing Engine $\rightarrow$ AI Classification $\rightarrow$ Landing Site & Path Routing $\rightarrow$ Dashboard Visualization.

### Slide 6: Wireframes / Mock Diagrams
- **Content**: Visuals of our proposed Streamlit dashboard interface.
- **Visual**: Screenshots or wireframes showing the toggleable map layers (Raw Radar, Ice Probability Map, Rover Path, Landing Sites) and volume estimation panels.

### Slide 7: Architecture Diagram
- **Content**: The technical system architecture.
- **Visual**: Embed the architectural diagram (from `SYSTEM_ARCHITECTURE.md`), showing the modular breakdown: Radar Engine, Terrain Engine, ML Engine, and Mission Planning Engine.

### Slide 8: Technologies Used
- **Core Languages**: Python 3.9+
- **Geospatial Processing**: GDAL, Rasterio, PyProj
- **Scientific Computing**: NumPy, SciPy
- **Machine Learning**: Scikit-Learn (Random Forest), XGBoost
- **Pathfinding & AI**: NetworkX (A* Algorithm), OpenCV
- **Frontend / UI**: Streamlit, Matplotlib, Folium

### Slide 9: Estimated Implementation Cost
- **Content**: Software licensing costs are $0 since the entire stack relies on robust open-source tools.
- **Computing Cost**: Minimal processing overhead. The system can be deployed on standard cloud instances (e.g., AWS EC2/GCP) for negligible cost, enabling scalable lunar resource mapping.

### Slide 10: Conclusion / Q&A
- **Content**: Summary statement, link to the open-source GitHub repository, team contact info, and an invitation for questions from the judging panel.

---

## Live Demo Strategy (If Applicable)
If a live demo is permitted alongside the PPT:
1. Open the Streamlit dashboard when presenting **Slide 6**.
2. Select a target crater (e.g., Faustini or Shackleton).
3. Toggle between the "Raw CPR" view and the "ML Ice Confidence" view to practically demonstrate the USP (the AI removing rocky crater rims from the target list).
4. Click "Calculate Route" to demonstrate the A* algorithm generating a safe path from a flat landing zone in real-time.

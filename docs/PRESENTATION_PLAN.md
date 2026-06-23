# Hackathon Presentation Plan

This document outlines the strategy for presenting LunaIceNet to the hackathon judges. The presentation is designed for a strict 5-to-7 minute pitch window.

## Core Pitch Narrative
**Hook**: Most teams are using radar data to find "bright spots" (high CPR) and calling it ice. We know from scientific literature that rocks also look bright to radar. 
**Solution**: LunaIceNet goes beyond basic radar processing. We built an AI pipeline that fuses radar with terrain data to eliminate false positives, and wrapped it in a full mission-planning dashboard that tells you exactly where to land and how to drive the rover there.

---

## Slide Deck Breakdown (8 Slides)

### Slide 1: Title & Vision
- **Title**: LunaIceNet: AI-Driven Subsurface Ice Detection & Mission Planning
- **Sub-title**: ISRO Bharatiya Antariksh Hackathon 2026 - Problem Statement 8
- **Visual**: A striking rendering of a lunar crater in shadow.

### Slide 2: The Problem (False Positives)
- **Concept**: Finding ice isn't as simple as finding radar-bright spots.
- **Visual**: Side-by-side comparison of a high-CPR region inside a PSR vs. a high-CPR region on a rocky crater wall.
- **Talking Point**: "CPR > 1 is not enough. Rocks trick the radar."

### Slide 3: The LunaIceNet Solution
- **Concept**: Multi-modal data fusion.
- **Visual**: High-level Architecture Diagram (from `SYSTEM_ARCHITECTURE.md`).
- **Talking Point**: We use Chandrayaan-2 DFSAR for penetration, combined with LOLA DEMs and ML to distinguish volumetric ice scattering (low DOP) from surface rock scattering.

### Slide 4: Scientific Processing (The Radar)
- **Concept**: Show our technical rigor.
- **Visual**: Raw DFSAR $\rightarrow$ Refined Lee Speckle Filter $\rightarrow$ CPR & DOP Maps.
- **Talking Point**: Highlight the use of Stokes parameters and the critical DOP $< 0.13$ threshold.

### Slide 5: The AI Engine
- **Concept**: How we eliminate the false positives.
- **Visual**: Feature importance chart from our Random Forest model showing Slope and DOP alongside CPR.
- **Talking Point**: The ML model learns the geomorphological context.

### Slide 6: Mission Planning (Landing & Traverse)
- **Concept**: Translating science into engineering.
- **Visual**: Heatmap of safe landing zones, and an A* path overlay avoiding steep slopes.
- **Talking Point**: We don't just find the ice; we provide the safe landing coordinates and the rover path.

### Slide 7: Live Demo / Dashboard Screenshots
- **Concept**: Show the Streamlit app.
- **Visual**: 2-3 clean screenshots or a very brief recorded GIF of the dashboard.
- **Talking Point**: Interactive tool for mission scientists to adjust parameters and visualize resources.

### Slide 8: Future Scope & Team
- **Concept**: Scalability.
- **Talking Point**: Ready for integration with future LUPEX mission data.

---

## Live Demo Strategy
If a live demo is permitted:
1. Open the Streamlit dashboard.
2. Select a target crater (e.g., Faustini or Shackleton).
3. Toggle between the "Raw CPR" view and the "ML Ice Confidence" view to show how the AI removes the rocky crater rims from the potential targets.
4. Click "Calculate Route" to show the A* algorithm generating a safe path from a flat landing zone.

## Anticipated Q&A
- **Q**: How did you handle the lack of ground-truth data for training the ML model?
  - **A**: We used proxy labels. Thermally stable doubly-shadowed crater floors with high CPR were labeled as likely ice, while known rocky slopes outside PSRs were labeled as false positives.
- **Q**: Why Refined Lee over a standard median filter?
  - **A**: Standard filters blur the crater rims. Refined Lee uses local variance to preserve structural edges while smoothing the noise, which is critical for accurate slope and feature extraction.
- **Q**: What depth does your volume estimate assume?
  - **A**: We assume up to ~5 meters, based on the penetration depth of S-band and L-band radar in dry lunar regolith.

# Evaluation Metrics & Validation Strategy

Evaluating a lunar ice detection system is challenging due to the lack of extensive in-situ ground truth. However, LunaIceNet employs a robust set of proxy metrics, cross-validation techniques, and physical sanity checks to ensure scientific validity and algorithmic reliability.

## 1. Machine Learning Evaluation

### Dataset Construction for Training/Testing
Since we cannot easily get labeled "ice" or "rock" pixels, we construct our training set using proxy labels based on geomorphology and thermal data:
- **Positive Labels (Probable Ice)**: Pixels deep inside thermally stable, doubly-shadowed craters that have CPR > 1.0.
- **Negative Labels (Rocks/False Positives)**: Pixels on steep, young crater rims (e.g., Shackleton rim) or known ejecta blankets that exhibit CPR > 1.0 but are too warm to support ice.

### Classification Metrics
The ML classifier is evaluated using standard metrics on a hold-out test set:
- **Precision**: How many of the predicted ice pixels are actually in thermally stable zones? (Crucial to minimize false positives and prevent sending a rover to a dry rock field).
- **Recall**: How much of the true thermally stable, high-CPR area did we successfully identify?
- **F1-Score**: Harmonic mean of Precision and Recall.
- **ROC-AUC**: Evaluates the model's ability to rank probabilities correctly.

## 2. Scientific Sanity Checks (Physical Validation)

Machine learning models can overfit. We validate the physical realism of our outputs:
- **The DOP Threshold Test**: Does the ML model implicitly learn the $\text{DOP} < 0.13$ rule discovered in recent Chandrayaan-2 literature? We verify this by analyzing the partial dependence plots of the Random Forest model.
- **Topographical Correlation**: The resulting ice probability map must inversely correlate with slope. Ice cannot remain stable on slopes $> 20^\circ$ due to mass wasting. If the model predicts ice on a cliff, the model fails the physical sanity check.

## 3. Mission Planning Evaluation

### Landing Site Safety
- Evaluated by the **Composite Safety Score**. A site is considered "Valid" if:
  - Max slope within landing ellipse $< 10^\circ$.
  - Illumination coverage $> 50\%$ of the lunar cycle (for solar power).
  - Distance to target $< 5$ km (rover traverse limit).

### A* Pathfinding Efficiency
- **Path Optimality**: Compared against a straight-line Euclidean path.
- **Hazard Avoidance Rate**: The algorithm must strictly route around any cell with a slope $> 15^\circ$ or known boulder clusters. The evaluation metric is the count of "hazardous cells traversed" (must be 0).
- **Energy Cost Proxy**: The integral of elevation change along the path, which serves as a proxy for rover battery consumption.

## 4. Volume Estimation Uncertainty

Volume estimates are provided with strict confidence intervals.
- **Sensitivity Analysis**: We evaluate how the total volume $V$ changes when varying the penetration depth parameter $D_p$ (between 2m and 5m) and the ice fraction $f$ (between 5% and 30%).
- **Reporting**: The final volume is never reported as a single number, but always as a bracketed range (e.g., $1.2 \times 10^6 \text{ m}^3$ to $3.5 \times 10^6 \text{ m}^3$) to reflect current scientific uncertainties.

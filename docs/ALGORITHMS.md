# Core Algorithms

This document describes the key mathematical and computational algorithms utilized within the LunaIceNet pipeline.

## 1. Radar Processing Algorithms

### Speckle Filtering: Refined Lee Filter
SAR images suffer from inherent "speckle" noise due to constructive and destructive interference of the coherent radar waves. Standard mean or median filters blur edges. The Refined Lee Filter is used because it preserves edges and structural features (like crater rims and boulders) while smoothing homogeneous regions.
- **Algorithm**: It uses local statistics (variance and mean) within a moving window. If the local variance is high (indicating an edge), the filter performs less smoothing. If the variance is low (homogeneous area), it smooths heavily.

### Polarimetric Invariants (Stokes Parameters)
From the four scattering matrix elements ($S_{HH}, S_{HV}, S_{VH}, S_{VV}$), assuming reciprocity ($S_{HV} \approx S_{VH}$), we compute the Stokes vector elements ($I, Q, U, V$):
1. **$I = |S_{HH}|^2 + |S_{VV}|^2$** (Total power)
2. **$Q = |S_{HH}|^2 - |S_{VV}|^2$** (Linear polarization difference)
3. **$U = 2 \cdot \text{Re}(S_{HH} \cdot S_{VV}^*)$** 
4. **$V = 2 \cdot \text{Im}(S_{HH} \cdot S_{VV}^*)$**

**Circular Polarization Ratio (CPR)**:
$$ \text{CPR} = \frac{\text{Same-Sense Power (SC)}}{\text{Opposite-Sense Power (OC)}} = \frac{I - V}{I + V} $$

**Degree of Polarization (DOP)**:
$$ \text{DOP} = \frac{\sqrt{Q^2 + U^2 + V^2}}{I} $$

## 2. Machine Learning: Random Forest / XGBoost

To handle the "false positive" problem of ice detection (where rocks mimic ice radar signatures), we frame the problem as a supervised classification task.
- **Features**: Vector $\mathbf{X} = [\text{CPR}, \text{DOP}, \sigma^0, \text{Slope}, \text{Roughness}, \text{Illumination}]$
- **Algorithm Choice**: Tree-based ensembles (Random Forest or XGBoost) are chosen because:
  - They handle non-linear relationships well without requiring extensive feature scaling.
  - They provide **feature importance**, which is crucial for scientific explainability (e.g., proving that the model actually uses DOP and Slope, not just CPR).
  - They output class probabilities (predict_proba), allowing us to generate a continuous Ice Confidence Map rather than a binary output.

## 3. Mission Planning: A* Pathfinding

Finding a safe rover path from the lander to the ice deposit requires solving a pathfinding problem on a weighted grid.
- **Algorithm**: A* (A-Star) search algorithm.
- **Cost Function (Heuristic)**: The cost $C_{i,j}$ to move into a cell $(i,j)$ is a weighted sum of distance and hazards:
  $$ C_{i,j} = w_d \cdot D + w_s \cdot (\text{Slope}_{i,j})^2 + w_h \cdot H_{i,j} + w_{ill} \cdot (1 - \text{Illum}_{i,j}) $$
  Where:
  - $D$ is the physical distance.
  - $\text{Slope}_{i,j}$ represents terrain steepness (squared to heavily penalize very steep slopes).
  - $H_{i,j}$ is hazard density (boulders).
  - $\text{Illum}_{i,j}$ encourages paths that stay in sunlight to preserve rover battery.

## 4. Resource Estimation: Volumetric Model

Ice volume estimation provides upper and lower bounds for mission feasibility.
- **Formula**:
  $$ V = \sum_{pixels} (A \cdot D_p \cdot P_{ice} \cdot f) $$
  Where:
  - $A$: Area of a single pixel.
  - $D_p$: Penetration depth of the radar (e.g., ~5m for S-band).
  - $P_{ice}$: The probability of ice from the ML classifier for that pixel.
  - $f$: Estimated volumetric fill fraction of ice within the regolith (typically assumed between 10% and 30% based on LRO/LCROSS data).

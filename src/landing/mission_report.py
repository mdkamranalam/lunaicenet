import numpy as np
import pandas as pd
from scipy.ndimage import zoom

print("Loading products...")

sites = pd.read_csv("data/final_sites.csv")
hazard = np.load("data/dem/hazard.npy")
safe = np.load("data/dem/safe_zones.npy")
ice = np.load("data/ice/ice_confidence.npy")
ellipse = pd.read_csv("data/landing_ellipses.csv")

# --------------------------------------------------
# Resample ice
# --------------------------------------------------
if ice.shape != hazard.shape:

    scale_y = hazard.shape[0] / ice.shape[0]
    scale_x = hazard.shape[1] / ice.shape[1]

    print(
        f"Resampling ice by "
        f"({scale_y:.4f}, {scale_x:.4f})"
    )

    ice = zoom(
        ice,
        (scale_y, scale_x),
        order=0
    )

    ice = ice[
        :hazard.shape[0],
        :hazard.shape[1]
    ]

# --------------------------------------------------
# Generate mission report
# --------------------------------------------------

reports = []

for _, row in ellipse.iterrows():

    x = int(row["x"])
    y = int(row["y"])

    h = float(hazard[y, x])
    s = bool(safe[y, x])
    i = int(round(ice[y, x]))

    if i == 0:
        ice_text = "None"
    elif i == 1:
        ice_text = "Low"
    elif i == 2:
        ice_text = "Medium"
    else:
        ice_text = "High"

    if row["confidence"] > 0.99:
        recommendation = "EXCELLENT"
    elif row["confidence"] > 0.95:
        recommendation = "GOOD"
    else:
        recommendation = "RISKY"

    reports.append({

        "site_id":
            int(row["site_id"]),

        "x":
            x,

        "y":
            y,

        "mission_score":
            row["mission_score"],

        "ellipse_confidence":
            row["confidence"],

        "hazard":
            h,

        "safe":
            s,

        "ice":
            ice_text,

        "recommendation":
            recommendation
    })

report = pd.DataFrame(reports)

report = report.sort_values(
    "ellipse_confidence",
    ascending=False
)

print()
print("MISSION REPORT")
print("----------------")
print(report.head(20))

# --------------------------------------------------
# Save
# --------------------------------------------------
report.to_csv(
    "data/mission_report.csv",
    index=False
)

print()
print(
    "Saved:",
    "data/mission_report.csv"
)
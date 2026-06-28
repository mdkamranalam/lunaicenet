import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Loading products...")

sites = pd.read_csv(
    "data/final_sites.csv"
)

hazard = np.load(
    "data/dem/hazard.npy"
)

safe = np.load(
    "data/dem/safe_zones.npy"
)

# --------------------------------------------------
# Parameters
# --------------------------------------------------

ELLIPSE_A = 150      # major axis
ELLIPSE_B = 80       # minor axis

results = []

print()
print("Evaluating landing ellipses...")

# --------------------------------------------------
# Evaluate top sites
# --------------------------------------------------

for _, row in sites.head(20).iterrows():

    cx = int(row.x)
    cy = int(row.y)

    y, x = np.ogrid[
        -ELLIPSE_B:ELLIPSE_B,
        -ELLIPSE_A:ELLIPSE_A
    ]

    mask = (
        (x*x)/(ELLIPSE_A*ELLIPSE_A)
        +
        (y*y)/(ELLIPSE_B*ELLIPSE_B)
    ) <= 1

    y0 = max(0, cy-ELLIPSE_B)
    y1 = min(
        hazard.shape[0],
        cy+ELLIPSE_B
    )

    x0 = max(0, cx-ELLIPSE_A)
    x1 = min(
        hazard.shape[1],
        cx+ELLIPSE_A
    )

    h = hazard[y0:y1, x0:x1]
    s = safe[y0:y1, x0:x1]

    mh, mw = h.shape

    ellipse = mask[:mh, :mw]

    if np.sum(ellipse) == 0:
        continue

    hazard_mean = np.mean(
        h[ellipse]
    )

    safe_percent = (
        np.sum(s[ellipse])
        /
        np.sum(ellipse)
    )

    confidence = (
        0.5*(1-hazard_mean)
        +
        0.5*safe_percent
    )

    results.append({
        "site_id":
            row.site_id,

        "x":
            cx,

        "y":
            cy,

        "mission_score":
            row.mission_score,

        "ellipse_safe":
            safe_percent,

        "ellipse_hazard":
            hazard_mean,

        "confidence":
            confidence
    })

# --------------------------------------------------
# Ranking
# --------------------------------------------------

df = pd.DataFrame(results)

df = df.sort_values(
    "confidence",
    ascending=False
)

print()
print("TOP LANDING ELLIPSES")
print("--------------------")
print(df)

# --------------------------------------------------
# Save
# --------------------------------------------------

df.to_csv(
    "data/landing_ellipses.csv",
    index=False
)

print()
print(
    "Saved:",
    "data/landing_ellipses.csv"
)

# --------------------------------------------------
# Visualization
# --------------------------------------------------
display = hazard[::20, ::20]

plt.figure(figsize=(12,7))
plt.imshow(display, cmap="inferno")

for i, (_, row) in enumerate(
        df.head(10).iterrows(),
        start=1):

    x = row.x / 20
    y = row.y / 20

    plt.scatter(
        x,
        y,
        c="cyan",
        s=100,
        marker="x"
    )

    plt.text(
        x+5,
        y,
        str(i),
        color="white"
    )

plt.title("Top Landing Ellipses")
plt.colorbar(label="Hazard")
plt.tight_layout()
plt.show()
import numpy as np
import pandas as pd
from scipy.ndimage import zoom
import matplotlib.pyplot as plt

print("Loading products...")

sites = pd.read_csv("data/candidate_sites.csv")
hazard = np.load("data/dem/hazard.npy")
safe = np.load("data/dem/safe_zones.npy")
ice = np.load("data/ice/ice_confidence.npy")

print("Sites :", len(sites))
print("Hazard:", hazard.shape)
print("Safe  :", safe.shape)
print("Ice   :", ice.shape)

# --------------------------------------------------
# Resample ice map
# --------------------------------------------------

scale_y = hazard.shape[0] / ice.shape[0]
scale_x = hazard.shape[1] / ice.shape[1]

print()
print(
    "Resampling ice by",
    (round(scale_y,4),
     round(scale_x,4))
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
# Score candidates
# --------------------------------------------------

mission_scores = []

for _, row in sites.iterrows():
    x = int(row.x)
    y = int(row.y)

    if (
        x >= hazard.shape[1]
        or
        y >= hazard.shape[0]
    ):
        continue

    suitability = row.mean_score

    hazard_score = (
        1.0 - hazard[y, x]
    )

    safe_score = (
        1.0
        if safe[y, x]
        else 0.0
    )

    ice_score = (
        ice[y, x] / 3.0
    )

    mission = (
        0.40*suitability +
        0.25*hazard_score +
        0.20*safe_score +
        0.15*ice_score
    )

    mission_scores.append({
        "site_id":
            row.site_id,

        "x":
            x,

        "y":
            y,

        "landing":
            suitability,

        "hazard":
            hazard[y, x],

        "safe":
            safe_score,

        "ice":
            ice_score,

        "mission_score":
            mission
    })

# --------------------------------------------------
# Ranking
# --------------------------------------------------

df = pd.DataFrame(
    mission_scores
)

df = df.sort_values(
    "mission_score",
    ascending=False
)

print()
print("TOP 20 LANDING SITES")
print("--------------------")
print(
    df.head(20)
)

# --------------------------------------------------
# Save
# --------------------------------------------------

df.to_csv(
    "data/final_sites.csv",
    index=False
)

print()
print(
    "Saved:",
    "data/final_sites.csv"
)

# --------------------------------------------------
# Visualization
# --------------------------------------------------

display = hazard[::20, ::20]

plt.figure(figsize=(12,7))
plt.imshow(
    display,
    cmap="inferno"
)

for i, (_, row) in enumerate(
        df.head(20).iterrows(),
        start=1):

    plt.scatter(
        row.x/20,
        row.y/20,
        c="cyan",
        s=80,
        marker="x"
    )

    plt.text(
        row.x/20 + 5,
        row.y/20,
        str(i),
        color="white",
        fontsize=8
    )

plt.title("Top Ranked Lunar Landing Sites")

plt.colorbar(label="Hazard")

plt.tight_layout()
plt.show()
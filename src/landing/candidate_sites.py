import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import pandas as pd

print("Loading landing suitability map...")

# --------------------------------------------------
# Load and downsample
# --------------------------------------------------
landing_full = np.load(
    "data/landing_score.npy"
)

landing = landing_full[::20, ::20]

print("Original shape:", landing_full.shape)
print("Working shape :", landing.shape)

# --------------------------------------------------
# Candidate threshold
# --------------------------------------------------
THRESHOLD = 0.90
candidate_mask = landing > THRESHOLD

print()
print("Candidate pixels:",
      np.sum(candidate_mask))

# --------------------------------------------------
# Connected components
# --------------------------------------------------
labels, num = ndimage.label(
    candidate_mask
)

print(
    "Candidate regions:",
    num
)

# --------------------------------------------------
# Extract statistics
# --------------------------------------------------
sites = []
objects = ndimage.find_objects(labels)

for idx, slc in enumerate(objects):
    if slc is None:
        continue

    region = labels[slc] == (idx + 1)

    area = np.sum(region)

    # ignore tiny regions
    if area < 3:
        continue

    y, x = ndimage.center_of_mass(region)

    y += slc[0].start
    x += slc[1].start

    values = landing[
        labels == (idx + 1)
    ]

    sites.append({
        "site_id":
            len(sites) + 1,

        # convert back to full resolution
        "x":
            int(x * 20),

        "y":
            int(y * 20),

        "pixels":
            int(area * 400),

        "mean_score":
            float(np.mean(values)),

        "max_score":
            float(np.max(values))
    })

# --------------------------------------------------
# Ranking
# --------------------------------------------------
sites = sorted(
    sites,
    key=lambda s: s["mean_score"],
    reverse=True
)

df = pd.DataFrame(sites)

print()
print("Top Candidate Sites")
print("-------------------")
print(df.head(20))

# --------------------------------------------------
# Save
# --------------------------------------------------
df.to_csv(
    "data/candidate_sites.csv",
    index=False
)

print()
print("Saved:")
print("data/candidate_sites.csv")

print()
print("Total candidate sites:",
      len(df))

print("Region", idx+1, "area =", area)

# --------------------------------------------------
# Visualization
# --------------------------------------------------
plt.figure(figsize=(12,7))
plt.imshow(
    landing,
    cmap="viridis",
    vmin=np.percentile(landing,5),
    vmax=np.percentile(landing,99)
)

for _, row in df.head(20).iterrows():
    plt.scatter(
        row["x"] / 20,
        row["y"] / 20,
        c="red",
        s=80,
        marker="x"
    )

    plt.text(
        row["x"] / 20 + 5,
        row["y"] / 20,
        str(row["site_id"]),
        color="white",
        fontsize=8
    )

plt.colorbar(
    label="Landing Suitability"
)

plt.title(
    "Top Candidate Lunar Landing Sites"
)

plt.tight_layout()
plt.show()
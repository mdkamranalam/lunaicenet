import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import pandas as pd

print("Loading landing suitability map...")

landing = np.load(
    "data/landing_score.npy"
)

print("Shape:", landing.shape)

# --------------------------------------------------
# Select best regions
# --------------------------------------------------
THRESHOLD = 0.80
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
# Extract site statistics
# --------------------------------------------------
sites = []

for i in range(1, num + 1):
    mask = labels == i
    area = np.sum(mask)

    # ignore tiny regions
    if area < 20:
        continue

    y, x = ndimage.center_of_mass(mask)
    score = np.mean(
        landing[mask]
    )

    maximum = np.max(
        landing[mask]
    )

    sites.append({
        "site_id": len(sites)+1,
        "x": int(x),
        "y": int(y),
        "pixels": int(area),
        "mean_score": float(score),
        "max_score": float(maximum)
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
print(
    "Saved:",
    "data/candidate_sites.csv"
)

# --------------------------------------------------
# Visualization
# --------------------------------------------------
display = landing[::20, ::20]
plt.figure(figsize=(10,6))
plt.imshow(
    display,
    cmap="viridis"
)

for _, row in df.head(20).iterrows():
    plt.scatter(
        row["x"]/20,
        row["y"]/20,
        c="red",
        s=50,
        marker="x"
    )

plt.title(
    "Top Candidate Landing Sites"
)

plt.tight_layout()
plt.show()
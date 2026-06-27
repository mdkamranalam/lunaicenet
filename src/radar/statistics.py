from spectral import open_image
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]

cpr = open_image(
    str(ROOT/"data/cpr/cpr.bin.hdr")
).load()

dop = open_image(
    str(ROOT/"data/dop/dop.bin.hdr")
).load()

cpr = np.squeeze(cpr)
dop = np.squeeze(dop)

# remove NaNs
cpr = cpr[np.isfinite(cpr)]
dop = dop[np.isfinite(dop)]

print("\nCPR Statistics")
print("----------------")
print("mean:",np.mean(cpr))
print("median:",np.median(cpr))
print("std:",np.std(cpr))
print("95 percentile:",np.percentile(cpr,95))
print("99 percentile:",np.percentile(cpr,99))

print("\nDOP Statistics")
print("----------------")
print("mean:",np.mean(dop))
print("median:",np.median(dop))
print("std:",np.std(dop))
print("95 percentile:",np.percentile(dop,95))
print("99 percentile:",np.percentile(dop,99))
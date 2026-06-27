from spectral import open_image
import matplotlib.pyplot as plt

print("Loading CPR...")
cpr = open_image(
    r"D:\Programming\hackathon\lunaicenet\data\cpr\cpr.bin.hdr"
)
cpr_data = cpr.load()

print("Loading DOP...")
dop = open_image(
    r"D:\Programming\hackathon\lunaicenet\data\dop\dop.bin.hdr"
)
dop_data = dop.load()

print("CPR Shape:", cpr_data.shape)
print("DOP Shape:", dop_data.shape)

plt.figure(figsize=(8,6))
plt.imshow(cpr_data)
plt.title("CPR")
plt.colorbar()
plt.show()

plt.figure(figsize=(8,6))
plt.imshow(dop_data)
plt.title("DOP")
plt.colorbar()
plt.show()
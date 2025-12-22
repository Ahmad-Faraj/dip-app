from Gauss_Filter import GaussFilter
from MinMax_Filter import MinMaxFilter
from PIL import Image
import numpy as np

print("Loading sample image...")
img = Image.new("RGB", (10, 10), color=(128, 128, 128))
arr = np.array(img)

print("Testing GaussFilter...")
try:
    gf = GaussFilter()
    out = gf.gauss_filter_custom(arr, size=3, method="padding")
    print("Gauss output shape:", out.shape, out.dtype)
except Exception as e:
    print("Gauss failed:", e)

print("Testing MinMaxFilter...")
try:
    mf = MinMaxFilter()
    out2 = mf.min_max_filter_custom(arr, size=3, mode="min", method="padding")
    print("MinMax output shape:", out2.shape, out2.dtype)
except Exception as e:
    print("MinMax failed:", e)

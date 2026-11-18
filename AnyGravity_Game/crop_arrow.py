from PIL import Image

im = Image.open(r"C:\Users\rupan\.gemini\antigravity\brain\77da8798-9795-4cb4-bad1-c04a07ad04af\.user_uploaded\media_1794939006432_da698125.jpg")
w, h = im.size
print(f"Image size: {w}x{h}")

# Find pixels that are blue (the arrow)
# Blue stroke is #2563eb -> RGB(37, 99, 235)
blue_pixels = []
for y in range(h):
    for x in range(w):
        r, g, b = im.getpixel((x, y))[:3]
        if b > 180 and b > r + 50 and b > g + 30:
            blue_pixels.append((x, y))

if blue_pixels:
    xs = [p[0] for p in blue_pixels]
    ys = [p[1] for p in blue_pixels]
    print(f"Blue arrow bbox: x=[{min(xs)}, {max(xs)}], y=[{min(ys)}, {max(ys)}]")
    # Crop around the blue arrow and surrounding area
    crop_box = (max(0, min(xs) - 80), max(0, min(ys) - 80), min(w, max(xs) + 120), min(h, max(ys) + 80))
    cropped = im.crop(crop_box)
    cropped.save("arrow_crop.png")
    print(f"Saved arrow_crop.png with box {crop_box}")

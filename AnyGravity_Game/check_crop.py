from PIL import Image
im = Image.open(r'C:\Users\rupan\.gemini\antigravity\brain\77da8798-9795-4cb4-bad1-c04a07ad04af\.user_uploaded\media_1794939006432_da698125.jpg')
arrow_pts = []
for y in range(400, 500):
    for x in range(280, 420):
        r, g, b = im.getpixel((x, y))[:3]
        if b > 180 and b > r + 60 and b > g + 40:
            arrow_pts.append((x, y))

if arrow_pts:
    xs = [p[0] for p in arrow_pts]
    ys = [p[1] for p in arrow_pts]
    print(f'Arrow bounds: x=[{min(xs)}, {max(xs)}], y=[{min(ys)}, {max(ys)}]')
    dots = []
    for y in range(200, 650):
        for x in range(350, 750):
            r, g, b = im.getpixel((x, y))[:3]
            if 160 < r < 210 and 180 < g < 225 and 210 < b < 245:
                dots.append((x, y))
    if dots:
        dxs = [p[0] for p in dots]
        print(f'Dots bounds: x=[{min(dxs)}, {max(dxs)}]')

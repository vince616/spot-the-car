import os
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "..", "icon-source.png")
RES = os.path.join(BASE, "..", "android", "app", "src", "main", "res")

LEGACY_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}
FOREGROUND_SIZES = {
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432,
}

src = Image.open(SRC).convert("RGBA")

def circular_mask(im):
    size = im.size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0] - 1, size[1] - 1), fill=255)
    out = im.copy()
    out.putalpha(mask)
    return out

for density, size in LEGACY_SIZES.items():
    d = os.path.join(RES, density)
    square = src.resize((size, size), Image.LANCZOS)
    square.save(os.path.join(d, "ic_launcher.png"))
    circular_mask(square).save(os.path.join(d, "ic_launcher_round.png"))
    print(f"{density}: ic_launcher.png / ic_launcher_round.png ({size}x{size})")

for density, size in FOREGROUND_SIZES.items():
    d = os.path.join(RES, density)
    fg = src.resize((size, size), Image.LANCZOS)
    fg.save(os.path.join(d, "ic_launcher_foreground.png"))
    print(f"{density}: ic_launcher_foreground.png ({size}x{size})")

# Play Store listing icon (not used by the APK itself, kept for later store submission)
store_icon = src.resize((512, 512), Image.LANCZOS)
store_icon.save(os.path.join(BASE, "..", "icon-512-playstore.png"))
print("Wrote icon-512-playstore.png")

"""Copy the authored dashboard artwork next to the generated HTML."""
import shutil
from pathlib import Path

project = Path(__file__).resolve().parents[1]
source = project / "src" / "content" / "assets" / "pack-art"
destination = project / "dist" / "artwork"
images = sorted(source.glob("*.webp"))
if len(images) != 33:
    raise SystemExit(f"Expected 33 artwork files, found {len(images)}")
destination.mkdir(parents=True, exist_ok=True)
for image in images:
    shutil.copy2(image, destination / image.name)
print(f"Staged {len(images)} original dashboard cover images in {destination}")

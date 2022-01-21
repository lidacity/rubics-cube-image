from PIL import Image
from rubiks_cube_image import GetImage

Cube = list("OBBOYYWWRWWROORGOGBRYBBGWRYBGORRYBGYWWGBGYOBYRYOGWWROG")
C = "Z"
Image0 = GetImage(Cube, 300)
Image0.save(f"Cube.png")
Image1 = GetImage(Cube, 300, Command=f"{C}")
Image1.save(f"{C}.png")
Image2 = GetImage(Cube, 300, Command=f"{C}'")
Image2.save(f"{C}'.png")
Image3 = GetImage(Cube, 300, Command=f"{C}2")
Image3.save(f"{C}2.png")

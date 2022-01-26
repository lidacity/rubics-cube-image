import io

from PIL import Image, ImageDraw, ImageFont
import numpy as np

from rubiks_cube_image.arrow import GetArrow
from rubiks_cube_image.line import GetLine


Colors = {
 "W": (255, 255, 255), #"white",
 "O": (223, 138, 67), #"orange",
 "G": (85, 148, 100), #"green",
 "R": (180, 62, 59), #"red",
 "B": (35, 89, 162), #"blue",
 "Y": (245, 234, 124), #"yellow",
}


FillColor = (0, 0, 0, 128)
LineColor = (0, 0, 0, 160)


#https://stackoverflow.com/questions/42827978/image-perspective-transform-using-pillow
#https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil/14178717
def FindCoeffs(OriginalCoords, WarpedCoords):
 Matrix = []
 for p1, p2 in zip(OriginalCoords, WarpedCoords):
  Matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
  Matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
 A = np.matrix(Matrix, dtype=np.float64)
 B = np.array(WarpedCoords).reshape(8)
 Result = np.dot(np.linalg.inv(A.T * A) * A.T, B)
 return np.array(Result).reshape(8)


def Get0(OriginalCoords, WarpedCoords):
 a, b, c, d, e, f, g, h = FindCoeffs(WarpedCoords, OriginalCoords)
 x = y = 0
 x1 = (a * x + b * y + c) / (g * x + h * y + 1)
 y1 = (d * x + e * y + f) / (g * x + h * y + 1)
 w1 = h1 = 0
 for w, h in OriginalCoords:
  w1 = max(w1, w) 
  h1 = max(h1, h) 
 return int(x1), int(y1), int(w1), int(h1)


def GetCoordArrow(X, Y, Direction, Size):
 x, y = X * Size + Size // 2, Y * Size + Size // 2
 t0 = Size // 4
 t1 = Size // 3
 h0 = Size * 2 // 3
 h1 = Size // 9
 if Direction == "U":
  return ((x, y - t1), (x - t0, y - t1 + h0), (x, y - t1 + h0 - h1), (x + t0, y - t1 + h0))
 elif Direction == "L":
  return ((x - t1, y), (x - t1 + h0, y - t0), (x - t1 + h0 - h1, y), (x - t1 + h0, y + t0))
 elif Direction == "D":
  return ((x, y + t1), (x - t0, y + t1 - h0), (x, y + t1 - h0 + h1), (x + t0, y + t1 - h0))
 elif Direction == "R":
  return ((x + t1, y), (x + t1 - h0, y - t0), (x + t1 - h0 + h1, y), (x + t1 - h0, y + t0))


def GetCoordLine(X, Y, Direction, Way, Full, Size):
 x, y = X * Size + Size // 2, Y * Size + Size // 2
 t1 = Size // 3
 h0 = Size * 2 // 3
 h1 = Size // 9
 FullSize = Size * 3
 HalfSize = Size // 2
 if Direction == "U":
  if Way == "B":
   return ((x, y - t1 + 3), (x, 0 if Full else HalfSize))
  elif Way == "E":
   return ((x, y - t1 + h0 - h1 - 3), (x, FullSize if Full else FullSize - HalfSize))
 #
 elif Direction == "L":
  if Way == "B":
   return ((x - t1 + 3, y), (0 if Full else HalfSize, y))
  elif Way == "E":
   return ((x - t1 + h0 - h1 - 3, y), (FullSize if Full else FullSize - HalfSize, y))
 #
 elif Direction == "D":
  if Way == "B":
   return ((x, y + t1 - 3), (x, FullSize if Full else FullSize - HalfSize))
  elif Way == "E":
   return ((x, y + t1 - h0 + h1 + 3), (x, 0 if Full else HalfSize))
 #
 elif Direction == "R":
  if Way == "B":
   return ((x + t1 - 3, y), (FullSize if Full else FullSize - HalfSize, y))
  elif Way == "E":
   return ((x + t1 - h0 + h1 + 3, y), (0 if Full else HalfSize, y))
 #
 return None


def DrawArrow(Draw1, X, Y, Direction, Way, Full, Size):
 Width = Size // 16
 Arrow = GetCoordArrow(X, Y, Direction, Size)
 Line = GetCoordLine(X, Y, Direction, Way, Full, Size)
 Draw1.polygon(Arrow, fill=FillColor, outline=LineColor)
 Draw1.line(Line, fill=LineColor, width=Width)


def DrawLine(Draw1, Direction, I, Full, Size):
 Width = Size // 16
 Line = None
 if Full:
  if Direction == "Col":
   x = I * Size + Size // 2
   Line = ((x, 0), (x, Size * 3))
  elif Direction == "Row":
   y = I * Size + Size // 2
   Line = ((0, y), (Size * 3, y))
 else:
  if Direction == "Col":
   x = I * Size + Size // 2
   y1, y2 = 0 * Size + Size // 2, 2 * Size + Size // 2
   Line = ((x, y1), (x, y2))
  elif Direction == "Row":
   x1, x2 = 0 * Size + Size // 2, 2 * Size + Size // 2
   y = I * Size + Size // 2
   Line = ((x1, y), (x2, y))
 Draw1.line(Line, fill=LineColor, width=Width)


def DrawCommand(Face, Image1, Size, Command):
 if Command is None:
  return Image1
 else:
  Image2 = Image.new('RGBA', Image1.size)
  Draw2 = ImageDraw.Draw(Image2)
  S = Size // 3
  for X, Y, Direction, Way, Full in GetArrow(Command, Face):
   DrawArrow(Draw2, X, Y, Direction, Way, Full, S)
  #
  for Direction, I, Full in GetLine(Command, Face):
   DrawLine(Draw2, Direction, I, Full, S)
  #
  return Image.alpha_composite(Image1, Image2)


def GetImage(Cube, Size, Command=None):
 Coords = {
  "0": [ (0, 0), (Size, 0), (Size, Size), (0, Size) ],
  "U": [ (Size // 2, 0), (Size + Size // 2, 0), (Size, Size // 2), (0, Size // 2) ],
  "L": [ (Size // 2, 0), (0, Size // 2), (0, Size + Size // 2), (Size // 2, Size) ],
  "F": [ (0, 0), (Size, 0), (Size, Size), (0, Size) ], 
  "R": [ (0, Size // 2), (Size // 2, 0), (Size // 2, Size), (0, Size + Size // 2) ],
  "B": [ (Size, 0), (0, 0), (0, Size), (Size, Size) ],
  "D": [ (0, Size // 2), (Size, Size // 2), (Size + Size // 2, 0), (Size // 2, 0) ],
 }
 #
 Position = [
  { "Face": 'B', "x": Size // 2 + Size // 6 + Size + Size // 3, "y": 0 },
  { "Face": "D", "x": Size // 2 + Size // 6, "y": Size + Size // 3 + Size + Size // 6 },
  { "Face": "L", "x": 0, "y": Size + Size // 3 - Size // 2 },
  { "Face": "U", "x": Size // 2 + Size // 6, "y": Size + Size // 3 - Size // 2 },
  { "Face": "R", "x": Size // 2 + Size // 6 + Size , "y": Size + Size // 3 - Size // 2 },
  { "Face": "F", "x": Size // 2 + Size // 6, "y": Size + Size // 3 },
 ]
 #
 Sides = {}
 for FaceIndex, Face in enumerate(list("ULFRBD")):
  Image1 = Image.new('RGBA', (Size, Size), 0)
  Draw1 = ImageDraw.Draw(Image1)
  Draw1.rectangle((0, 0, Size, Size), fill='black')
  Size0 = min(1, Size / 150)
  w = h = Size / 3 - Size0 * 2
  for Index in range(9):
   x, y = Size0 + Index % 3 * Size / 3, Size0 + Index // 3 * Size / 3
   C = Cube[(FaceIndex * 9) + Index]
   #print(Face, (FaceIndex * 9) + Index, Cube[(FaceIndex * 9) + Index], Color)
   Draw1.rounded_rectangle((x, y, x + w - 1, y + h - 1), radius=Size // 50, fill=Colors[C])
  #Image1.save(f"{Face}.png")
  Image2 = DrawCommand(Face, Image1, Size, Command)
  #Image2.save(f"{Face}_.png")
  x0, y0, w0, h0 = Get0(Coords[Face], Coords["0"])
  #print(x0, y0, w0, h0, Coords[Face])
  Coeffs = FindCoeffs(Coords[Face], Coords["0"])
  Image3 = Image2.transform(((w0, h0)), method=Image.PERSPECTIVE, data=Coeffs)
  #Image3.save(f"{Face}__.png")
  Sides[Face] = { "Image": Image3, "x": x0, "y": y0, "w": w0, "h": h0 }
 #
 w = h = 0
 for Item in Position:
  w = max(Item["x"], w)
  h = max(Item["y"], h)
 Result = Image.new('RGBA', (w + Size, h + Size // 2), 0)
 #
 if Command is not None:
  Font1 = ImageFont.truetype("FreeMono.ttf", Size // 3)
  Draw1 = ImageDraw.Draw(Result)
  Draw1.text((Size - Size / 5, Size / 5), Command, font=Font1, fill="black")
 #
 for Item in Position:
  Face = Item["Face"]
  x, y = Item["x"], Item["y"]
  Side = Sides[Face]
  Result.alpha_composite(Side["Image"], (x, y))
 #Result.save(f"Result.png")
 return Result


def GetRaw(Cube, Size, Command=None):
 Result = io.BytesIO()
 Image1 = GetImage(Cube, Size, Command=Command)
 Image1.save(Result, format=image.format)
 return Result.getvalue()

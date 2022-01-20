from PIL import Image, ImageDraw, ImageFont
import numpy as np

Colors = {
 "W": (255, 255, 255), #"white",
 "O": (223, 138, 67), #"orange",
 "G": (85, 148, 100), #"green",
 "R": (180, 62, 59), #"red",
 "B": (35, 89, 162), #"blue",
 "Y": (245, 234, 124), #"yellow",
}


'''
  U
L F R B
  D

           01 02 03
           04 05 06
           07 08 09

 10 11 12  19 20 21  28 29 30  37 38 39
 13 14 15  22 23 24  31 32 33  40 41 42
 16 17 18  25 26 27  34 35 36  43 44 45

           46 47 48
           49 50 51
           52 53 54
''' 

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


After, Before = range(2)
Up, Left, Down, Right = range(4)


def GetArrow(X, Y, Direction, Size):
 x, y = X * Size + Size // 2, Y * Size + Size // 2
 t0 = Size // 4
 t1 = Size // 3
 h0 = Size * 2 // 3
 h1 = Size // 9
 if Direction == Up:
  return ((x, y - t1), (x - t0, y - t1 + h0), (x, y - t1 + h0 - h1), (x + t0, y - t1 + h0))
 elif Direction == Left:
  return ((x - t1, y), (x - t1 + h0, y - t0), (x - t1 + h0 - h1, y), (x - t1 + h0, y + t0))
 elif Direction == Down:
  return ((x, y + t1), (x - t0, y + t1 - h0), (x, y + t1 - h0 + h1), (x + t0, y + t1 - h0))
 elif Direction == Right:
  return ((x + t1, y), (x + t1 - h0, y - t0), (x + t1 - h0 + h1, y), (x + t1 - h0, y + t0))


def GetLine(X, Y, Direction, Way, Full, Size):
 x, y = X * Size + Size // 2, Y * Size + Size // 2
 t1 = Size // 3
 h0 = Size * 2 // 3
 h1 = Size // 9
 if Direction == Up:
  if Way == After:
   return ((x, y - t1 + 3), (x, 0) if Full else (x, Size // 2))
  elif Way == Before:
   return ((x, y - t1 + h0 - h1 - 3), (x, Size * 3) if Full else (x, Size * 3 - Size // 2))
 #
 elif Direction == Left:
  if Way == After:
   return ((x - t1 + 3, y), (Size * 3, y) if Full else (Size // 2, y))
  elif Way == Before:
   return ((x - t1 + h0 - h1 - 3, y), (0, y) if Full else (Size * 3 - Size // 2, y))
 #
 elif Direction == Down:
  if Way == After:
   return ((x, y + t1 - 3), (x, Size * 3) if Full else (x, Size * 3 - Size // 2))
  elif Way == Before:
   return ((x, y + t1 - h0 + h1 + 3), (x, 0) if Full else (x, Size // 2))
 #
 elif Direction == Right:
  if Way == After:
   return ((x + t1 - 3, y), (0, y) if Full else (Size * 3 - Size // 2, y))
  elif Way == Before:
   return ((x + t1 - h0 + h1 + 3, y), (Size * 3, y) if Full else (Size // 2, y))
 #
 return None


FillColor = (0, 0, 0, 128)
LineColor = (0, 0, 0, 160)


def DrawArrow(Draw1, X, Y, Direction, Way, Full, Size):
 Width = Size // 16
 Arrow = GetArrow(X, Y, Direction, Size)
 Line = GetLine(X, Y, Direction, Way, Full, Size)
 Draw1.polygon(Arrow, fill=FillColor, outline=LineColor)
 Draw1.line(Line, fill=LineColor, width=Width)


def DrawLine(Draw1, Full, Size, Col=None, Row=None):
 Width = Size // 16
 Line = None
 if Full:
  if Col is not None:
   x = Col * Size + Size // 2
   Line = ((x, 0), (x, Size * 3))
  elif Row is not None:
   y = Row * Size + Size // 2
   Line = ((0, y), (Size * 3, y))
 else:
  if Col is not None:
   x = Col * Size + Size // 2
   y1, y2 = 0 * Size + Size // 2, 2 * Size + Size // 2
   Line = ((x, y1), (x, y2))
  elif Row is not None:
   x1, x2 = 0 * Size + Size // 2, 2 * Size + Size // 2
   y = Row * Size + Size // 2
   Line = ((x1, y), (x2, y))
 Draw1.line(Line, fill=LineColor, width=Width)



def DrawCommand(Face, Image1, Size, Command):
 Image2 = Image.new('RGBA', Image1.size)
 Draw2 = ImageDraw.Draw(Image2)
 S = Size // 3
 #
 if Command == "L":
  if Face == "L":
   DrawArrow(Draw2, 1, 0, Right, After, False, S)
   DrawArrow(Draw2, 2, 1, Down, Before, False, S)
  elif Face == "U":
   DrawArrow(Draw2, 0, 1, Down, After, True, S)
  elif Face == "F":
   DrawArrow(Draw2, 0, 1, Down, Before, True, S)
 elif Command == "L'":
  if Face == "L":
   DrawArrow(Draw2, 2, 1, Up, After, False, S)
   DrawArrow(Draw2, 1, 0, Left, Before, False, S)
  elif Face == "F":
   DrawArrow(Draw2, 0, 1, Up, After, True, S)
  elif Face == "U":
   DrawArrow(Draw2, 0, 1, Up, Before, True, S)
 elif Command == "L2":
  if Face == "L":
   DrawArrow(Draw2, 1, 0, Right, After, False, S)
   DrawLine(Draw2, False, S, Col=2)
   DrawArrow(Draw2, 1, 2, Left, Before, False, S)
  elif Face == "U":
   DrawArrow(Draw2, 0, 1, Down, After, True, S)
  elif Face == "F":
   DrawLine(Draw2, True, S, Col=0)
  elif Face == "D":
   DrawArrow(Draw2, 0, 1, Down, Before, True, S)
 #
# "R": [ [ "R", ], ],
# "R'": [ [ "R'", ], ],
# "R2": [ [ "R2", ], ],
# "U": [ [ "U", ], ],
# "U'": [ [ "U'", ], ],
# "U2": [ [ "U2", ], ],
# "D": [ [ "D", ], ],
# "D'": [ [ "D'", ], ],
# "D2": [ [ "D2", ], ],
# "X": [ [ "X", ], ],
# "X'": [ [ "X'", ], ],
# "X2": [ [ "X2", ], ],
# "Y": [ [ "Y", ], ],
# "Y'": [ [ "Y'", ], ],
# "Y2": [ [ "Y2", ], ],
# # change unsupported
# "F": [ [ "Y", "L", "Y'", ], [ "Y'", "R", "Y", ], ],
# "F'": [ [ "Y", "L'", "Y'", ], [ "Y'", "R'", "Y", ], ],
# "F2": [ [ "Y", "L2", "Y'", ], [ "Y'", "R2", "Y", ], ],
# "B": [ [ "Y", "R", "Y'", ], [ "Y'", "L", "Y", ], ],
# "B'": [ [ "Y", "R'", "Y'", ], [ "Y'", "L'", "Y", ], ],
# "B2": [ [ "Y", "R2", "Y'", ], [ "Y'", "L2", "Y", ], ],
# "M": [ [ "X'", "L'", "R", ], [ "X'", "R", "L'", ],  [ "L'", "X'", "R", ], [ "L'", "R", "X'", ], [ "R", "X'", "L'", ], [ "R", "L'", "X'", ], ],
# "M'": [ [ "X", "L", "R'", ], [ "X", "R'", "L", ], [ "L", "X", "R'", ], [ "L", "R'", "X", ], [ "R'", "X", "L", ], [ "R'", "L", "X", ], ],
# "M2": [ [ "X2", "L2", "R2", ], [ "X2", "R2", "L2", ], [ "L2", "X2", "R2", ], [ "L2", "R2", "X2", ], [ "R2", "X2", "L2", ], [ "R2", "L2", "X2", ], ],
# "E": [ [ "Y'", "U", "D'", ], [ "Y'", "D'", "U", ], [ "U", "Y'", "D'", ], [ "U", "D'", "Y'", ], [ "D'", "Y'", "U", ], [ "D'", "U", "Y'", ], ],
# "E'": [ [ "Y", "U'", "D", ], [ "Y", "D", "U'", ], [ "U'", "Y", "D", ], [ "U'", "D", "Y", ], [ "D", "Y", "U'", ], [ "D", "U'", "Y", ], ],
# "E2": [ [ "Y2", "U2", "D2", ], [ "Y2", "D2", "U2",  ], [ "U2", "Y2", "D2", ], [ "U2", "D2", "Y2",  ], [ "D2", "Y2", "U2", ], [ "D2", "U2", "Y2",  ], ],
# "S": [ [ "Y", "X'", "L'", "R", "Y'", ], [ "Y", "X'", "R", "L'", "Y'", ],  [ "Y", "L'", "X'", "R", "Y'", ], [ "Y", "L'", "R", "X'", "Y'", ], [ "Y", "R", "X'", "L'", "Y'", ], [ "Y", "R", "L'", "X'", "Y'", ], [ "Y'", "X", "L", "R'", "Y", ], [ "Y'", "X", "R'", "L", "Y", ], [ "Y'", "L", "X", "R'", "Y", ], [ "Y'", "L", "R'", "X", "Y", ], [ "Y'", "R'", "X", "L", "Y", ], [ "Y'", "R'", "L", "X", "Y", ], ],
# "S'": [ [ "Y", "X", "L", "R'", "Y'", ], [ "Y", "X", "R'", "L", "Y'", ],  [ "Y", "L", "X", "R'", "Y'", ], [ "Y", "L", "R'", "X", "Y'", ], [ "Y", "R'", "X", "L", "Y'", ], [ "Y", "R'", "L", "X", "Y'", ], [ "Y'", "X'", "L'", "R", "Y", ], [ "Y'", "X'", "R", "L'", "Y", ], [ "Y'", "L'", "X'", "R", "Y", ], [ "Y'", "L'", "R", "X'", "Y", ], [ "Y'", "R", "X'", "L'", "Y", ], [ "Y'", "R", "L'", "X'", "Y", ], ],
# "S2": [ [ "Y", "X2", "L2", "R2", "Y'" ], [ "Y", "X2", "R2", "L2", "Y'" ], [ "Y", "L2", "X2", "R2", "Y'" ], [ "Y", "L2", "R2", "X2", "Y'" ], [ "Y", "R2", "X2", "L2", "Y'" ], [ "Y", "R2", "L2", "X2", "Y'" ], [ "Y'", "X2", "L2", "R2", "Y" ], [ "Y'", "X2", "R2", "L2", "Y" ], [ "Y'", "L2", "X2", "R2", "Y" ], [ "Y'", "L2", "R2", "X2", "Y" ], [ "Y", "R2", "X2", "L2", "Y'" ], [ "Y", "R2", "L2", "X2", "Y'" ], ],
## "u": [],
## "l": [],
## "f": [],
## "r": [],
## "b": [],
## "d": [],
## "u'": [],
## "l'": [],
# "f'": [],
# "r'": [],
# "b'": [],
# "d'": [],
# "u2": [],
# "l2": [],
# "f2": [],
# "r2": [],
# "b2": [],
# "d2": [],
# "Z": [],
# "Z'": [],
# "Z2": [],
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
  Image1.save(f"{Face}.png")
  if Command is not None:
   Image2 = DrawCommand(Face, Image1, Size, Command)
  Image2.save(f"{Face}_.png")
  x0, y0, w0, h0 = Get0(Coords[Face], Coords["0"])
  #print(x0, y0, w0, h0, Coords[Face])
  Coeffs = FindCoeffs(Coords[Face], Coords["0"])
  Image3 = Image2.transform(((w0, h0)), method=Image.PERSPECTIVE, data=Coeffs)
  Image3.save(f"{Face}__.png")
  Sides[Face] = { "Image": Image3, "x": x0, "y": y0, "w": w0, "h": h0 }
 #
 w = h = 0
 for Item in Position:
  w = max(Item["x"], w)
  h = max(Item["y"], h)
 #
 if Command is not None:
  Result = Image.new('RGBA', (w + Size, h + Size // 2), 0)
  Font1 = ImageFont.truetype("FreeMono.ttf", Size // 3)
  Draw1 = ImageDraw.Draw(Result)
  Draw1.text((Size - Size / 5, Size / 5), Command, font=Font1, fill="black")
 #
 for Item in Position:
  Face = Item["Face"]
  x, y = Item["x"], Item["y"]
  Side = Sides[Face]
  Result.alpha_composite(Side["Image"], (x, y))
 Result.save(f"Result.png")
 return Result






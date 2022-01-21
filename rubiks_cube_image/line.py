Array = {
 "L2": {
  "L": [ ( "Row", 2, False ), ],
  "D": [ ( "Col", 0, True ), ],
 },
 "R2": {
  "R": [ ( "Row", 0, False ), ],
  "U": [ ( "Col", 2, True ), ],
 },
 "U2": {
  "U": [ ( "Col", 0, False ), ],
  "L": [ ( "Row", 0, True ), ],
 }, 
 "D2": {
  "D": [ ( "Col", 2, False ), ],
  "R": [ ( "Row", 2, True ), ],
 }, 
 "X2": {
  "L": [ ( "Row", 0, False ), ],
  "R": [ ( "Row", 0, False ), ],
  "U": [ ( "Col", 0, True ), ( "Col", 1, True ), ( "Col", 2, True ), ],
 },
 "Y2": {
  "U": [ ( "Col", 0, False ), ],
  "D": [ ( "Col", 0, False ), ],
  "L": [ ( "Row", 0, True ), ( "Row", 1, True ), ( "Row", 2, True ), ],
 },
# # change unsupported
 "F2": {
  "F": [ ( "Col", 2, False ), ],
  "R": [ ( "Col", 0, True ), ],
 },
 "B2": {
  "B": [ ( "Col", 2, False ), ],
  "L": [ ( "Col", 0, True ), ],
 },
 "M2": {
  "D": [ ( "Col", 1, True ), ],
 },
 "E2": {
  "R": [ ( "Row", 1, True ), ],
 },
 "S2": {
  "R": [ ( "Col", 1, True ), ],
 },
 "u2": {
  "U": [ ( "Col", 0, False ), ],
  "L": [ ( "Row", 0, True ), ( "Row", 1, True ), ],
 },
 "l2": {
  "L": [ ( "Row", 2, False ), ],
  "D": [ ( "Col", 0, True ), ( "Col", 1, True ), ],
 },
 "f2": {
  "F": [ ( "Col", 2, False ), ],
  "R": [ ( "Col", 0, True ), ( "Col", 1, True ), ],
 },
 "r2": {
  "R": [ ( "Row", 0, False ), ],
  "U": [ ( "Col", 2, True ),  ( "Col", 1, True ), ],
 },
 "b2": {
  "B": [ ( "Col", 2, False ), ],
  "L": [ ( "Col", 0, True ),  ( "Col", 1, True ), ],
 },
 "d2": {
  "D": [ ( "Col", 2, False ), ],
  "R": [ ( "Row", 2, True ),  ( "Row", 1, True ), ],
 },
 "Z2": {
  "F": [ ( "Col", 2, False ), ],
  "B": [ ( "Col", 0, False ), ],
  "R": [ ( "Col", 0, True ), ( "Col", 1, True ), ( "Col", 2, True ), ],
 },
}


def GetLine(Command, Face):
 return Array.get(Command, {}).get(Face, [])

#!/usr/bin/env python3

# Uključivanje matematičkog modula
from math import sin, cos, radians

# Geometrijska transformacija ravni
# predstavljena homogenom 3x3 matricom
class Geom:
  # Konstruktor transformacije
  def __init__(self, mat):
    self.mat = mat
  
  # Uobičajeno množenje matrica ili, pak,
  # množenje matrice sa tačkom ravni
  def __mul__(self, dr):
    if isinstance(dr, Geom):
      pom = tuple(tuple(sum(self[i][k] * dr[k][j] for k in range(3))
                           for j in range(3)) for i in range(3))

      return Geom(pom)
    else:
      drr = (dr[0], dr[1], 1)
      
      pom = tuple(sum(self[i][j] * drr[j]
                  for j in range(3)) for i in range(3))
      
      return Tačka(pom) if isinstance(dr, Tačka) else (pom[0], pom[1])
  
  # Magični metod za dohvatanje elemata
  def __getitem__(self, indeks):
    return self.mat[indeks]
  
  # Uobičajena string predstava matrice
  def __str__(self):
    return 'Transformacija:\n[(%.2f, %.2f, %.2f)\n' \
           ' (%.2f, %.2f, %.2f)\n (%.2f, %.2f, %.2f)]' \
           % (self[0][0], self[0][1], self[0][2],
              self[1][0], self[1][1], self[1][2],
              self[2][0], self[2][1], self[2][2])

# Translacija nasleđuje geom. trans.
class Trans(Geom):
  def __init__(self, x=0, y=0):
    self.mat = ((1, 0, x),
                (0, 1, y),
                (0, 0, 1))

# Skaliranje nasleđuje geom. trans.
class Skal(Geom):
  def __init__(self, x=1, y=1):
    self.mat = ((x, 0, 0),
                (0, y, 0),
                (0, 0, 1))

# Smicanje nasleđuje geom. trans.
class Smic(Geom):
  def __init__(self, x=0, y=0):
    self.mat = ((1, x, 0),
                (y, 1, 0),
                (0, 0, 1))

# Rotacija nasleđuje geom. trans.
class Rot(Geom):
  def __init__(self, u=0):
    pom1 = cos(radians(u))
    pom2 = sin(radians(u))
    
    self.mat = ((pom1, -pom2,  0),
                (pom2,  pom1,  0),
                (0,      0,    1))

# Refleksija nasleđuje geom. trans.
class Refl(Geom):
  def __init__(self, u=0):
    pom1 = cos(radians(u))
    pom2 = sin(radians(u))
    
    self.mat = ((pom1,  pom2,  0),
                (pom2, -pom1,  0),
                (0,      0,    1))

# Tačka predstavljena koordinatama
class Tačka:
  def __init__(self, x=0, y=0, w=1):
    if (isinstance(x, tuple)):
      self.mat = x
    else:
      self.mat = (x/w, y/w, 1)
  
  # Magični metod za dohvatanje elemata
  def __getitem__(self, indeks):
    return self.mat[indeks]
  
  # Uobičajena string predstava tačke
  def __str__(self):
    return 'Tačka:\n[(%.2f, %.2f)]' % (self.mat[0], self.mat[1])

# Fja za testiranje implementiranih klasa;
# predlaže se pokretanje sa < test.py, gde
# se nalaze transformacije bitne za rad
def test():
  print('Unosite linije koda do kraja ulaza.\n'
        'Podržano: dodela, kompozicija, štampanje.\n'
        'Transformacije: translacija, skaliranje,\n'
        'smicanje, rotacija, refleksija.\n')
  
  # Mali interpretator koji se oslanja
  # na pozivanje Pajtonovog interpretera;
  # u pitanju je poznata RE(P)L petlja
  while True:
    try:
      linija = input()
      exec(linija)
    except EOFError:
      print('Kraj ulaza.')
      break
    except:
      print('Pokušajte ponovo.')

# Poziv test funkcije ukoliko
# je modul direktno izvršen
if __name__ == '__main__':
  test()

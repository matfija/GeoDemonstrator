#!/usr/bin/env python3

# Uključivanje matematičkog modula
from math import sin, cos, radians

# Geometrijska transformacija ravni
# predstavljena homogenom 3x3 matricom
class geom:
  # Konstruktor transformacije
  def __init__(self, mat):
    self.mat = mat
  
  # Uobičajeno množenje matrica ili, pak,
  # množenje matrice sa tačkom prostora
  def __mul__(self, dr):
    if isinstance(dr, geom):
      pom = [[0 for i in range(3)] for j in range(3)]
        
      for i in range(3):
        for j in range(3):
          for k in range(3):
            pom[i][j] += self.mat[i][k] * dr.mat[k][j]

      return geom(pom)
    else:
      pom = [0 for i in range(3)] 
      
      for i in range(3):
        for j in range(3):
          pom[i] += self.mat[i][j] * dr.mat[j]
      
      return tacka(pom)
  
  # Uobičajena string predstava matrice
  def __str__(self):
    return str(self.mat[0]) + '\n' \
         + str(self.mat[1]) + '\n' \
         + str(self.mat[2])

# Translacija nasleđuje geom. trans.
class trans(geom):
  def __init__(self, x=0, y=0):
    self.mat = [[1, 0, x],
                [0, 1, y],
                [0, 0, 1]]

# Skaliranje nasleđuje geom. trans.
class skal(geom):
  def __init__(self, x=1, y=1):
    self.mat = [[x, 0, 0],
                [0, y, 0],
                [0, 0, 1]]

# Smicanje nasleđuje geom. trans.
class smic(geom):
  def __init__(self, x=0, y=0):
    self.mat = [[1, x, 0],
                [y, 1, 0],
                [0, 0, 1]]

# Rotacija nasleđuje geom. trans.
class rot(geom):
  def __init__(self, u=0):
    pom1 = cos(radians(u))
    pom2 = sin(radians(u))
    
    self.mat = [[pom1, -pom2,  0],
                [pom2,  pom1,  0],
                [0,      0,    1]]

# Refleksija nasleđuje geom. trans.
class refl(geom):
  def __init__(self, u=0):
    pom1 = cos(radians(u))
    pom2 = sin(radians(u))
    
    self.mat = [[pom1,  pom2,  0],
                [pom2, -pom1,  0],
                [0,      0,    1]]

# Tačka predstavljena koordinatama
class tacka:
  def __init__(self, x=0, y=0, w=1):
    if (isinstance(x, list)):
      self.mat = x
    else:
      self.mat = [x, y, w]
  
  # Uobičajena string predstava tačke
  def __str__(self):
    return str(self.mat)

# Fja za testiranje implementiranih klasa;
# predlaže se pokretanje sa < test.txt
def test():
  print('Unosite linije koda do kraja ulaza.\n'
        'Podržano: dodela, kompozicija, štampanje.\n'
        'Transformacije: translacija, skaliranje,\n'
        'smicanje, rotacija, refleksija.\n')
  
  # Mali interpretator koji se oslanja
  # na pozivanje Pajtonovog interpretera
  while True:
    try:
      linija = input()
      exec(linija)
    except EOFError:
      print('Kraj ulaza.')
      break
    except:
      print('Pokušajte ponovo.')

if __name__ == '__main__':
  test()

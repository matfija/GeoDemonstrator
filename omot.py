#!/usr/bin/env python3

# Uključivanje modula sa operatorima
from operator import itemgetter

# Određivanje položaja prosleđene tačke
def vekt_proiz(t, u, v):
  a = (t[0]-u[0], t[1]-u[1])
  b = (v[0]-u[0], v[1]-u[1])
  
  # Vraćanje dela vektorskog proizvoda
  return a[0]*b[1] - a[1]*b[0]

# Vraćanje tačaka sa leve strane vektora
def podela(u, v, tačke):
    # return [t for t in tačke if vekt_proiz(t, u, v) < 0]
    return list(filter(lambda t: vekt_proiz(t, u, v) < 0, tačke))

# Proširivanje pretrage omotnih tačaka
def proširi(u, v, tačke):
    # Nema proširivanja prazne liste
    if not tačke:
        return []

    # Nalaženje najudaljenije tačke
    w = min(tačke, key = lambda t: vekt_proiz(t, u, v))
    
    # Podela pretrage po određenoj tački
    t1, t2 = podela(w, v, tačke), podela(u, w, tačke)
    return proširi(w, v, t1) + [w] + proširi(u, w, t2)

# Brzi algoritam za pronalazak konveksnog omotača
def konveksni_omot(tačke):
    # Prazna lista tačaka nema konveksni omot
    if not tačke:
        return []
    
    # Nalaženje dve tačke omota
    u = min(tačke, key = itemgetter(0))
    v = max(tačke, key = itemgetter(0))
    
    # Podela pretrage na levu i desnu stranu
    levo, desno = podela(u, v, tačke), podela(v, u, tačke)

    # Nalaženje omota na obe strane
    return [v] + proširi(u, v, levo) + [u] + proširi(v, u, desno)

# Fja za testiranje implementiranog algoritma
def test():
  tačke = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 0)]
  omotač = konveksni_omot(tačke)
  print(omotač)

if __name__ == '__main__':
  test()

#!/usr/bin/env python3

# Uključivanje vremenskog modula,
# kojim se proverava brzina rada
from time import time

# Uključivanje funkcionalnog modula
from functools import partial

# Uključivanje modula sa operatorima
from operator import gt, itemgetter as ig

# Uključivanje modula sa nitima
from nit import Nit

# Određivanje položaja prosleđene tačke
def vekt_proiz(t, u, v):
  a = (t[0]-u[0], t[1]-u[1])
  b = (v[0]-u[0], v[1]-u[1])
  
  # Vraćanje dela vektorskog proizvoda
  # koji ukazuje na orijentaciju tačke
  return a[0]*b[1] - a[1]*b[0]

# Vraćanje tačaka sa jedne strane vektora
def podela(u, v, tačke):
    # lambda t: partial(gt, 0)(partial(vekt_proiz, u=u, v=v)(t))
    # return list(filter(lambda t: vekt_proiz(t, u, v) < 0, tačke))
    return [t for t in tačke if vekt_proiz(t, u, v) < 0]

# Proširivanje pretrage tačaka omota
def proširi(u, v, tačke):
    # Nema proširivanja prazne liste
    if not tačke:
        return []

    # Nalaženje ekstremne tačke
    w = min(tačke, key = partial(vekt_proiz, u=u, v=v))
    
    # Niti za podelu pretrage
    nit1 = Nit(target = podela, args = (w, v, tačke))
    nit2 = Nit(target = podela, args = (u, w, tačke))
    
    # Pokretanje niti
    nit1.start()
    nit2.start()
    
    # Podela pretrage po određenoj tački
    t1, t2 = nit1.join(), nit2.join()
    
    # Niti za proširivanje pretrage
    nit1 = Nit(target = proširi, args = (w, v, t1))
    nit2 = Nit(target = proširi, args = (u, w, t2))
    
    # Pokretanje niti
    nit1.start()
    nit2.start()
    
    # Dohvatanje rezultata
    p1, p2 = nit1.join(), nit2.join()
    
    # Postavljanje određene tačke na svoje mesto
    return p1 + [w] + p2

# Brzi algoritam za pronalazak konveksnog omotača
def konveksni_omot(tačke):
    # Prazna lista tačaka nema konveksni omot
    if not tačke:
        return []
    
    # Niti za ekstremne tačke
    nit1 = Nit(target = min, args = [tačke], kwargs = {'key': ig(0)})
    nit2 = Nit(target = max, args = [tačke], kwargs = {'key': ig(0)})
    
    # Pokretanje niti
    nit1.start()
    nit2.start()
    
    # Paralelno nalaženje ekstremnih tačaka omota
    u, v = nit1.join(), nit2.join()
    
    # Niti za podelu pretrage
    nit1 = Nit(target = podela, args = (u, v, tačke))
    nit2 = Nit(target = podela, args = (v, u, tačke))
    
    # Pokretanje niti
    nit1.start()
    nit2.start()
    
    # Podela pretrage po određenim tačkama
    t1, t2 = nit1.join(), nit2.join()
    
    # Niti za proširivanje pretrage
    nit1 = Nit(target = proširi, args = (u, v, t1))
    nit2 = Nit(target = proširi, args = (v, u, t2))
    
    # Pokretanje niti
    nit1.start()
    nit2.start()
    
    # Dohvatanje rezultata
    p1, p2 = nit1.join(), nit2.join()

    # Nalaženje omota na obe strane
    return [v] + p1 + [u] + p2

# Fja za testiranje implementiranog algoritma
def test():
  # Generisanje milion tačaka
  tačke = [(i, j) for i in range(1000) for j in range(1000)]
  
  # Merenje vremena
  vreme1 = time()
  
  # Nalaženje konveksnog omotača
  omotač = konveksni_omot(tačke)
  
  # Merenje vremena
  vreme2 = time()
  
  # Ispis proteklog vremena i omota
  print('Vreme rada: {}'.format(vreme2 - vreme1))
  print(omotač)

# Poziv test funkcije ukoliko
# je modul direktno izvršen
if __name__ == '__main__':
  test()

#!/usr/bin/env python3

# Uključivanje modula za geometriju
from geom import *

# Definisanje potrebnih transformacija:
# prvo se koordinatni početak translira
# u centar platna, zatim se orijentacija
# y-ose obrne, i na kraju se, radi smanjenja
# gustine piksela, koord. sistem skalira;
# pri ovoj skali platno je dimenzija 60x40,
# te za svaku tačku važi -30<x<30, -20<y<20
t1 = trans(-204, -132)
t2 = refl() # refl(0)
t3 = skal(1/7, 1/7)

# Matrica prelaza sa platna na koord. sistem
plat_u_koord = t3 * t2 * t1
print(plat_u_koord, end = '\n\n')

# Definisanje inverznih transformacija: primena
# obrnutih transformacija obrnutim redosledom
t1 = trans(204, 132)
t2 = refl() # refl(0)
t3 = skal(7, 7)

# Matrica prelaza sa koord. sistema na platno
koord_u_plat = t1 * t2 * t3
print(koord_u_plat, end = '\n\n')

# Definisanje tačke platna
tac_plat = tacka(205, 131)
print(tac_plat, end = '\n\n')

# Prelazak u koord. sistem
tac_koord = plat_u_koord * tac_plat
print(tac_koord, end = '\n\n')

# Skaliranje u koord. sistemu
tac_skal_koord = skal(2,2) * tac_koord
print(tac_skal_koord, end = '\n\n')

# Vraćanje u platno
tac_skal_plat = koord_u_plat * tac_skal_koord
print(tac_skal_plat)

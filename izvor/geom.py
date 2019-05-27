#!/usr/bin/env python3

# Uključivanje matematičkog modula
from math import sin, cos, radians, \
                 trunc, floor, ceil

# Uključivanje funkcionalnog modula
from functools import partial, total_ordering

# Uključivanje modula sa operatorima
from operator import eq, ne

# Uključivanje modula za kopiranje
from copy import deepcopy

# Geometrijska transformacija ravni
# predstavljena homogenom 3x3 matricom
class Geom:
  # Ispitivanje da li je argument matrica
  def matrix(arg):
    if isinstance(arg, Geom):
      return deepcopy(arg.mat)
    
    # Može biti linearna matrica dimenzija 2x2
    if len(arg) is 2 and all(map(partial(eq, 2), map(len, arg))):
      return ((float(arg[0][0]), float(arg[0][1]), 0),
              (float(arg[1][0]), float(arg[1][1]), 0),
              (       0,                0,         1))
    
    # Inače mora biti objekat dimenzija 3x3
    if len(arg) is not 3 or any(map(partial(ne, 3), map(len, arg))):
      raise TypeError
    
    # I to mora biti afina matrica
    if arg[2][0] != 0 or arg[2][1] != 0 or arg[2][2] != 1:
      raise TypeError
    
    # Izdvajanje numeričkih vrednosti
    return tuple(tuple(float(arg[i][j]) for j in range(3))
                               for i in range(3))
  
  # Pomeranje transformacije u odnosu na tačku
  def pomereno(self, t, tp=None):
    if t is not None:
      # Provera da li je t tačka
      try:
        t = Tačka.point(t)
        
        # Ako jeste, tp mora niti None
        if tp is not None:
          raise TypeError
        
        # Vraćanje odgovarajuće matrice
        return Geom.matrix(Trans(t[0], t[1]) * self * Trans(-t[0], -t[1]))
      except:
        # Ako nije, onda je (t, tp) tačka
        if not isinstance(tp, (int, float)) \
         or not isinstance(t, (int, float)):
          raise TypeError
        
        # Vraćanje odgovarajuće matrice
        return Geom.matrix(Trans(t, tp) * self * Trans(-t, -tp))
    elif tp is not None:
      # Provera drugog argumenta
      return self.pomereno(tp)
    else:
      # Ako nema tačke, ništa se ne menja
      return self.mat
  
  # Opšti postupak inverzije afinih transformacijskih
  # matrica; u suštini je zasnovan na ideji o adjungovanoj
  # matrici, koja se računa preko kofaktora (determinanti
  # manjih 2x2 podmatrica), ali ovde je taj postupak
  # skraćen i direktno se vraća sračunati rezultat:
  #     |a   b   c|                        | e  -b   bf-ce|
  # T = |d   e   f|,  inv(T) = 1/(ae-bd) * |-d   a   cd-af|
  #     |0   0   1|                        | 0   0     1  |
  def inv(self, inplace = False):
    # Nije moguće 'u mestu' menjati
    # nešto što nije transformacija
    if not isinstance(self, Geom) and inplace:
      raise TypeError
    
    # Pomoćna promenljiva zarad mogućnosti
    # generičkog rada sa više tipova podataka
    pom = Geom.matrix(self)
    
    # Izvlačenje vrednosti polja matrice
    a, b, c = tuple(pom[0][i] for i in range(3))
    d, e, f = tuple(pom[1][i] for i in range(3))
    
    # Računanje nekih kofaktora
    k = 1/(a*e-b*d)
    t1 = b*f-c*e
    t2 = c*d-a*f
    
    # Formiranje inverza po izloženoj formuli
    if isinstance(self, Geom):
      matrica = ((k*e, k*-b, k*t1),
                 (k*-d, k*a, k*t2),
                 (  0,   0,    1 ))
    else:
      # Dinamičko određivanje tipova ako nije
      # prosleđena geometrijska transformacija
      matrica = type(self)((type(self[0])((k*e, k*-b, k*t1)),
                            type(self[1])((k*-d, k*a, k*t2)),
                           (type(self[2]) if len(self) is 3
                         else type(self))(( 0,    0,    1 ))))
    
    # Zamena ako je zatražena
    if inplace:
      self.mat = matrica
      return
    
    # Vraćanje rezultata
    return Geom(matrica) if isinstance(self, Geom) else matrica
  
  # Konstruktor transformacije
  def __init__(self, mat = None):
    if mat is not None:
      self.mat = Geom.matrix(mat)
    else:
      # Jedinična matrica ako nema posleđene
      #      |1   0   0|
      # ID = |0   1   0|
      #      |0   0   1|
      self.mat = tuple(tuple(1 if i is j else 0
                             for j in range(3))
                             for i in range(3))
  
  # Moguće množenje matrice skalarom
  # (to je analogno skaliranju sleva),
  # množenje dveju matrica ili, pak,
  # množenje matrice sa tačkom ravni
  def __mul__(self, dr):
    if isinstance(dr, (int, float)):
      return Geom((tuple(dr*self[0][i] for i in range(3)),
                   tuple(dr*self[1][i] for i in range(3)),
                     (0,             0,             1)))
    
    try:
      drr = Geom.matrix(dr)
      
      return Geom(tuple(tuple(sum(self[i][k] * drr[k][j] for k in range(3))
                                   for j in range(3)) for i in range(3)))
    except:
      # Pomoćna torka za homogeno množenje
      drr = Tačka.point(dr)
      
      pom = tuple(sum(self[i][j] * drr[j]
                      for j in range(3))
                      for i in range(3))
      
      # Generička konstrukcija odgovarajućeg objekta
      return type(dr)((pom[0], pom[1]))
  
  # Moguće množenje skalarom
  # ili drugom matricom zdesna
  def __rmul__(self, dr):
    if isinstance(dr, (int, float)):
      return self * dr
    
    drr = Geom.matrix(dr)
    
    return Geom(tuple(tuple(sum(self[i][k] * drr[k][j] for k in range(3))
                                 for j in range(3)) for i in range(3)))
  
  # Logaritamsko stepenovanje matrice
  def __pow__(self, dr):
    if not isinstance(dr, int):
      raise TypeError
    elif dr < 0:
      return pow(self.inv(), -dr)
    elif dr is 0:
      return Geom()
    elif dr is 1:
      return Geom(self.mat)
    elif dr%2 is 0:
      return pow(self*self, dr//2)
    else:
      return self*pow(self*self, (dr-1)//2)

  # Magični metod za jednakost
  def __eq__(self, dr):
    if isinstance(dr, Geom):
      return eval(repr(self)).mat == eval(repr(dr)).mat
    else:
      raise TypeError
  
  # Magični metod za dohvatanje elementa
  def __getitem__(self, indeks):
    return self.mat[indeks]
  
  # Magični metod za iteraciju
  def __iter__(self):
    return iter(self.mat)
  
  # Uobičajena string predstava matrice
  def __str__(self):
    return 'Transformacija:\n[(%.2f, %.2f, %.2f)\n' \
           ' (%.2f, %.2f, %.2f)\n (%.2f, %.2f, %.2f)]' \
           % tuple(self[i][j] for i in range(3) for j in range(3))
  
  # Uprošćena reprezentacija objekta u kodu;
  # zadaje se osam cifara kao bitno
  def __repr__(self):
    return 'Geom(((%.8f, %.8f, %.8f),' \
                 '(%.8f, %.8f, %.8f),' \
                 '(%.8f, %.8f, %.8f)))' \
           % tuple(self[i][j] for i in range(3)
                              for j in range(3))

# Translacija nasleđuje geom. trans.
class Trans(Geom):
  def __init__(self, x=0, y=0, inv=False):
    if not isinstance(x, (int, float)):
      x, y, _ = Tačka.point(x)
    elif not isinstance(y, (int, float)):
      raise TypeError
    
    # Inverzna je aditivni inverz:
    #     |1   0   x|            |1   0  -x|
    # T = |0   1   y|,  inv(T) = |0   1  -y|
    #     |0   0   1|            |0   0   1|
    if inv: x, y = -x, -y
    
    # Matrica translacije u ravni
    self.mat = ((1, 0, x),
                (0, 1, y),
                (0, 0, 1))

# Skaliranje nasleđuje geom. trans.
class Skal(Geom):
  def __init__(self, x=1, y=1, t=None, tp=None, inv=False):
    if not isinstance(x, (int, float)):
      x, y, _ = Tačka.point(x)
    elif not isinstance(y, (int, float)):
      raise TypeError
    
    # Inverzna je multiplikativni inverz:
    #     |x   0   0|            |1/x  0   0|
    # T = |0   y   0|,  inv(T) = | 0  1/y  0|
    #     |0   0   1|            | 0   0   1|
    if inv: x, y = 1/x, 1/y
    
    # Matrica istezanja u ravni
    self.mat = ((x, 0, 0),
                (0, y, 0),
                (0, 0, 1))
    
    # Eventualno centriranje transformacije
    self.mat = self.pomereno(t, tp)

# Smicanje nasleđuje geom. trans.
class Smic(Geom):
  def __init__(self, x=0, y=0, t=None, tp=None, inv=False):
    if not isinstance(x, (int, float)):
      x, y, _ = Tačka.point(x)
    elif not isinstance(y, (int, float)):
      raise TypeError
    
    # Inverzna je aditivni inverz, ali
    # skaliran za korektivni faktor:
    #     |1   x   0|                       | 1  -x   0|
    # T = |y   1   0|,  inv(T) = 1/(1-xy) * |-y   1   0|
    #     |0   0   1|                       | 0   0   1|
    # Alternativno, moguće bi bilo primeniti
    # transformaciju bez korektivnog faktora,
    # ali je u tom slučaju neophodno popraviti
    # matricu, što se u kodu može učiniti npr.:
    # if inv and x != 0 and y != 0:
    #   self.mat = Geom.matrix(Skal(1-x*y, 1-x*y, inv=True) * \
    #              Trans(t1*x*y, t2*x*y, inv=True) * self.mat)
    f = 1
    if inv:
      f = 1/(1-x*y)
      x, y = -x, -y
    
    # Matrica smicanja u ravni
    self.mat = (( f,  f*x, 0),
                (f*y,  f,  0),
                ( 0,   0,  1))
    
    # Eventualno centriranje transformacije
    self.mat = self.pomereno(t, tp)

# Rotacija nasleđuje geom. trans.
class Rot(Geom):
  def __init__(self, u=0, t=None, tp=None, inv=False):
    if not isinstance(u, (int, float)):
      raise TypeError
    
    # Inverzna je aditivni inverz:
    #     |cos(u)  -sin(u)   0|            | cos(u)   sin(u)   0|
    # T = |sin(u)   cos(u)   0|,  inv(T) = |-sin(u)   cos(u)   0|
    #     |  0        0      1|            |   0        0      1|
    if inv: u = -u
    
    # Koeficijenti rotacije u ravni
    pom1 = cos(radians(u))
    pom2 = sin(radians(u))
    
    # Matrica rotacije u ravni
    self.mat = ((pom1, -pom2,  0),
                (pom2,  pom1,  0),
                (0,      0,    1))
    
    # Eventualno centriranje transformacije
    self.mat = self.pomereno(t, tp)

# Refleksija nasleđuje geom. trans.
class Refl(Geom):
  def __init__(self, u=0, t=None, tp=None, inv=False):
    if not isinstance(u, (int, float)):
      raise TypeError
    
    # Svaka refleksija je samoj sebi inverzna:
    #     |cos(2u)   sin(2u)   0|
    # T = |sin(2u)  -cos(2u)   0|,  inv(T) = T
    #     |  0         0       1|
    if inv: pass
    
    # Koeficijenti refleksije u ravni
    pom1 = cos(radians(2*u))
    pom2 = sin(radians(2*u))
    
    # Matrica refleksije u ravni
    self.mat = ((pom1,  pom2,  0),
                (pom2, -pom1,  0),
                (0,      0,    1))
    
    # Eventualno centriranje transformacije
    self.mat = self.pomereno(t, tp)

# Tačka predstavljena koordinatama; funkcionalno
# dekorisana tako da podržava totalno uređenje
@total_ordering
class Tačka:
  # Ispitivanje da li je argument tačka
  def point(arg):
    if isinstance(arg, Tačka):
      return deepcopy(arg.mat)
    
    # Sve vrednosti moraju biti numeričke
    dr = tuple(map(float, arg))
    
    # Dalje razmatranje po dužini argumenta
    if len(dr) is 2:
      return (dr[0], dr[1], 1)
    elif len(dr) is 3:
      return (dr[0]/dr[2], dr[1]/dr[2], 1)
    else:
      raise TypeError
  
  # Konsktruktor tačke; podrazumevana je
  # vrednost KP = (0, 0, 1) tj. (0, 0);
  # nisu podržane beskonačno udaljene tačke
  # proširene afine ravni tipa (x, y, 0)
  def __init__(self, x=0, y=0, w=1):
    if  isinstance(x, (int, float)) \
    and isinstance(y, (int, float)) \
    and isinstance(w, (int, float)):
      self.mat = (x/w, y/w, 1)
    elif y == 0 and w == 1:
      self.mat = Tačka.point(x)
    else:
      raise TypeError
  
  # Uobičajeno sabiranje dve tačke ili
  # tačke sa skalarom (vektorizacija)
  def __add__(self, dr):
    if isinstance(dr, (int, float)):
      return Tačka(self[i]+dr for i in range(2))
    else:
      drr = Tačka.point(dr)
      return Tačka(self[i]+drr[i] for i in range(2))
  
  # Uobičajeno oduzimanje dve tačke ili
  # skalara od tačke (vektorizacija)
  def __sub__(self, dr):
    if isinstance(dr, (int, float)):
      return Tačka(self[i]-dr for i in range(2))
    else:
      drr = Tačka.point(dr)
      return Tačka(self[i]-drr[i] for i in range(2))
  
  # Uobičajeno množenje tačke skalarom
  def __mul__(self, dr):
    drr = float(dr)
    return Tačka(drr*self[i] for i in range(2))
  
  # Analogno sabiranje zdesna
  def __radd__(self, dr):
    return self + dr
  
  # Analogno oduzimanje zdesna
  def __rsub__(self, dr):
    return -self + dr
  
  # Analogno množenje zdesna ili
  # množenje tačke matricom
  def __rmul__(self, dr):
    try:
      return self * dr
    except:
      return Geom(dr) * self
  
  # Deljenje tačke skalarom
  def __truediv__(self, dr):
    return Tačka(self[i]/dr for i in range(2))
  
  # Celobrojno deljenje tačke skalarom
  def __floordiv__(self, dr):
    return Tačka(self[i]//dr for i in range(2))
  
  # Ostatak pri deljenju tačke skalarom
  def __mod__(self, dr):
    return Tačka(self[i]%dr for i in range(2))
  
  # Celobrojno deljenje sa ostatkom
  def __divmod__(self, dr):
    return self//dr, self%dr
  
  # Negacija tačke
  def __neg__(self):
    return Tačka(-self[i] for i in range(2))
  
  # Pozitivna tačka
  def __pos__(self):
    return Tačka(+self[i] for i in range(2))
    
  # Apsolutna tačka
  def __abs__(self):
    return Tačka(abs(self[i]) for i in range(2))
  
  # Zaokrugljena tačka
  def __round__(self, cifre=0):
    return Tačka(round(self[i], cifre) for i in range(2))
  
  # Odsečena tačka
  def __trunc__(self):
    return Tačka(trunc(self[i]) for i in range(2))
  
  # Zaokrugljivanje naniže
  def __floor__(self):
    return Tačka(floor(self[i]) for i in range(2))
    
  # Zaokrugljivanje naviše
  def __ceil__(self):
    return Tačka(ceil(self[i]) for i in range(2))
    
  # Magični metod za jednakost
  def __eq__(self, dr):
    if isinstance(dr, Tačka):
      return eval(repr(self)).mat == eval(repr(dr)).mat
    else:
      raise TypeError
  
  # Magični metod za poređenje
  def __lt__(self, dr):
    if isinstance(dr, Tačka):
      return eval(repr(self)).mat < eval(repr(dr)).mat
    else:
      raise TypeError
  
  # Magični metod za dohvatanje elementa
  def __getitem__(self, indeks):
    return self.mat[indeks]
  
  # Magični metod za iteraciju
  def __iter__(self):
    return iter(self.mat)
  
  # Uobičajena string predstava tačke
  def __str__(self):
    return 'Tačka:\n[(%.2f, %.2f)]' \
           % tuple(self[i] for i in range(2))
  
  # Uprošćena reprezentacija objekta u kodu;
  # zadaje se osam cifara kao bitno
  def __repr__(self):
    return 'Tačka(%.8f, %.8f)' \
           % tuple(self[i] for i in range(2))

# Fja za testiranje implementiranih klasa;
# predlaže se pokretanje sa < test.py, gde
# se nalaze transformacije bitne za rad
def test():
  print('Unosite linije koda do kraja ulaza.\n'
        'Podržano: dodela, kompozicija, stepenovanje,\n'
        'štampanje, aritmetika i logika sa tačkama...\n'
        'Transformacije: translacija, skaliranje,\n'
        'smicanje, rotacija, refleksija.\n')
  
  # Mali interpretator koji se oslanja
  # na pozivanje Pajtonovog interpretera;
  # u pitanju je poznata RE(P)L petlja
  # iz koje se izlazi EOF-om (CTRL+D)
  while True:
    try:
      exec(input())
    except EOFError:
      print('Kraj ulaza.')
      break
    except:
      print('Pokušajte ponovo.')

# Poziv test funkcije ukoliko
# je modul direktno izvršen
if __name__ == '__main__':
  test()

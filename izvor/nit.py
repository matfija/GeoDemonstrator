#!/usr/bin/env python3

# Uključivanje modula sa nitima
from threading import Thread

# Uključivanje modula sa
# pseudoslučajnim brojevima
from random import randrange

# Uključivanje modula za inspekciju
from inspect import getmembers, isfunction

# Uključivanje dodatnog modula za
# reflektivno i metaprogramiranje
from types import FunctionType

# Klasa koja predstavlja nit sa povratnom vrednosti;
# imena su ista kao za Thread, kako bi se isto ponašali;
# pri nalaženju konveknog omotača, ubrzava rad sa velikim
# brojem tačaka u višeprocesorskom okruženju
class StaraNit(Thread):
  # Konstruktor izvedene klase
  def __init__(self, group = None, target = None, name = None,
                 args = (), kwargs = {}, Verbose = False):
    # Pozivanje konstruktora natklase
    Thread.__init__(self, group, target, name, args, kwargs)
    
    # Čuvanje podatka o 'pričljivosti'
    self.Verbose = Verbose
    
    # Podrazumevano ne postoji povratna vrednost
    self.rezultat = None
  
  # Prevazilaženje metoda za pokretanje niti
  def run(self):
    # Ukoliko postoji fja, rezultat je ono što vraća
    if self._target is not None:
      self.rezultat = self._target(*self._args, **self._kwargs)
  
  # Prevazilaženje metoda za čekanje niti
  def join(self, *args):
    # Dočekivanje iz natklase
    Thread.join(self, *args)
    
    # Vraćanje sačuvanog rezultata
    return self.rezultat

# Pravljenje metaklase prosleđivanjem odgovarajućih
# argumenata konstruktoru metaklase (to je klasa koja
# instancira klase, a ne objekte u užem smislu) type:
# ime klase, torka baznih klasa, rečnik klase
MetaNit = type('MetaNit', tuple([type]), {})

# Definisanje metoda koji se poziva prilikom pravljenja
# objekata klasâ čija je metaklasa MetaNit
def poziv(self, *args, **kwargs):
  # Pravljenje podrazumevanog objekta
  objekat = type.__call__(self, *args, **kwargs)
  
  # Ispisivanje podatka o 'pričljivosti'
  if objekat.Verbose:
    print('Instanciran pričljiv objekat metaklase MetaNit!')
  
  # Vraćanje napravljenog objekta
  return objekat

# Vezivanje definisanog metoda za metaklasu
MetaNit.__call__ = poziv

# Pravljenje klase Nit kao klase čija je
# metaklasa MetaNit, a natklasa Thread
Nit = MetaNit('Nit', tuple([Thread]), {})

# Postavljanje lambda metoda za stringovnu predstavu
Nit.__str__ = lambda self: 'Nit za {} nad {}' \
          .format(self._target.__name__, self._args)

# Vezivanje metoda napravljene klase
# za one napisane za klasu StaraNit
Nit.__init__ = StaraNit.__init__
# Nit.run = StaraNit.run
# Nit.join = StaraNit.join

# Ostalo se dodaje pomoću inspekcije
for metod in getmembers(StaraNit, isfunction):
  if not metod[0].startswith('_'):
    # Izdvajanje metoda
    met = getattr(StaraNit, metod[0])
    
    # Pravljenje duboke kopije metoda
    fja = FunctionType(met.__code__, met.__globals__,
    met.__name__, met.__defaults__, met.__closure__)
    
    # Dodeljivanje napravljenog metoda
    exec('Nit.{} = fja'.format(metod[0]))

# Fja za testiranje implementirane klase
def test():
  # Generisanje deset brojeva
  brojevi = [randrange(1, 11) for i in range(10)]
  
  # Inicijalizacija niza niti
  niti = []
  
  # Definisanje niti koje sa jednakom verovatnoćom
  # traže minimim ili maksimum generisanog niza
  for i in range(3):
    niti.append(Nit(args = brojevi, target = min if randrange(2)
                          == 0 else max, Verbose = True))
  
  # Pokretanje niti
  for i in range(3):
    niti[i].start()
    print(niti[i])
  
  # Dohvatanje rezultata
  for i in range(3):
    rez = niti[i].join()
    print('{} je {}.'.format('Minimum' if niti[i]._target ==
                               min else 'Maksimum', rez))

# Poziv test funkcije ukoliko
# je modul direktno izvršen
if __name__ == '__main__':
  test()

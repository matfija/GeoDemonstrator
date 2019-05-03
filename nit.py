# Uključivanje modula sa nitima
from threading import Thread

# Uključivanje modula sa
# pseudoslučajnim brojevima
from random import randrange

# Klasa koja predstavlja nit sa povratnom vrednosti;
# imena su ista kao za Thread, kako bi se isto ponašali;
# pri nalaženju konveknog omotača, ubrzava rad sa velikim
# brojem tačaka u višeprocesorskom okruženju
class Nit(Thread):
  # Konstruktor izvedene klase
  def __init__(self, group = None, target = None, name = None,
                 args = (), kwargs = {}, Verbose = None):
    # Pozivanje konstruktora natklase
    super(Nit, self).__init__(group, target, name, args, kwargs)
    
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
    super(Nit, self).join(*args)
    
    # Vraćanje sačuvanog rezultata
    return self.rezultat

# Fja za testiranje implementirane klase
def test():
  # Generisanje deset brojeva
  brojevi = [randrange(1, 11) for i in range(10)]
  
  # Inicijalizacija niza niti
  niti = []
  
  # Definisanje niti koje sa jednakom verovatnoćom
  # traže minimim ili maksimum generisanog niza
  for i in range(10):
    niti.append(Nit(args = brojevi, target = min
                if randrange(2) == 0 else max))
  
  # Pokretanje niti
  for i in range(10):
    niti[i].start()
  
  # Dohvatanje rezultata
  for i in range(10):
    rez = niti[i].join()
    print('{} je {}.'.format('Minimum' if niti[i]._target ==
                               min else 'Maksimum', rez))

# Poziv test funkcije ukoliko
# je modul direktno izvršen
if __name__ == '__main__':
  test()

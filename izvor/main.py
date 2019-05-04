#!/usr/bin/env python3

# Uključivanje modula za GKI
from gki import GeoDemonstrator

# Glavna (main) fja
def main():
  # Instanciranje objekta stožerne klase
  aplikacija = GeoDemonstrator()
  
  # Pokretanje glavne petlje programa
  aplikacija.mainloop()

# Ispitivanje globalne promenljive koja sadrži
# ime programa kako bi se znalo da li je pravilno
# pokrenut, a ne npr. samo importovan ili uzet
# kao ulaz programu koji interpretira kod
if __name__ == '__main__':
  main()

#!/usr/bin/env python3

# Ukljucivanje modula za GKI
import gki

# Glavna (main) fja
def main():
  # Instanciranje stozerne klase
  aplikacija = gki.GeoDemonstrator()
  
  # Pokretanje glavne petlje programa
  aplikacija.mainloop()

# Ispitivanje globalne promenljive koja sadrzi
# ime programa kako bi se znalo da li je pravilno
# pokrenut, a ne npr. samo importovan
if __name__ == '__main__':
  main()


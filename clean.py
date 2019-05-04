#!/usr/bin/env python3

# Uključivanje modula za
# rad sa fajl sistemom
from os import system

# Čišćenje repozitorijuma od nepoželjnih
# datoteka; pajtonična zamena za gitignore
system('rm -rf '              # rekurzivno prinudno brisanje
       '*~ '                  # svih keš fajlova u direktorijumu
       'izvor/*~ '            # svih keš fajlova u izvoru
       'izvor/__pycache__ '   # keš foldera nastalog od biblioteka
       'slike/*~')            # svih keš fajlova u slikama

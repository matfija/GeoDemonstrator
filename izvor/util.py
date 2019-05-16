#!/usr/bin/env python3

# Uključivanje sistemskog modula, kao i
# modula za rad sa datotečnim sistemom
from sys import exit as greška
from os.path import join as put

# Uključivanje grafičkog modula
from tkinter import PhotoImage

# Uključivanje pomoćnog modula za
# kutijice sa iskačućim porukama
from tkinter.messagebox import showinfo, showerror, askyesno

# Uključivanje funkcionalnog modula
from functools import partial

# Uključivanje modula sa operatorima
from operator import mul

# Uključivanje modula za nalazak konveksnog omotača
from omot import konveksni_omot

# Mixin klasa služi da razdvoji funkcionalnosti
# jedne klase na više delova, čime je poboljšana
# modularnost i čitljivost koda; nema konstruktor
# i sadrži isključivo pomoćne tj. dodatne metode
class GeoMixinHelp():
  # Funkcija za korektno učitavanje slike
  def učitaj_sliku(self, ime):
    # Pokušaj dohvatanja slike na očekivanom mestu
    try:
      return PhotoImage(file = put('..', 'slike', ime))
    
    # U suprotnom pokušaj dohvatanja iz specijalnog
    # puta u kojem PyInstaller smešta privremene fajlove
    # u toku izvršavanja 'zamrznutih' programa
    except:
      # Uključivanje privremenih modula
      import sys, os.path
      
      # Dohvatanje slike sa izračunate lokacije,
      # te specijalne ili radnog direktorijuma ako
      # ova prva ne postoji na pokrenutom sistemu
      slika = PhotoImage(file = put(getattr(sys, '_MEIPASS',
                                            os.path.dirname
                                           (os.path.abspath
                                          (__file__))), ime))
      
      # Brisanje privremenih modula
      del sys, os.path
      
      # Vraćanje generisane slike
      return slika
  
  # Dodavanje pritisnute tačke
  def dodaj_tačku(self, dog):
    # Ukoliko je u toku unos tačaka
    if self.unos:
      # Dodavanje pritisnute tačke
      tačka = (dog.x, dog.y)
      self.tačke.append(tačka)
      
      # Čuvanje i u koordinatnom sistemu
      ttačka = self.puk * tačka
      self.ttačke.append(ttačka)
      
      # Log poruka o akciji
      print('Dodata tačka (%.2f, %.2f) klikom na platno.' % ttačka)
      
      # Iscrtavanje figure
      self.nacrtaj_figuru()
      
      # Kontrola pristupa
      self.baricentar()
  
  # Promena teksta u zavisnosti od toga
  # da li je unos tačaka u toku ili ne
  def promena_unosa(self, dog = None):
    if self.unos:
      # Ne zaključuje se prazan unos
      if not self.tačke:
        showerror('Greška', 'Unesite tačke na platno!')
        return
      
      self.okvir_d.config(text = 'Transformišite figuru po želji')
      self.umeni.entryconfig(1, label = 'Ponovi unos')
      
      # Promena stanja unosa i crtanje formiranog mnogougla
      self.unos = False
      self.nacrtaj_figuru()
      
      # Log poruka o akciji
      print('Zaključen unos tačaka na zahtev korisnika.')
    else:
      self.okvir_d.config(text = 'Unosite tačke klikovima po platnu')
      self.umeni.entryconfig(1, label = 'Zaključi unos')
      
      # Brisanje platna i reinicijalizacija liste tačaka
      self.novo_platno()
      
      # Promena stanja unosa
      self.unos = True
      
      # Log poruka o akciji
      print('Ponovljen unos tačaka na zahtev korisnika.')
  
  # Ispravljanje iscrtane figure
  def ispravi(self, dog = None):
    # Ne ispravljaju se prazne figure
    if not self.tačke:
      showerror('Greška', 'Unesite tačke na platno!')
      return
    
    # Ne ispravlja se pre kraja unosa
    if self.unos:
      showerror('Greška', 'Prvo zaključite unos tačaka!')
      return
    
    # Zamena liste tačaka konveksnim omotom
    self.tačke = konveksni_omot(self.tačke)
    self.ttačke = list(map(partial(mul, self.puk), self.tačke))
    
    # Crtanje ispravljene figure
    self.nacrtaj_figuru()
    
    # Eventualno upisivanje nekih
    # vrednosti u slobodna polja
    self.baricentar()
    
    # Log poruka o akciji
    print('Ispravljena figura na zahtev korisnika.')
  
  # Reinicijalizacija platna
  def novo_platno(self, ind=False):
    self.obriši_platno()
    self.tačke = []
    self.ttačke = []
    self.id_tač = []
    self.baricentar()
    
    # Ukoliko je pozivalac dugme
    if ind:
      print('Obrisano platno na zahtev korisnika.')
      
      # Ponavljanje unosa ako nije u toku
      if not self.unos:
        self.promena_unosa()
  
  # Brisanje platna; ne može sa kratkim
  # self.platno.delete('all') jer se njime
  # briše i slika koordinatnog sistema
  def obriši_platno(self):
    # Brisanje prethodno nacrtane figure
    self.platno.delete(self.figura)
    
    # Brisanje prethodno nacrtanih tačaka
    list(map(self.platno.delete, self.id_tač))
  
  # Crtanje potrebne figure
  def nacrtaj_figuru(self):
    # Brisanje platna
    self.obriši_platno()
    
    # Iscrtavanje trenutnih tačaka i
    # čuvanje njihovih identifikatora
    self.id_tač = [self.platno.create_oval
              (t[0]-2, t[1]-2, t[0]+2, t[1]+2,
              outline = 'blue', fill = 'blue')
                    for t in self.tačke]
    
    # Ukoliko je unos u toku, crtanje nove linije
    if self.unos:
      self.figura = self.platno.create_line(self.tačke) \
                     if len(self.tačke) > 1 else None
    else:
      # Inače iscrtavanje mnogougla ukoliko su tačke učitane
      self.figura = self.platno.create_polygon(self.tačke, outline
         = 'black', fill = '') if len(self.tačke) > 1 else None
  
  # Prikazivanje prozora za pomoć
  def pomoć(self, dog = None):
    # Log poruka o akciji
    print('Ispisana upustva za upotrebu.')
    
    # Prikazivanje uputstava
    showinfo('Pomoć',
             'Na prikazanom prozoru nalaze se meni, platno i polja za'
             ' odabir i unos. Levim klikom unosite tačke po platnu,'
             ' nakon čega možete zaključiti unos (desni klik'
             ' ili opcije iz menija), ispraviti figuru nalaženjem'
             ' konveksnog omota (srednji klik ili opcije) i odabrati'
             ' transformaciju iz padajućeg menija, kao i njene parametre.\n\n'
             'Sledi tumačenje svake transformacije i njenih parametara:\n'
             '\u2022 translacija – (pravo)linijsko kretanje'
             ' u pravcu vektora (x, y),\n'
             '\u2022 skaliranje – istezanje zraka iz tačke (t1, t2) za'
             ' faktore x i y,\n'
             '\u2022 smicanje – klizanje usled pritiska pod uglovima'
             ' -arctg(x) i arctg(y) u odnosu na ose koordinatnog sistema'
             ' sa centrom u (t1, t2),\n'
             '\u2022 rotacija – kružno kretanje za ugao \u03b8'
             ' oko tačke (t1, t2),\n'
             '\u2022 refleksija – ogledalsko obrtanje u odnosu na pravu koja'
             ' zaklapa ugao \u03b8 sa x osom i sadrži tačku (t1, t2).')
  
  # Prikazivanje glavnih informacija o aplikaciji
  def info(self, dog = None):
    # Log poruka o akciji
    print('Ispisane informacije o programu.')
    
    # Prikazivanje glavnih informacija
    showinfo('Informacije',
             'GeoDemonstrator, seminarski iz Programskih paradigmi.\n\n'
             'Korisnik zadaje figuru u dvodimenzionom okruženju, nad'
             ' kojom zatim vrši proizvoljne afine geometrijske'
             ' transformacije: translaciju, rotaciju, refleksiju,'
             ' skaliranje, smicanje.\n\n'
             'Ideja je omogućiti jednostavno interaktivno prikazivanje i lakše'
             ' razumevanje materije koja se obrađuje na časovima Geometrije'
             ' za I smer, kao i Računarske grafike.\n\n'
             'Autori (tim KriLa):\n'
             'Kristina Pantelić, 91/2016,\n'
             'Lazar Vasović, 99/2016.\n\n'
             'Matematički fakultet, 2019')
  
  # Zatvaranje aplikacije na zahtev korisnika
  def kraj(self, dog = None):
    # Poruka korisniku o kraju programa
    if askyesno('Kraj programa',
       'Da li stvarno želite da napustite program?'):
      
      # Log poruka o zatvaranju aplikacije
      print('GeoDemonstrator zatvoren na zahtev korisnika!')
      
      # Upotreba self.quit() zamrzava prozor na Windows-u,
      # pošto prekida izvršavanje i pokretačkog programa
      self.destroy()

# Obaveštenje o grešci ukoliko je modul
# pokrenut kao samostalan program
if __name__ == '__main__':
  greška('Mixin nije samostalan program! Pokrenite main!')

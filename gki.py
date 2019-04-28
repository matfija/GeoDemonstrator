# Uključivanje sistemskog i grafičkog modula
import sys, tkinter

# Uključivanje pomoćnog modula za kutijice sa porukama
from tkinter import messagebox

# Nosilac programa je klasa GeoDemonstrator, koja
# nasleđuje grafičku klasu Tk iz modula tkinter
class GeoDemonstrator(tkinter.Tk):
  # Konstruktor aplikacije
  def __init__(self):
    # Pozivanje konstruktora roditeljske klase
    super(GeoDemonstrator, self).__init__()
    
    # Postavljanje naziva aplikacije
    self.title('GeoDemonstrator')
    
    # Inicijalizacija liste tačaka
    self.tačke = []
    
    # Inicijalizacija elemenata GKI
    self.inicijalizacija()
  
  # Inicijalizacija elemenata GKI
  def inicijalizacija(self):
    # Postavljanje veličine i pozicije prozora
    self.geometry('450x450+75+75')
    
    # Onemogućavanje promene veličine prozora,
    # pošto je Tk prilično plastičan, pa promene
    # ugrožavaju zamišljeni izgled aplikacije
    self.resizable(False, False)
    
    # Postavljanje glavnog menija i vezivanje
    # komandi za odgovarajuće funkcionalnosti
    meni = tkinter.Menu(self)
    meni.add_command(label = 'Info (F1)', command = self.info)
    meni.add_command(label = 'Kraj (Esc)', command = self.kraj)
    self.config(menu = meni)
    
    # Vezivanje tipki za akcije analogne
    # onima iz prethodno postavljenog menija
    self.bind('<F1>', self.info)
    self.bind('<Escape>', self.kraj)
    
    # Pravljenje okvira za platno
    okvir_p = tkinter.LabelFrame(self, text = 'Zakoračite u svet geometrijskih'
                                       ' transformacija', padx = 10, pady = 10)
    okvir_p.place(x = 10, y = 10,
                  height = 300, width = 430)
    
    # Postavljanje platna unutar okvira
    self.platno = tkinter.Canvas(okvir_p, bg = 'grey',
                                 height = 260, width = 405)
    self.platno.place(x = 0, y = 0)
    
    # Vezivanje čuvanja tačke za klik na platno
    self.unos = True
    self.platno.bind("<Button-1>", lambda e: self.tačke.append((e.x, e.y))
                                             if self.unos else None)
    
    # Pravljenje okvira za dugmad
    self.okvir_d = tkinter.LabelFrame(self, text = 'Unosite tačke klikovima'
                                      ' po platnu', padx = 10, pady = 10)
    self.okvir_d.place(x = 10, y = 315,
                       height = 120, width = 430)
    
    # Postavljanje dugmeta za kontrolu unosa
    self.dugme_u = tkinter.Button(self.okvir_d, text = 'Zaključi unos',
                                  command = self.promena_unosa)
    self.dugme_u.place(x = 0, y = 0)
    
    # Postavljanje dugmeta za sortiranje tačaka
    self.dugme_s = tkinter.Button(self.okvir_d, text = 'Ispravi figuru',
                                  command = lambda: self.tačke.sort())
    self.dugme_s.place(x = 0, y = 40)
  
  # Promena teksta u zavisnosti od toga
  # da li je unos tačaka u toku ili ne
  def promena_unosa(self):
    if self.unos:
      self.okvir_d.config(text = 'Transformišite figuru pomoću dugmadi')
      self.dugme_u.config(text = 'Ponovi unos')
      
      # Iscrtavanje mnogougla ukoliko su
      # tačke uspešno učitane tj. neprazne
      self.mnogougao = self.platno.create_polygon(self.tačke,
           outline = 'black', fill = '') if self.tačke else None
    else:
      self.okvir_d.config(text = 'Unosite tačke klikovima po platnu')
      self.dugme_u.config(text = 'Zaključi unos')
      
      # Brisanje platna i reinicijalizacija liste tačaka
      self.platno.delete(self.mnogougao)
      self.tačke = []
    
    # Promena stanja unosa
    self.unos = not self.unos
  
  # Prikazivanje glavnih informacija o aplikaciji;
  # *args je neophodan kako bi se prosledili dodatni
  # podaci o događaju tastature, slično kao što fje
  # događaja u GLUT-u obavezno primaju koordinate
  def info(self, *args):
    messagebox.showinfo('Informacije',
               'GeoDemonstrator, seminarski iz Programskih paradigmi.\n\n'
               'Zamisao je da korisnik zada mnogougao u dvodimenzionom'
               ' okruženju, nad kojim zatim vrši proizvoljne afine geometrijske'
               ' tranformacije: translaciju, rotaciju, refleksiju, skaliranje,'
               ' smicanje.\n\n'
               'Ideja je omogućiti jednostavno interaktivno prikazivanje i lakše'
               ' razumevanje materije koja se obrađuje na časovima Geometrije'
               ' za I smer, kao i Računarske grafike.\n\n'
               'Autori (tim KriLa):\n'
               'Kristina Pantelić, 91/2016,\n'
               'Lazar Vasović, 99/2016.\n\n'
               'Matematički fakultet, 2019.')
  
  # Zatvaranje aplikacije na zahtev korisnika
  def kraj(self, *args):
    print('GeoDemonstrator zatvoren na zahtev korisnika!')
    self.quit()

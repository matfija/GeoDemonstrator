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


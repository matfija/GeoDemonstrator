#!/usr/bin/env python3

# Uključivanje sistemskog modula, kao i
# modula za rad sa datotečnim sistemom
from sys import exit as greška
from os.path import join as put

# Uključivanje grafičkog modula
from tkinter import *
from tkinter import messagebox

#Tk, Menu, LabelFrame, Canvas, \
#                   PhotoImage, Button, messagebox, \
#                    Label, StringVar, OptionMenu

# Uključivanje modula za nalazak konveksnog omotača
from omot import konveksni_omot

# Uključivanje funkcionalnog modula
from functools import partial

# Uključivanje modula sa operatorima
from operator import mul

# Uključivanje geometrijskog modula
from geom import *

# Nosilac programa je klasa GeoDemonstrator, koja
# nasleđuje grafičku klasu Tk iz modula tkinter
class GeoDemonstrator(Tk):
  # Konstruktor aplikacije
  def __init__(self):
    # Log poruka o pokretanju aplikacije
    print('Dobro došli u aplikaciju GeoDemonstrator!')
    
    # Pozivanje konstruktora roditeljske klase
    super().__init__()
    
    # Postavljanje naziva aplikacije
    self.title('GeoDemonstrator')
    
    # Inicijalizacija liste tačaka
    self.tačke = []
    self.ttačke = []
    
    # Inicijalizacija liste identifikatora
    # na platnu trenutno iscrtanih tačaka
    self.id_tač = []
    
    # Inicijalizacija figure
    self.figura = None
    
    # Inicijalizacija transformacija iz platna
    # u iscrtani koordinatni sistem i obrnuto
    self.puk = Skal(1/7, -1/7) * Trans(-204, -132)
    self.kup = Trans(204, 132) * Skal(7, -7)
    
    # Inicijalizacija elemenata GKI
    self.init_gki()
  
  # Inicijalizacija elemenata GKI
  def init_gki(self):
    # Postavljanje veličine i pozicije prozora
    self.geometry('450x450+75+75')
    
    # Onemogućavanje promene veličine prozora,
    # pošto je Tk prilično plastičan, pa promene
    # ugrožavaju zamišljeni izgled aplikacije
    self.resizable(False, False)
    
    # Inicijalizacija glavnog menija
    self.init_meni()
    
    # Inicijalizacija platna
    self.init_platno()
    
    # Kontrola unosa tačaka
    self.init_unos()
  
  # Inicijalizacija glavnog menija
  def init_meni(self):
    # Postavljanje glavnog menija i vezivanje
    # komandi za odgovarajuće funkcionalnosti
    meni = Menu(self)
    meni.add_command(label = 'Info (F1)', command = self.info)
    meni.add_command(label = 'Kraj (Esc)', command = self.kraj)
    self.config(menu = meni)
    
    # Vezivanje tipki za akcije analogne
    # onima iz prethodno postavljenog menija
    self.bind('<F1>', self.info)
    self.bind('<Escape>', self.kraj)
    
    # Vezivanje protokola zatvaranja prozora
    # za istu akciju kao za Kraj i Escape
    self.protocol('WM_DELETE_WINDOW', self.kraj)
  
  # Inicijalizacija platna
  def init_platno(self):
    # Pravljenje okvira za platno
    okvir_p = LabelFrame(self, text = 'Zakoračite u svet geometrijskih'
                           ' transformacija', padx = 10, pady = 10)
    okvir_p.place(x = 10, y = 10,
                  height = 300, width = 430)
    
    # Postavljanje platna unutar okvira
    self.platno = Canvas(okvir_p, height = 261, width = 405)
    self.platno.place(x = 0, y = 0)
    
    # Postavljanje koordinatnog sistema na platno;
    # slika nije lokalna promenljiva, pošto bi je u
    # tom slučaju 'pojeo' sakupljač otpadaka
    self.slika = PhotoImage(file = put('..', 'slike', 'koord.gif'))
    self.platno.create_image(203, 131, image = self.slika)

    # Vezivanje čuvanja tačke za klik na platno
    self.unos = True
    self.platno.bind('<Button-1>', self.dodaj_tačku)
  
  # Funkcija za transformisanje kreiranog poligona
  def transformisi(self, *args):
      print ("Transformišem!")
      
      
      
  # Transformacijski okvir
  def tranformacije(self):
    
    self.funkcije = {'translacija': Trans(), 'skaliranje': Skal(), 
                     'smicanje': Smic(), 'rotacija': Rot(),
                     'refleksija': Refl()}
      
    def unos_transformacije(*args):
        print("Uneli ste novu transformaciju!")
        tr = var.get()
        print("Odabrali ste: {}".format(str(tr)))
        self.odabrana_transformacija = self.funkcije[tr]
        
        if tr == 'translacija' or tr == 'smicanje' or tr == 'skaliranje':
            x_koord.configure(state = 'normal')
            y_koord.configure(state = 'normal')
            ugao.configure(state = 'disabled')
        else:
            x_koord.configure(state = 'disabled')
            y_koord.configure(state = 'disabled')
            ugao.configure(state = 'normal')
        
    # Pravljenje okvira za odabir transformacije
    self.okvir_t = LabelFrame(self, text = 'Izaberite transformaciju', 
                              padx = 5, pady = 5)
    self.okvir_t.place(x = 150, y = 337,
                       height = 91, width = 170)

    # U zavisnosti od vrednosti var koje procitamo iz padajuceg menija,
    # pozivamo odgovarajucu funkciju transformacije
    var = StringVar(self)
    var.set('                 ')
    # Funkcija za pracenje promenljive
    var.trace('w', unos_transformacije)
    
    # Padajuca lista geometrijskih transformacija
    self.option = OptionMenu(self.okvir_t, var, 
                             'translacija', 
                             'skaliranje', 
                             'smicanje', 
                             'rotacija', 
                             'refleksija').pack()
    
    # Postavljanje dugmeta za pokretanje transformacije
    dugme_t = Button(self.okvir_t, text = 'Transformiši', 
                     command = self.transformisi).pack()
    
    # Naslovi parametara koje korisnik unosi
    x_koord_labela = Label(self, text = 'x:') 
    y_koord_labela = Label(self, text = 'y:') 
    ugao_labela = Label(self, text = u"\u03B8:") 
    
    # Promena pozicije elemenata
    x_koord_labela.place(x = 325, y = 345)
    y_koord_labela.place(x = 325, y = 370)
    ugao_labela.place(x = 325, y = 395)
    
    # Polja za unos vrednosti transformacija
    x_koord = Entry(self)
    y_koord = Entry(self)
    ugao = Entry(self)
    
    # Opcija za postavljanje elemenata u tabloliku strukturu
    x_koord.grid(row = 0, column = 1)
    y_koord.grid(row = 1, column = 1)
    
    # Konfiguracija elemenata, postavljanje sirine polja za unos parametara
    x_koord.config(width = 5)
    y_koord.config(width = 5)
    ugao.config(width = 5)
    
    # Promena pozicije elemenata
    x_koord.place(x = 345, y = 345)
    y_koord.place(x = 345, y = 370)
    ugao.place(x = 345, y = 395)
    
    self.mainloop()
  
  # Kontrola unosa tačaka
  def init_unos(self):
    # Pravljenje okvira za dugmad
    self.okvir_d = LabelFrame(self, text = 'Unosite tačke klikovima'
                               ' po platnu', padx = 10, pady = 10)
    self.okvir_d.place(x = 10, y = 315,
                       height = 120, width = 430)
    
    # Postavljanje dugmeta za kontrolu unosa
    self.dugme_u = Button(self.okvir_d, text = 'Zaključi unos',
                              command = self.promena_unosa)
    self.dugme_u.place(x = 0, y = 0)
    
    # Postavljanje dugmeta za konveksni omotač
    dugme_s = Button(self.okvir_d, text = 'Ispravi figuru',
                           command = self.ispravi)
    dugme_s.place(x = 0, y = 40)
    
    self.tranformacije()
    
    
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
      print('Dodata tačka (%.2f, %.2f) na zahtev korisnika!' % ttačka)
      
      # Iscrtavanje figure
      self.nacrtaj_figuru()
  
  # Promena teksta u zavisnosti od toga
  # da li je unos tačaka u toku ili ne
  def promena_unosa(self):
    if self.unos:
      self.okvir_d.config(text = 'Transformišite figuru pomoću dugmadi')
      self.dugme_u.config(text = 'Ponovi unos')
      
      # Promena stanja unosa i crtanje formiranog mnogougla
      self.unos = False
      self.nacrtaj_figuru()
      
      # Log poruka o akciji
      print('Zaključen unos tačaka na zahtev korisnika!')
    else:
      self.okvir_d.config(text = 'Unosite tačke klikovima po platnu')
      self.dugme_u.config(text = 'Zaključi unos')
      
      # Brisanje platna i reinicijalizacija liste tačaka
      self.obriši_platno()
      self.tačke = []
      self.ttačke = []
      self.id_tač = []
    
      # Promena stanja unosa
      self.unos = True
      
      # Log poruka o akciji
      print('Ponovljen unos tačaka na zahtev korisnika!')
  
  # Zamena liste tačaka konveksnim omotom
  def ispravi(self):
    self.tačke = konveksni_omot(self.tačke)
    self.ttačke = list(map(partial(mul, self.puk), self.tačke))
    
    # Crtanje ispravljene figure
    self.nacrtaj_figuru()
    
    # Log poruka o akciji
    print('Ispravljena figura na zahtev korisnika!')
  
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
  
  # Prikazivanje glavnih informacija o aplikaciji;
  # *args je neophodan kako bi se prosledili dodatni
  # podaci o događaju tastature, slično kao što fje
  # događaja u GLUT-u obavezno primaju koordinate
  def info(self, *args):
    # Log poruka o akciji
    print('Ispisane informacije o programu na zahtev korisnika!')
    
    # Prikazivanje glavnih informacija
    messagebox.showinfo('Informacije',
               'GeoDemonstrator, seminarski iz Programskih paradigmi.\n\n'
               'Korisnik zadaje mnogougao u dvodimenzionom okruženju, nad'
               ' kojim zatim vrši proizvoljne afine geometrijske'
               ' tranformacije: translaciju, rotaciju, refleksiju,'
               ' skaliranje, smicanje.\n\n'
               'Ideja je omogućiti jednostavno interaktivno prikazivanje i lakše'
               ' razumevanje materije koja se obrađuje na časovima Geometrije'
               ' za I smer, kao i Računarske grafike.\n\n'
               'Autori (tim KriLa):\n'
               'Kristina Pantelić, 91/2016,\n'
               'Lazar Vasović, 99/2016.\n\n'
               'Matematički fakultet, 2019')
  
  # Zatvaranje aplikacije na zahtev korisnika
  def kraj(self, *args):
    # Poruka korisniku o kraju programa
    if messagebox.askyesno('Kraj programa',
       'Da li stvarno želite da napustite program?'):
      
      # Log poruka o zatvaranju aplikacije
      print('GeoDemonstrator zatvoren na zahtev korisnika!')
      
      # Upotreba self.quit() zamrzava prozor na Windows-u,
      # pošto prekida izvršavanje i pokretačkog programa
      self.destroy()

# Obaveštenje o grešci ukoliko je modul
# pokrenut kao samostalan program
if __name__ == '__main__':
  greška('GKI nije samostalan program! Pokrenite main!')

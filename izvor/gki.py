#!/usr/bin/env python3

# Uključivanje sistemskog modula
from sys import exit as greška

# Uključivanje mixin modula
from trans import GeoMixinTrans
from util import GeoMixinHelp

# Uključivanje grafičkog modula
from tkinter import Tk, Menu, LabelFrame, Canvas, Button, \
                    Label, Entry, BooleanVar, StringVar, \
                    Checkbutton, OptionMenu, Radiobutton

# Uključivanje pomoćnog modula za
# kutijice sa iskačućim porukama
from tkinter.messagebox import showerror

# Uključivanje funkcionalnog modula
from functools import partial

# Uključivanje geometrijskog modula
from geom import *

# Nosilac programa je klasa GeoDemonstrator, koja
# nasleđuje grafičku klasu Tk iz modula tkinter, kao
# i mixin klase radi razdvajanja funkcionalnosti
class GeoDemonstrator(Tk, GeoMixinTrans, GeoMixinHelp):
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
    # Pravljenje glavnog menija
    meni = Menu(self)
    
    # Postavljanje sporednog padajućeg menija
    self.umeni = Menu(meni)
    self.umeni.add_command(label = 'Zaključi unos',
                           command = self.promena_unosa)
    self.umeni.add_command(label = 'Ispravi figuru',
                           command = self.ispravi)
    self.umeni.add_command(label = 'Očisti platno',
                           command = partial(self.novo_platno, True))
    
    # Postavljanje glavnog menija i vezivanje
    # komandi za odgovarajuće funkcionalnosti
    meni.add_cascade(label = 'Opcije', menu = self.umeni)
    meni.add_command(label = 'Pomoć (H)', command = self.pomoć)
    meni.add_command(label = 'Info (G)', command = self.info)
    self.config(menu = meni)
    
    # Vezivanje tipki za akcije analogne
    # onima iz prethodno postavljenog menija;
    # od F1 se odustalo jer se ne ponaša kako
    # treba na operativnom sistemu Windows
    self.bind('<H>', self.pomoć)
    self.bind('<h>', self.pomoć)
    self.bind('<G>', self.info)
    self.bind('<g>', self.info)
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
    self.slika = self.učitaj_sliku('koord.gif')
    self.platno.create_image(203, 131, image = self.slika)

    # Vezivanje čuvanja tačke za klik na platno
    self.unos = True
    self.platno.bind('<Button-1>', self.dodaj_tačku)
    
    # Vezivanje promene unosa za desni klik,
    # a ispravljanja figure za srednji, prema
    # sugestiji asistenta, čime se dobija na
    # lakoći korišćenja, bez potrebe za menijem
    self.platno.bind('<Button-2>', self.ispravi)
    self.platno.bind('<Button-3>', self.promena_unosa)
  
  # Okvir za magični svet transformacija
  def init_unos(self):
    # Pravljenje okvira za elemente
    self.okvir_d = LabelFrame(self, text = 'Unosite tačke klikovima'
                               ' po platnu', padx = 10, pady = 10)
    self.okvir_d.place(x = 10, y = 315,
                       height = 128, width = 430)
    
    # Inicijalizacija polja sa transformacijama
    self.init_trans()
    
    # Oznake parametara koje korisnik unosi
    x_koord_labela = Label(self, text = 'x:')
    y_koord_labela = Label(self, text = 'y:')
    ugao_labela = Label(self, text = '\u03b8:')
    
    # Postavljanje oznaka na prozor
    x_koord_labela.place(x = 185, y = 348)
    y_koord_labela.place(x = 185, y = 375)
    ugao_labela.place(x = 185, y = 403)
    
    # Polja za unos vrednosti transformacija
    self.x_koord = Entry(self, width = 4, state = 'disabled')
    self.y_koord = Entry(self, width = 4, state = 'disabled')
    self.ugao = Entry(self, width = 4, state = 'disabled')
    
    # Postavljanje polja na prozor
    self.x_koord.place(x = 200, y = 348)
    self.y_koord.place(x = 200, y = 375)
    self.ugao.place(x = 200, y = 403)
    
    # Postavljanje ostalih elemenata
    self.init_centar()
    self.init_inverz()
  
  # Transformacijski okvir
  def init_trans(self):
    # Mapa za preslikavanje niske u
    # odgavarajuću klasu transformacije
    self.funkcije = {'translacija': Trans,
                     'skaliranje': Skal, 
                     'smicanje': Smic,
                     'rotacija': Rot,
                     'refleksija': Refl}
    
    # Pravljenje okvira za odabir transformacije
    okvir_t = LabelFrame(self, text = 'Izaberite transformaciju', 
                                      padx = 23, pady = 7)
    okvir_t.place(x = 18, y = 337,
                  height = 95, width = 158)
    
    # U zavisnosti od vrednosti var koju pročitamo iz
    # padajućeg menija, poziva se prava transformacija
    self.tr = StringVar(self)
    self.tr.set('')
    
    # Funkcija za praćenje promenljive; izveštava o odabiru
    # transformacije i kontroliše pristup poljima za unos
    # parametara u zavisnosti od odabira; nepakovana lista
    # argumenata *args je neophodna kako bi se prosledili
    # (i zanemarili) dodatni podaci o promeni odabira, slično
    # kao što npr. kolbek funkcije u GLUT-u obavezno primaju
    # koordinate događaja, iako one često nisu nužan podatak
    self.tr.trace('w', lambda *args: print('Odabrana transformacija:'
                      ' {}.'.format(self.tr.get())) or self.kontrola())
    
    # Padajuća lista geometrijskih transformacija;
    # umesto dosad korišćene fje place za postavljanje
    # objekta na tačno određeno mesto na prozoru, ovde
    # se koristi pack, koji objekat optimalno spakuje
    # na raspoloživom prostoru; iz tog razloga je i
    # roditeljski element upravo transformacioni okvir,
    # u koji se pakuje, a ne self, kako je dosad bilo
    OptionMenu(okvir_t, self.tr, 'translacija', 'skaliranje', 
              'smicanje', 'rotacija', 'refleksija').pack(fill='x')
    
    # Dugme za pokretanje transformacije
    self.dugme_t = Button(okvir_t, text = 'Transformiši', 
                                   command = self.transformiši,
                                   state = 'disabled')
    self.dugme_t.pack(fill='x')
  
  # Odabir centra transformacije
  def init_centar(self):
    # Promenljiva za praćenje
    self.centar = StringVar(self)
    self.centar.set(None)
    self.centar.trace('w', lambda *args: print('Odabran {}'
                                 ' za centar transformacije.'
                                 .format(self.centar.get()))
                                   if self.centar.get() !=
                                      'None' else None)
    
    # Oznaka za odabir centra
    odabir_centra = Label(self, text = 'Centar transformacije:')
    odabir_centra.place(x = 265, y = 330)
    
    # Dugme za transformaciju sa centrom
    # u koordinatnom početku
    self.radio1 = Radiobutton(self,
              text = 'centar platna',
              padx = 3,
              variable = self.centar,
              value = 'centar platna',
              state = 'disabled',
              command = partial(self.kontrola, True))
    self.radio1.place(x = 242, y = 350)
    
    # Dugme za transformaciju sa centrom
    # u centru mase (baricentru) figure
    self.radio2 = Radiobutton(self, 
              text = 'centar mase',
              padx = 3, 
              variable = self.centar, 
              value = 'centar mase',
              state = 'disabled',
              command = partial(self.kontrola, True))
    self.radio2.place(x = 242, y = 370)
    
    # Dugme za transformaciju sa centrom
    # u korisnički unetoj tački
    self.radio3 = Radiobutton(self, 
              text = 'uneta tačka',
              padx = 3, 
              variable = self.centar, 
              value = 'korisnički unos',
              state = 'disabled',
              command = partial(self.kontrola, True))
    self.radio3.place(x = 242, y = 390)
    
    # Oznake za unos centra transformacija
    t1_labela = Label(self, text = 't1:')
    t2_labela = Label(self, text = 't2:')
    
    # Postavljanje oznaka na prozor
    t1_labela.place(x = 360, y = 358)
    t2_labela.place(x = 360, y = 385)
    
    # Polja za unos centra transformacija
    self.t1_koord = Entry(self, width = 4, state = 'disabled')
    self.t2_koord = Entry(self, width = 4, state = 'disabled')
    
    # Postavljanje polja na prozor
    self.t1_koord.place(x = 380, y = 358)
    self.t2_koord.place(x = 380, y = 385)
  
  # Funkcija za praćenje inverza
  def init_inverz(self):
    self.inv = BooleanVar(self)
    self.inv.trace('w', lambda *args: print('Odabrana inverzna'
                        ' transformacija.') if self.inv.get() else
                        print('Odabrana klasična transformacija.'))
    
    # Dugme za odabir inverza
    self.inverz = Checkbutton(self, text = 'Invertuj promenu',
                              variable = self.inv, state = 'disabled')
    self.inverz.place(x = 262, y = 410)

# Obaveštenje o grešci ukoliko je modul
# pokrenut kao samostalan program
if __name__ == '__main__':
  greška('GKI nije samostalan program! Pokrenite main!')

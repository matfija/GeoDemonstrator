#!/usr/bin/env python3

# Uključivanje sistemskog modula, kao i
# modula za rad sa datotečnim sistemom
from sys import exit as greška
from os.path import join as put

# Uključivanje grafičkog modula
from tkinter import Tk, Menu, LabelFrame, Canvas, Button, \
                    PhotoImage, Label, Entry, IntVar, StringVar, \
                    Checkbutton, OptionMenu, Radiobutton

# Uključivanje pomoćnog modula za
# kutijice sa iskačućim porukama
from tkinter.messagebox import showinfo, showerror, askyesno

# Uključivanje modula za nalazak konveksnog omotača
from omot import konveksni_omot

# Uključivanje funkcionalnog modula
from functools import partial

# Uključivanje modula sa operatorima
from operator import mul, itemgetter as ig

# Uključivanje matematičkog modula
from math import isnan

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
    
    # Transformacija
    self.tr = ''
    
    # Indikator inverzne transformacije
    self.inv = 0
    
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
    self.meni = Menu(self)
    
    # Postavljanje sporednog padajućeg menija
    self.umeni = Menu(self.meni)
    self.umeni.add_command(label = 'Zaključi unos',
                           command = self.promena_unosa)
    self.umeni.add_command(label = 'Ispravi figuru',
                           command = self.ispravi)
    self.umeni.add_command(label = 'Očisti platno',
                           command = self.novo_platno)
    
    # Postavljanje glavnog menija i vezivanje
    # komandi za odgovarajuće funkcionalnosti
    self.meni.add_cascade(label = 'Opcije', menu = self.umeni)
    self.meni.add_command(label = 'Info (F1)', command = self.info)
    self.meni.add_command(label = 'Kraj (Esc)', command = self.kraj)
    self.config(menu = self.meni)
    
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
  
  # Funkcija za dohvatanje vrednosti promenljive; pokušava
  # se evaluacija vrednosti ili ispaljuje izuzetak
  def uzmi_prom(self, prom):
    try:
      if prom == 'x':
        return float(eval(self.x_koord.get()))
      elif prom == 'y':
        return float(eval(self.y_koord.get()))
      else:
        return float(eval(self.ugao.get()))
    except:
      showerror('Greška', 'Loši parametri tranformacije!')
      return float('nan')
  
  # Funkcija za transformisanje kreiranog poligona
  def transformiši(self):
    # Nije moguće transformisati prazan skup tačaka
    if not self.ttačke:
      showerror('Greška', 'Unesite tačke na platno!')
      return
    
    # Neophodno je da transformacija bude odabrana
    if not self.tr:
      showerror('Greška', 'Izaberite transformaciju!')
      return
    
    # Neophodno je odabrati sve parametre rotacije
    if self.tr == 'rotacija' and \
       not self.način_rotacije and \
       not self.ugao.get():
      showerror('Greška', 'Izaberite ugao i način rotacije!')
      return
    elif self.tr == 'rotacija' and not self.način_rotacije:
      showerror('Greška', 'Izaberite način rotacije!')
      return
    
    # Preslikavanje stringa u odgovarajuću matricu
    # transformacije u zavisnosti od unetih parametara
    if self.tr == 'rotacija' and \
       self.način_rotacije == 'oko koordinatnog početka' or \
       self.tr == 'refleksija':
      # Greška ako nije unet ugao
      if not self.ugao.get():
        showerror('Greška', 'Unesite parametre tranformacije!')
        return
      
      # Izračunavanje parametra transformacije
      if self.inv == 0:
        u = self.uzmi_prom('u')
      else:
        u = -self.uzmi_prom('u')
      
      # Propagacija greške u izračunavanju
      if isnan(u): return
      
      self.odabrana_transformacija = (self.funkcije[self.tr])(u)
      
    # Obrada rotacije oko tačke
    elif self.tr == 'rotacija':
      centar_mase = lambda t: (sum(map(ig(0), t))/len(t),
                               sum(map(ig(1), t))/len(t))
      
      # Ukoliko je odabrana inverzna transformacija
      if self.inv == 0:
        u = self.uzmi_prom('u')
      else:
        u = -self.uzmi_prom('u')
      
      # Propagacija greške u izračunavanju
      if isnan(u): return
      
      if self.način_rotacije == 'oko centra mase':
        # Računanje centra mase
        t1, t2 = centar_mase(self.ttačke)
      elif self.način_rotacije == 'oko tačke':
        if not self.x_koord.get() or not self.x_koord.get():
          # Greška ako nisu uneti x i y
          showerror('Greška', 'Unesite parametre transformacije!')
          return
        
        # Izračunavanje parametra transformacije
        # i eventualna propagacija greške u računu
        t1 = self.uzmi_prom('x')
        if isnan(t1): return
        t2 = self.uzmi_prom('y')
        if isnan(t2): return
      
      self.odabrana_transformacija = (self.funkcije[self.tr])(u, t1, t2)
    
    else:
      if not self.x_koord.get() or not self.y_koord.get():
        # Greška ako nisu uneti x i y
        showerror('Greška', 'Unesite parametre tranformacije!')
        return
      
      # Izračunavanje parametra transformacije
      if self.inv == 0:
        t1 = self.uzmi_prom('x')
        if isnan(t1): return
        t2 = self.uzmi_prom('y')
      elif self.tr == 'skaliranje':
        t1 = 1/self.uzmi_prom('x')
        if isnan(t1): return
        t2 = 1/self.uzmi_prom('y')
      else:
        t1 = -self.uzmi_prom('x')
        if isnan(t1): return
        t2 = -self.uzmi_prom('y')
      
      # Propagacija greške u izračunavanju
      if isnan(t2): return
      
      self.odabrana_transformacija = (self.funkcije[self.tr])(t1,t2)

    # Nove transformisane tačke u
    # koordinatnom sistemu sa slike
    nttačke = list(map(partial(mul,
              self.odabrana_transformacija),
                      self.ttačke))
    
    # Provera da li su tačke otišle van koordinatnog
    # sistema sa slike tj. vidljivog dela platna
    if any(map(lambda t: t[0] < -29 or t[1] < -19 or
                     t[0] > 29 or t[1] > 19, nttačke)):
      showerror('Greška', 'Neuspela transformacija!')
      return
    else:
      # U slucaju da je korektno, iscrtava se transformisan poligon
      # ttačke -> lista tačaka u koordinatnom sistemu sa slike
      # tačke -> lista tačaka u koordinatnom sistemu platna
      print ('Izvršena transformacija: {}!'. format(self.tr))
      self.ttačke = nttačke
      self.tačke = list(map(partial(mul, self.kup), self.ttačke))
      self.nacrtaj_figuru()
      
  # Transformacijski okvir
  def tranformacije(self):
    # Mapa za preslikavanje stringa u
    # odgavarajuću matricu transformacije
    self.funkcije = {'translacija': Trans,
                     'skaliranje': Skal, 
                     'smicanje': Smic,
                     'rotacija': Rot,
                     'refleksija': Refl}
    
    def unos_transformacije(*args):
      # Čitanje vrednosti odabrane transformacije
      self.tr = var.get()
      print('Odabrana transformacija: {}'.format(self.tr))
      
      # Promena stanja dugmića u odnosu na odabir
      if self.tr != 'rotacija':
        self.način_rotacije = ''
        self.radio1.deselect()
        self.radio2.deselect()
        self.radio3.deselect()
        
        self.radio1.configure(state = 'disabled')
        self.radio2.configure(state = 'disabled')
        self.radio3.configure(state = 'disabled')
      else:
        self.radio1.configure(state = 'normal')
        self.radio2.configure(state = 'normal')
        self.radio3.configure(state = 'normal')
    
      # Dozvola i zabrana pristupa poljima za unos parametara 
      # u zavisnosti od odabrane transformacije
      if self.tr == 'translacija' or \
         self.tr == 'smicanje' or \
         self.tr == 'skaliranje':
        self.x_koord.configure(state = 'normal')
        self.y_koord.configure(state = 'normal')
        
        # Brisanje unete vrednosti parametra
        self.ugao.delete(0, 'end')
        self.ugao.configure(state = 'disabled')
      else:
        self.zabrana_pristupa()
        
    # Pravljenje okvira za odabir transformacije
    self.okvir_t = LabelFrame(self, text = 'Izaberite transformaciju', 
                              padx = 5, pady = 5)
    self.okvir_t.place(x = 20, y = 337,
                       height = 95, width = 170)

    # U zavisnosti od vrednosti var koju pročitamo iz
    # padajućeg menija, poziva se prava transformacija
    var = StringVar(self)
    var.set('                 ')
    
    # Funkcija za praćenje promenljive
    var.trace('w', unos_transformacije)
    
    # Padajuća lista geometrijskih transformacija
    self.option = OptionMenu(self.okvir_t, var, 
                             'translacija', 
                             'skaliranje', 
                             'smicanje', 
                             'rotacija', 
                             'refleksija').pack()
    
    # Postavljanje dugmeta za pokretanje transformacije
    dugme_t = Button(self.okvir_t, text = 'Transformiši', 
                     command = self.transformiši).pack()
    
    # Naslovi parametara koje korisnik unosi
    x_koord_labela = Label(self, text = 'x:')
    y_koord_labela = Label(self, text = 'y:')
    ugao_labela = Label(self, text = '\u03B8:')
    
    # Promena pozicije elemenata
    x_koord_labela.place(x = 200, y = 348)
    y_koord_labela.place(x = 200, y = 375)
    ugao_labela.place(x = 200, y = 403)
    
    # Polja za unos vrednosti transformacija
    self.x_koord = Entry(self, state = 'disabled')
    self.y_koord = Entry(self, state = 'disabled')
    self.ugao = Entry(self, state = 'disabled')
    
    # Promena pozicije elemenata
    self.x_koord.place(x = 215, y = 348)
    self.y_koord.place(x = 215, y = 375)
    self.ugao.place(x = 215, y = 403)
    
    # Konfiguracija elemenata, postavljanje
    # širine polja za unos parametara
    self.x_koord.config(width = 5)
    self.y_koord.config(width = 5)
    self.ugao.config(width = 5)
    
    # Konfiguracija ostalih parametara
    self.odabir_rotacije()
    self.inverz()
  
  # Funkcija za praćenje inverza
  def inverz(self):
    def odaberi_inverz(*args):
      self.inv = int(var.get())
      if self.inv == 1:
        print('Odabrana inverzna transformacija.')
    
    var = IntVar()
    var.trace('w', odaberi_inverz)
    
    self.inverz = Checkbutton(self, text = 'Inverz',
                              variable = var, command = None)
    self.inverz.place(x = 300, y = 410)
  
  # Kontrola pristupa poljima za unos
  def zabrana_pristupa(self):
    self.x_koord.delete(0, 'end')
    self.x_koord.configure(state = 'disabled')
    self.y_koord.delete(0, 'end')
    self.y_koord.configure(state = 'disabled')
    self.ugao.configure(state = 'normal')
  
  # Odabir načina rotacije
  def odabir_rotacije(self):
    def unos_rotacije(*args):
      self.način_rotacije = var.get()
    
    # Kontrola pristupa poljima za rotaciju
    def rot_promena():
      if self.način_rotacije != 'oko tačke':
        self.zabrana_pristupa()
      else:
        self.x_koord.configure(state = 'normal')
        self.y_koord.configure(state = 'normal')
        self.ugao.configure(state = 'normal')
    
    # Praćenje stanja rotacije
    var = StringVar()
    self.način_rotacije = ''
    var.trace('w', unos_rotacije)
    
    # Oznaka za odabir načina rotacije
    odabir_rotacije = Label(self,
        text = 'Način rotacije',
        justify = 'center',
        padx = 10)
    odabir_rotacije.place(x = 290, y = 326)
    
    # Dugme za rotaciju oko tačke (0, 0)
    self.radio1 = Radiobutton(self,
              text= 'oko koord. početka',
              padx = 3,
              variable = var,
              value = 'oko koordinatnog početka',
              command = rot_promena)
    self.radio1.place(x = 270, y = 345)
    
    # Dugme za rotaciju oko baricentra
    self.radio2 = Radiobutton(self, 
              text = 'oko centra mase',
              padx = 3, 
              variable = var, 
              value = 'oko centra mase',
              command = rot_promena)
    self.radio2.place(x = 270, y = 365)
    
    # Dugme za rotaciju oko unete tačke
    self.radio3 = Radiobutton(self, 
              text = 'oko tačke',
              padx = 3, 
              variable=var, 
              value= 'oko tačke',
              command = rot_promena)
    self.radio3.place(x = 270, y = 385)
    
    # Isprva su dugmad nepristupačna
    self.radio1.configure(state = 'disabled')
    self.radio2.configure(state = 'disabled')
    self.radio3.configure(state = 'disabled')
            
  # Okvir za magični svet transformacija
  def init_unos(self):
    # Pravljenje okvira za dugmad
    self.okvir_d = LabelFrame(self, text = 'Unosite tačke klikovima'
                               ' po platnu', padx = 10, pady = 10)
    self.okvir_d.place(x = 10, y = 315,
                       height = 128, width = 430)
    
    # Inicijalizacija polja sa transformacijama
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
      self.umeni.entryconfig(1, label = 'Ponovi unos')
      
      # Promena stanja unosa i crtanje formiranog mnogougla
      self.unos = False
      self.nacrtaj_figuru()
      
      # Log poruka o akciji
      print('Zaključen unos tačaka na zahtev korisnika!')
    else:
      self.okvir_d.config(text = 'Unosite tačke klikovima po platnu')
      self.umeni.entryconfig(1, label = 'Zaključi unos')
      
      # Brisanje platna i reinicijalizacija liste tačaka
      self.novo_platno()
      
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
  
  # Reinicijalizacija platna
  def novo_platno(self):
    self.obriši_platno()
    self.tačke = []
    self.ttačke = []
    self.id_tač = []
  
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
  
  # Prikazivanje glavnih informacija o aplikaciji
  def info(self, dog = None):
    # Log poruka o akciji
    print('Ispisane informacije o programu na zahtev korisnika!')
    
    # Prikazivanje glavnih informacija
    showinfo('Informacije',
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
  greška('GKI nije samostalan program! Pokrenite main!')

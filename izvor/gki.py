#!/usr/bin/env python3

# Uključivanje sistemskog modula, kao i
# modula za rad sa datotečnim sistemom
from sys import exit as greška
from os.path import join as put

# Uključivanje grafičkog modula
from tkinter import Tk, Menu, LabelFrame, Canvas, Button, \
                    PhotoImage, Label, Entry, BooleanVar, StringVar, \
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
    
    # Trenutna transformacija
    self.tr = ''
    
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
  
  # Funkcija za dohvatanje vrednosti promenljive; pokušava
  # se evaluacija vrednosti ili ispaljuje izuzetak
  def uzmi_prom(self, prom):
    try:
      if prom == 'x':
        return float(eval(self.x_koord.get()))
      elif prom == 'y':
        return float(eval(self.y_koord.get()))
      elif prom == 'u':
        return float(eval(self.ugao.get()))
      elif prom == 't1':
        return float(eval(self.t1_koord.get()))
      else:
        return float(eval(self.t2_koord.get()))
    except:
      showerror('Greška', 'Loši parametri transformacije!')
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
    
    # Rotacija i refleksija moraju da dobiju ugao
    if self.tr in ('rotacija', 'refleksija'):
      if not self.ugao.get():
        showerror('Greška', 'Unesite parametre transformacije!')
        return
      
      # Izračunavanje parametra (ugla)
      # rotacije odnosno refleksije
      u = self.uzmi_prom('u')
      
      # Propagacija greške u izračunavanju
      if isnan(u): return
      
      # Izračunavanje transformacije na osnovu centra
      if self.centar.get() == 'centar platna':
        transformacija = (self.funkcije[self.tr])(u, inv=self.inv.get())
      else:
        # Greška ako nisu uneti t1 i t2
        if not self.t1_koord.get() or not self.t2_koord.get():
          showerror('Greška', 'Unesite parametre transformacije!')
          return
        
        # Izračunavanje centra transformacije
        # i eventualna propagacija greške u računu
        t1 = self.uzmi_prom('t1')
        if isnan(t1): return
        t2 = self.uzmi_prom('t2')
        if isnan(t2): return
        
        transformacija = (self.funkcije[self.tr])(u, t1, t2,
                                                  inv=self.inv.get())
    else:
      # Greška ako nisu uneti x i y
      if not self.x_koord.get() or not self.y_koord.get():
        showerror('Greška', 'Unesite parametre transformacije!')
        return
      
      # Izračunavanje parametara transformacije
      # i eventualna propagacija greške u računu
      x = self.uzmi_prom('x')
      if isnan(x): return
      y = self.uzmi_prom('y')
      if isnan(y): return
      
      # Obrada aritmetičke greške (deljenja sa
      # nulom) u slučaju inverznog istezanja
      if self.tr == 'skaliranje' and \
         self.inv.get() and (x == 0 or y == 0):
          showerror('Greška', 'Deljenje nulom pri skaliranju!')
          return
      
      # Obrada geometrijske greške (loša inverzna
      # matrica) u slučaju inverznog smicanja
      if self.tr == 'smicanje' and \
         self.inv.get() and x != 0 and y != 0:
          showerror('Greška', 'Nedozvoljeno inverzno smicanje!')
          return
      
      # Translacija ne zahteva centar
      if self.tr == 'translacija' or \
         self.centar.get() == 'oko koordinatnog početka':
        transformacija = (self.funkcije[self.tr])(x, y,
                                                  inv=self.inv.get())
      else:
        # U suprotnom je greška ako nisu uneti t1 i t2
        if not self.t1_koord.get() or not self.t2_koord.get():
          showerror('Greška', 'Unesite parametre transformacije!')
          return
        
        # Izračunavanje centra transformacije
        # i eventualna propagacija greške u računu
        t1 = self.uzmi_prom('t1')
        if isnan(t1): return
        t2 = self.uzmi_prom('t2')
        if isnan(t2): return
        
        transformacija = (self.funkcije[self.tr])(x, y, t1, t2,
                                                  inv=self.inv.get())
    
    # Nove transformisane tačke u
    # koordinatnom sistemu sa slike
    nttačke = list(map(partial(mul, transformacija), self.ttačke))
    
    # Provera da li su tačke otišle van koordinatnog
    # sistema sa slike tj. vidljivog dela platna
    if any(map(lambda t: t[0] < -28.75 or t[1] < -18.75 or
                     t[0] > 28.75 or t[1] > 18.75, nttačke)):
      showerror('Greška', 'Transformacija izmešta figuru van platna!')
      return
    else:
      # U slucaju da je korektno, iscrtava se transformisan poligon
      # ttačke -> lista tačaka u koordinatnom sistemu sa slike
      # tačke -> lista tačaka u koordinatnom sistemu platna
      print ('Izvršena transformacija: {}.'. format(self.tr))
      self.ttačke = nttačke
      self.tačke = list(map(partial(mul, self.kup), self.ttačke))
      self.nacrtaj_figuru()
      
  # Transformacijski okvir
  def transformacije(self):
    # Mapa za preslikavanje stringa u
    # odgavarajuću matricu transformacije
    self.funkcije = {'translacija': Trans,
                     'skaliranje': Skal, 
                     'smicanje': Smic,
                     'rotacija': Rot,
                     'refleksija': Refl}
    
    # Nepakovana lista argumenata *args je neophodna
    # kako bi se prosledili (i zanemarili) dodatni
    # podaci o promeni odabira, slično kao što npr.
    # kolbek fje u GLUT-u obavezno primaju koordinate
    # događaja, iako one često nisu nužan podatak
    def unos_transformacije(*args):
      # Čitanje vrednosti odabrane transformacije
      self.tr = var.get()
      print('Odabrana transformacija: {}.'.format(self.tr))
      
      # Kontrola pristupa poljima za unos parametara 
      # u zavisnosti od odabrane transformacije
      self.kontrola()
        
    # Pravljenje okvira za odabir transformacije
    okvir_t = LabelFrame(self, text = 'Izaberite transformaciju', 
                                      padx = 4, pady = 4)
    okvir_t.place(x = 18, y = 337,
                  height = 95, width = 158)

    # U zavisnosti od vrednosti var koju pročitamo iz
    # padajućeg menija, poziva se prava transformacija
    var = StringVar(self)
    var.set('                 ')
    
    # Funkcija za praćenje promenljive
    var.trace('w', unos_transformacije)
    
    # Padajuća lista geometrijskih transformacija
    option = OptionMenu(okvir_t, var, 'translacija', 'skaliranje', 
                        'smicanje', 'rotacija', 'refleksija').pack()
    
    # Dugme za pokretanje transformacije
    dugme_t = Button(okvir_t, text = 'Transformiši', 
                     command = self.transformiši).pack()
    
    # Oznake parametara koje korisnik unosi
    x_koord_labela = Label(self, text = 'x:')
    y_koord_labela = Label(self, text = 'y:')
    ugao_labela = Label(self, text = '\u03B8:')
    
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
    
    # Konfiguracija ostalih parametara
    self.odabir_centra()
    self.inverz()
  
  # Funkcija za praćenje inverza
  def inverz(self):
    self.inv = BooleanVar()
    self.inv.trace('w', lambda *args: print('Odabrana inverzna'
                        ' transformacija.') if self.inv.get() else
                        print('Odabrana klasična transformacija.'))
    
    # Dugme za odabir inverza
    self.inverz = Checkbutton(self, text = 'Invertuj promenu',
                              variable = self.inv, command = None)
    self.inverz.place(x = 262, y = 410)
  
  # Kontrola pristupa poljima za unos
  def kontrola(self, radio=False):
    # Zanemarivanje kontrole ako još
    # nije birana transformacija
    if not self.tr:
      return
    
    # Svaka transformacija sem translacije
    # osvežava odabir centra transformacije
    if self.tr != 'translacija':
      if radio:
        self.t1_koord.config(state = 'normal')
        self.t2_koord.config(state = 'normal')
      
      # Uključivanje radio dugmića
      self.radio1.config(state = 'normal')
      self.radio2.config(state = 'normal')
      self.radio3.config(state = 'normal')
      
      # Postavljanje podrazumevanog centra
      if not radio:
        self.radio1.select()
    
    # Vektorske transformacije podrazumevaju
    # unos parametara x i y, ali ne i teta
    if self.tr in ('translacija',
                   'skaliranje',
                   'smicanje'):
      # Uključivanje unosa tačaka i eventualno
      # postavljanje na jedinične vrednosti
      self.x_koord.config(state = 'normal')
      
      if not radio:
        self.x_koord.delete(0, 'end')
      
      self.y_koord.config(state = 'normal')
      
      if not radio:
        self.y_koord.delete(0, 'end')
      
      # Podrazumevane su jedinične transformacije
      # ukoliko je došlo do promene transformacije
      if not radio:
       if self.tr == 'skaliranje':
         self.x_koord.insert(0, '1')
         self.y_koord.insert(0, '1')
       else:
         self.x_koord.insert(0, '0')
         self.y_koord.insert(0, '0')
       
       # Isključivanje unosa ugla
       self.ugao.delete(0, 'end')
       self.ugao.config(state = 'disabled')
      
      # Translacija nije oko tačke
      if self.tr == 'translacija':
        # Isključivanje unosa centra transformacije
        self.t1_koord.delete(0, 'end')
        self.t1_koord.config(state = 'disabled')
        
        self.t2_koord.delete(0, 'end')
        self.t2_koord.config(state = 'disabled')
        
        # Isključivanje svih radio dugmića
        self.centar.set('')
        
        self.radio1.config(state = 'disabled')
        self.radio2.config(state = 'disabled')
        self.radio3.config(state = 'disabled')
    
    # Rotacija i refleksija zahtevaju ugao i tačku,
    # ali promena nastaje samo uz promenu transformacije
    elif not radio:
        # Uključivanje unosa ugla i postavljanje
        # na podrazumevanu jediničnu vrednost
        self.ugao.config(state = 'normal')
        self.ugao.delete(0, 'end')
        self.ugao.insert(0, '0')
        
        # Isključivanje unosa koordinata
        self.x_koord.delete(0, 'end')
        self.x_koord.config(state = 'disabled')
        
        self.y_koord.delete(0, 'end')
        self.y_koord.config(state = 'disabled')
    
    # Eventualno upisivanje nekih
    # vrednosti u slobodna polja
    self.baricentar()
  
  # Eventualno upisivanje nekih
  # vrednosti u slobodna polja
  def baricentar(self):
    # Zanemarivanje kontrole ako još
    # nije birana transformacija
    if not self.tr:
      return
    
    # Popunjavanje centra transformacije
    if self.centar.get() in ('centar platna', 'centar mase'):
      baricentar = lambda t: (sum(map(ig(0), t))/len(t),
                              sum(map(ig(1), t))/len(t)) \
                                  if t else (0, 0)
      
      # Bira se centar mase ili centar platna
      t1, t2 = baricentar(self.ttačke) if self.centar.get() \
                                    == 'centar mase' else (0, 0)
      
      # Uključivanje polja za unos
      self.t1_koord.config(state = 'normal')
      self.t2_koord.config(state = 'normal')
      
      # Brisanje prethodnog sadržaja
      self.t1_koord.delete(0, 'end')
      self.t2_koord.delete(0, 'end')
      
      # Upisivanje novoizračunatih vrednosti
      self.t1_koord.insert(0, '%.2f'%t1)
      self.t2_koord.insert(0, '%.2f'%t2)
      
      # Gašenje polja za unos
      self.t1_koord.config(state = 'readonly')
      self.t2_koord.config(state = 'readonly')
  
  # Odabir centra transformacije
  def odabir_centra(self):
    # Promenljiva za praćenje
    self.centar = StringVar()
    self.centar.set(None)
    self.centar.trace('w', lambda *args: print('Odabran {}'
                                 ' za centar transformacije.'
                                 .format(self.centar.get()))
                                if self.centar.get() else None)
    
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
            
  # Okvir za magični svet transformacija
  def init_unos(self):
    # Pravljenje okvira za elemente
    self.okvir_d = LabelFrame(self, text = 'Unosite tačke klikovima'
                               ' po platnu', padx = 10, pady = 10)
    self.okvir_d.place(x = 10, y = 315,
                       height = 128, width = 430)
    
    # Inicijalizacija polja sa transformacijama
    self.transformacije()
    
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
  greška('GKI nije samostalan program! Pokrenite main!')

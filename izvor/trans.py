#!/usr/bin/env python3

# Uključivanje sistemskog modula
from sys import exit as greška

# Uključivanje pomoćnog modula za
# kutijice sa iskačućim porukama
from tkinter.messagebox import showerror

# Uključivanje funkcionalnog modula
from functools import partial

# Uključivanje modula sa operatorima
from operator import mul, itemgetter as ig

# Uključivanje matematičkog modula
from math import isnan

# Mixin klasa služi da razdvoji funkcionalnosti
# jedne klase na više delova, čime je poboljšana
# modularnost i čitljivost koda; nema konstruktor
# i sadrži isključivo pomoćne tj. dodatne metode
class GeoMixinTrans():
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
    if not self.tr.get():
      showerror('Greška', 'Izaberite transformaciju!')
      return
    
    # Rotacija i refleksija moraju da dobiju ugao
    if self.tr.get() in ('rotacija', 'refleksija'):
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
        # Pamćenje centra zbog log poruke
        t1, t2 = 0, 0
        
        # Izračunavanje same transformacije
        transformacija = (self.funkcije[self.tr.get()]) \
                           (u, inv = self.inv.get())
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
        
        # Izračunavanje same transformacije
        transformacija = (self.funkcije[self.tr.get()]) \
                        (u, t1, t2, inv = self.inv.get())
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
      if self.tr.get() == 'skaliranje' and \
         self.inv.get() and (x == 0 or y == 0):
          showerror('Greška', 'Deljenje nulom pri skaliranju!')
          return
      
      # Obrada aritmetičke greške (deljenja sa
      # nulom) u slučaju inverznog smicanja
      if self.tr.get() == 'smicanje' and \
         self.inv.get() and x*y == 1:
          showerror('Greška', 'Deljenje nulom pri smicanju!')
          return
      
      # Translacija ne zahteva centar, a ni bilo koja
      # transformacija sa centrom u koordinatnom početku
      if self.tr.get() == 'translacija' or \
         self.centar.get() == 'centar platna':
        # Pamćenje centra zbog log poruke
        t1, t2 = 0, 0
        
        # Izračunavanje same transformacije
        transformacija = (self.funkcije[self.tr.get()]) \
                          (x, y, inv = self.inv.get())
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
        
        # Izračunavanje same transformacije
        transformacija = (self.funkcije[self.tr.get()]) \
                      (x, y, t1, t2, inv = self.inv.get())
    
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
      # Log poruka o uspešnoj transformaciji
      if self.tr.get() == 'translacija':
        print('Izvršena {}translacija\nsa parametrima ({:.2f}, {:.2f}).'
              .format('inverzna ' if self.inv.get() else '', x, y))
      elif self.tr.get() in ('rotacija, refleksija'):
        print('Izvršena {}{}\nsa parametrom (uglom) {:.2f}\u00b0\n'
              'i centrom u ({:.2f}, {:.2f}).'.format('inverzna '
             if self.inv.get() else '', self.tr.get(), u, t1, t2))
      else:
        print('Izvršeno {}{}\nsa parametrima ({:.2f}, {:.2f})\n'
              'i centrom u ({:.2f}, {:.2f}).'.format('inverzno '
             if self.inv.get() else '', self.tr.get(), x, y, t1, t2))
      
      # ttačke -> lista tačaka u koordinatnom sistemu sa slike
      # tačke -> lista tačaka u koordinatnom sistemu platna
      self.ttačke = nttačke
      self.tačke = list(map(partial(mul, self.kup), self.ttačke))
      
      # Crtanje transformisane figure
      self.nacrtaj_figuru()
  
  # Kontrola pristupa poljima za unos
  def kontrola(self, radio=False):
    # Zanemarivanje kontrole ako još
    # nije birana transformacija
    if not self.tr.get():
      return
    
    # Svaka transformacija sem translacije
    # osvežava odabir centra transformacije
    if self.tr.get() != 'translacija':
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
    if self.tr.get() in ('translacija',
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
        if self.tr.get() == 'skaliranje':
          self.x_koord.insert(0, '1')
          self.y_koord.insert(0, '1')
        else:
          self.x_koord.insert(0, '0')
          self.y_koord.insert(0, '0')
        
        # Isključivanje unosa ugla
        self.ugao.delete(0, 'end')
        self.ugao.config(state = 'disabled')
      
      # Translacija nije oko tačke
      if self.tr.get() == 'translacija':
        # Isključivanje unosa centra transformacije
        self.t1_koord.delete(0, 'end')
        self.t1_koord.config(state = 'disabled')
        
        self.t2_koord.delete(0, 'end')
        self.t2_koord.config(state = 'disabled')
        
        # Isključivanje svih radio dugmića
        self.centar.set(None)
        
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
    if not self.tr.get():
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

# Obaveštenje o grešci ukoliko je modul
# pokrenut kao samostalan program
if __name__ == '__main__':
  greška('Mixin nije samostalan program! Pokrenite main!')

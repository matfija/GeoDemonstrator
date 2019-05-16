#### KriLa
<img height="460" src="https://raw.githubusercontent.com/matf-pp2019/Geo-Demonstrator/master/slike/2019_05_08.png">

## GeoDemonstrator :loop:
Seminarski rad na kursu Programske paradigme. Korisnik zadaje figuru u dvodimenzionom okruženju, nad kojom zatim vrši proizvoljne afine geometrijske transformacije: translaciju, rotaciju, refleksiju, skaliranje, smicanje.

Ukratko, skelet projekta je GKI sa platnom koje predstavlja koordinatni sistem, poljima za odabir i unos parametara transformacija i dugmetom koje ih izvršava. Ideja je omogućiti jednostavno interaktivno prikazivanje i lakše razumevanje materije koja se obrađuje na časovima Geometrije za I smer, kao i Računarske grafike.

## Tehnički detalji :robot:
Program je napisan u jeziku Python3 (malo starija verzija 3.2.3), na operativnom sistemu Ubuntu, uz korišćenje osobina raznih paradigmi odnosno obrazaca programiranja koji su u osnovi ovog jezika ili čiji se koncepti provlače kroz njega:
* imperativna/proceduralna paradigma: promenljive, funkcije, nizanje naredbi, opis procedure...,
* skript paradigma: exec, eval, obrada pozivanja čak i sintaksno neispravnih naredbi...,
* objektno-orijentisana paradigma: klase, nasleđivanje, polimorfizam, preopterećivanje operatora...,
* funkcionalna paradigma: map, filter, partial, fje višeg reda, lambda fje, dekoratori, apstrakcija listi...,
* komponentna paradigma: grafički korisnički interfejs, više nezavisnih modula koji predstavljaju ugovorene interfejse,
* konkurentna paradigma: višenitno programiranje (nalaženje konveksnog omotača je u potpunosti paralelizovano),
* reaktivno i programiranje vođeno događajima: GKI, koncept glavne petlje, osluškivanje i obrada događaja, reakcija na promenu stanja menija sa opcijama prilikom odabira željene transformacije,
* generičko programiranje: jedan obrazac obrade podataka nezavisno od ulaznih tipova, razni tipovi polimorfizma (magični metodi, dinamička tipiziranost, preopterećivanje operatora...),
* reflektivno i metaprogramiranje: pisanje programa unutar njega samog (nit sa povratnom vrednosti je u potpunosti ručno, dakle, dinamički definisana), in(tro)spekcija tj. refleksija na ovaj način napisane klase.

Upotrebljeni su i prikladni pomoćni moduli neobuhvaćeni fakultetskim kursevima: tkinter, threading, operator, time, inspect, types... Naravno, nisu izostavljeni ni oni upotrebljavani: sys, os, math, functools, random, copy...

GKI je odrađen pomoću Pajtonovog standardnog Tk/Tcl paketa – [tkinter](https://docs.python.org/3/library/tkinter.html) – koji se može podesiti komandom poput `sudo apt-get install python3-tk` za Ubuntu za starije verzije, dok je za novije automatski podešen.

## Podešavanje :memo:
Nakon kloniranja (`git clone https://github.com/matf-pp2019/Geo-Demonstrator`) tj. bilo kog načina preuzimanja repozitorijuma, program se pokreće uobičajenim pozivanjem Pajtonovog interpretatora nad glavnim fajlom (`python3 main.py`).

Osim toga, omogućeno je i direktno pokretanje komandom poput `./main.py`, pošto se na početku svake datoteke sa glavnom (main ili test) fjom nalazi shebang koji sugeriše operativnom sistemu gde se nalazi neophodni interpretator. Naravno, za ovaj pristup je neophodno prethodno učiniti fajl izvršivim komandom poput `chmod u+x main.py`.

Program korektno radi i na operativnom sistemu Windows, na kom je testiran preko alata [IDLE](https://www.python.org/downloads/release/python-323/). Za oba navedena operativna sistema dostupne su release verzije rada na odgovarajućoj [stranici](https://github.com/matf-pp2019/Geo-Demonstrator/releases) na GitHub adresi projekta.

## Članovi tima :computer:
* [Kristina Pantelić](https://github.com/beskonacnost), 91/2016
* [Lazar Vasović](https://github.com/matfija), 99/2016


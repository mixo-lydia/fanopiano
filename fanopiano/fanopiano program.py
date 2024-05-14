import random 
import re 

rad = 2 #nerovná se 6 aj.
mohutnost = rad * ( rad + 1 ) + 1 
vektorIncidence = {0,1,3} #známo empiricky pro řád = 2 
#vektorIncidence = {0,1,3,9} #známo empiricky pro řád = 3 
#vektorIncidence = {0,1,4,6} #známo empiricky pro řád = 3 
#vektorIncidence = {0,1,4,14,16} #známo empiricky pro řád = 4 
#vektorIncidence = {0,1,4,10,12,17} #známo empiricky pro řád = 5 

body   = range(0,mohutnost)
primky = range(0,mohutnost)
Bod    = True
Primka = not Bod 

def jeBod( misto ) : 
    return( misto[0] ) 
def incidence(l,P):
    # toť definice Fanovy roviny
    return( (l-P)%mohutnost in vektorIncidence )
def bodyPrimky( l ) :
    return( [ P for P in body if incidence( l , P ) ] )
def primkyBodem( P ) :
    return( [ l for l in primky if incidence( l , P ) ] )

jmenovkaBodu   = dict.fromkeys(body,   "")
jmenovkaPrimky = dict.fromkeys(primky, "")
jmenovkaPrimkyVBode  = { X : dict.fromkeys( primkyBodem(X) , "" ) for X in body   } 
jmenovkaBoduNaPrimce = { x : dict.fromkeys( bodyPrimky(x)  , "" ) for x in primky } 

def rozcestnik():
    if jeBod( tady ):
        textMista = "Jsi v místnosti " 
        textMista2 = "Změň označení místnosti" 
        jmenovkaMista = jmenovkaBodu[tady[1]] 
        jmenovkaOkoli = jmenovkaPrimkyVBode[tady[1]]
    else:
        textMista = "Jsi v chodbě " 
        textMista2 = "Změň označení chodby" 
        jmenovkaMista = jmenovkaPrimky[tady[1]] 
        jmenovkaOkoli = jmenovkaBoduNaPrimce[tady[1]]
    textOznaceni = "bez označení." if jmenovkaMista=="" else "označené \"" + jmenovkaMista + "\"." 
    dvereOzn = { i:jmenovkaOkoli[i] for i in jmenovkaOkoli if jmenovkaOkoli[i] != "" }
    nDvereOzn = len(dvereOzn)
    listDvereOzn = random.sample(list(dvereOzn.values()),nDvereOzn)
    nDvereNeozn = len(jmenovkaOkoli) - nDvereOzn
    textDvereOzn   = "" if nDvereOzn==0   else " Označené dveře: "+str(listDvereOzn)+"."
    textDvereNeozn = "" if nDvereNeozn==0 else " Počet dveří bez označení: "+str(nDvereNeozn)
    #|Jsi v místnosti/chodbě |označené "X"./bez označení.| Označené dveře: "a".| Počet dveří bez označení: 1|
    print( textMista + textOznaceni + textDvereOzn + textDvereNeozn )
    #Z Změň označení místnosti / chodby
    print( "" , "Z" , textMista2 )
    #D Projdi (některými) dveřmi bez označení
    sDvere = "" 
    if nDvereNeozn>0:
        print( "" , "D" , "Projdi (některými) dveřmi bez označení" )
        sDvere += "^D$|" 
    #1…Projdi dveřmi s označením …
    for i in range(0,nDvereOzn):
        print( "" , 1+i , "Projdi dveřmi s označením \""+listDvereOzn[i]+"\"" )
        sDvere += "^" + str(1+i) + "$|"
    #X Opusť geometrii
    print( "" , "X" , "Opusť geometrii" )
    x = input(" Zvol akci: ").upper()
    while not( re.match( "^(Z)|"+sDvere+"(X)$" , x ) ) :
        x = input(" \"" +x+ "\"  není platná akce. Zkus to znovu: ").upper()
    if x == "X":
        print ("R.I.P.")
        return False 
    elif x == "Z":
        noveJmenoMistnosti = input ("  Vyber jméno: ")
        pojmenujToTady (noveJmenoMistnosti)
    elif x == "D":
        noveJmenoDveri = input ("  Vyber jméno dveří: ")
        projdiDvermi ("",noveJmenoDveri)
    else:
        jmenoDveri = listDvereOzn [int (x) - 1]
        noveJmenoDveri = input ("  Vyber nové jméno (Enter pro zachování starého): ")
        projdiDvermi (jmenoDveri,noveJmenoDveri)
    return True 

def pojmenujToTady(jmeno):
    if jeBod( tady ):
        jmenovkaBodu[ tady[1] ] = jmeno
    else:
        jmenovkaPrimky[ tady[1] ] = jmeno

def projdiDvermi(jmeno, noveJmeno = None):
    global tady 
    if jeBod( tady ):
        jmenovkaOkoli = jmenovkaPrimkyVBode[ tady[1] ] 
    else:
        jmenovkaOkoli = jmenovkaBoduNaPrimce[ tady[1] ] 
    vyber = { i:jmenovkaOkoli[i] for i in jmenovkaOkoli if jmenovkaOkoli[i] == jmeno } 
    if not vyber : 
        print( "Jmenovka neexistuje." )
        return
    volba = random.choice(list(vyber.keys()))
    if noveJmeno != None:
        if noveJmeno != "":
            jmenovkaOkoli[volba] = noveJmeno
    tady = ( not jeBod( tady ) , volba ) 

tady = (Bod,0)
while rozcestnik():
    pass 

def cheat() : 
    '''
    for X in body :
        print( X , primkyBodem(X) )
    for X in body :
        print( X , [ 1 if incidence(p,X) else 0 for p in primky ] )
    print(jmenovkaBodu)
    print(jmenovkaPrimkyVBode)
    print(jmenovkaPrimky)
    print(jmenovkaBoduNaPrimce)
    print(tady)
    '''
    for X in body :
        print(    "Bod " + str(X) +"["+ jmenovkaBodu[X]   +"]" , *[ "[" + jmenovkaPrimkyVBode[X][x]  +"]>"+ str(x) +"["+ jmenovkaPrimky[x] +"]" for x in primkyBodem(X) ] )
    for x in primky :
        print( "Přímka " + str(x) +"["+ jmenovkaPrimky[x] +"]" , *[ "[" + jmenovkaBoduNaPrimce[x][X] +"]>"+ str(X) +"["+ jmenovkaBodu[X]   +"]" for X in bodyPrimky(x)  ] )
    print( "Tady je " + ( "bod " + str(tady[1]) +"["+ jmenovkaBodu[tady[1]] +"]" if tady[0] else "přímka " + str(tady[1]) +"["+ jmenovkaPrimky[tady[1]] +"]" ) ) 

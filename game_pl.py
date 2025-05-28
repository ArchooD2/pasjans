# game_pl.py
from board import stworzenie_talii, kolory_listy, obecna_karta_idx, wyswietl_plansze_gry
from os import system
import random as r

# --- Stałe ---
wartosci = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
kolory   = ["♥","♠","♦","♣"]

def niezakryte_karty(kolumna):
    return sum(1 for k in kolumna if not k.zakryta)

def przetasuj_stos_rezerwowy(stos_r):
    r.shuffle(stos_r)
    return stos_r, -1

def win(kolory_listy, kolumny, stos_r, idx):
    # 1) wszystkie na stosach końcowych
    if sum(len(p) for p in kolory_listy) == 52:
        print("Wygrałeś!"); return True
    # 2) brak kart w rezerwie + puste kolumny
    if not stos_r and all(len(c)==0 for c in kolumny):
        print("Wygrałeś! (Tabela pusta i brak rezerwy.)"); return True
    # 3) rezerwa wyczerpana + brak zakrytych kart
    ukryte = sum(1 for c in kolumny for k in c if k.zakryta)
    if idx == len(stos_r)-1 and ukryte == 0:
        print("Wygrałeś! (Brak ukrytych kart.)"); return True
    return False

def weryfikacja_ruchu(k1, k2):
    if kolory.index(k1.kolor)%2 == kolory.index(k2.kolor)%2: return False
    if wartosci.index(k1.wartosc)+1 != wartosci.index(k2.wartosc): return False
    return True

def ruch(przenoszone, typ, kolumny, src=0, uncov=0, dst=0, idx=0):
    system("cls")
    if typ=="kol→kol":
        if src==dst:
            print("Nie można na tę samą kolumnę."); return kolumny
        dest = kolumny[dst-1]
        for k in przenoszone:
            if not dest:
                if przenoszone[0].wartosc=="K":
                    dest.append(przenoszone[0]); kolumny[src-1].remove(przenoszone[0])
                else:
                    print("Tylko król do pustej kolumny."); return kolumny
            else:
                top = dest[-1]
                if weryfikacja_ruchu(k, top):
                    dest.append(k); kolumny[src-1].remove(k)
                else:
                    print(f"Nie można przenieść {przenoszone[0]} na {top}."); return kolumny
        print(f"Przeniesiono {', '.join(str(x) for x in przenoszone)} do kolumny {dst}.")
        if uncov==len(przenoszone) and kolumny[src-1]:
            kolumny[src-1][-1].zakryta=False

    elif typ=="kol→kon":
        k=przenoszone; i=kolory.index(k.kolor); f=kolory_listy[i]
        if len(f)==wartosci.index(k.wartosc):
            f.append(k); kolumny[src-1].remove(k)
            if uncov==1 and kolumny[src-1]: kolumny[src-1][-1].zakryta=False
            print(f"Przeniesiono {k} do stosu końcowego {k.kolor}")
        else:
            print(f"Nie można przenieść {k} do stosu końcowego.")

    elif typ=="rez→kol":
        k=przenoszone; dest=kolumny[dst-1]
        if not dest:
            if k.wartosc=="K":
                dest.append(k); stos_r.remove(k); idx-=1
                print(f"Przeniesiono {k} do pustej kolumny {dst}.")
            else:
                print("Tylko król do pustej kolumny.")
        elif weryfikacja_ruchu(k,dest[-1]):
            dest.append(k); stos_r.remove(k); idx-=1
            print(f"Przeniesiono {k} do kolumny {dst}.")
        else:
            print(f"Nie można przenieść {k} na {dest[-1]}.")
        return kolumny, idx

    elif typ=="rez→kon":
        k=przenoszone; i=kolory.index(k.kolor); f=kolory_listy[i]
        if len(f)==wartosci.index(k.wartosc):
            f.append(k); stos_r.remove(k); idx-=1
            print(f"Przeniesiono {k} do stosu końcowego {k.kolor}")
        else:
            print(f"Nie można przenieść {k} do stosu końcowego.")
        return kolumny, idx

    elif typ=="kon→kol":
        k=przenoszone; dest=kolumny[dst-1]
        if not dest and k.wartosc=="K":
            dest.append(k); print(f"Przeniesiono {k} do kolumny {dst}.")
        elif dest and weryfikacja_ruchu(k,dest[-1]):
            dest.append(k)
            kolory_listy[kolory.index(k.kolor)].remove(k)
            print(f"Przeniesiono {k} do kolumny {dst}.")
        else:
            print("Niepoprawny ruch kon→kol.")
        return kolumny, kolory_listy

    return kolumny

def main(kolumny, idx, kolory_listy, stos_r, talia):
    while True:
        print("======================================")
        wyswietl_plansze_gry(kolumny, stos_r, kolory, kolory_listy, idx)
        print("======================================")
        print("Wybierz opcję:")
        print("[1] kol→kol   [2] kol→kon   [3] rez→kol")
        print("[4] rez→kon   [5] dobierz   [6] kon→kol")
        print("[7] restart")
        w=int(input("Opcja (1–7): "))

        if w==1:
            s=int(input("Z kolumny (1–7): "))
            if 1<=s<=7 and kolumny[s-1]:
                col=kolumny[s-1]; nc=niezakryte_karty(col)
                print("Odkryte:")
                for i,k in enumerate(col[-nc:],1): print(f"{i}-{k}")
                p=int(input(f"Wybierz 1–{nc}: "))
                mov=col[-nc+p-1]
                # full slice for multi-card:
                movs=col[-nc+p-1:]
                d=int(input("Do kolumny (1–7): "))
                kolumny=ruch(movs,"kol→kol",kolumny,s,nc,d)
            else:
                system("cls"); print("Nieprawidłowa kolumna.")

        elif w==2:
            s=int(input("Kolumna na koniec (1–7): "))
            if 1<=s<=7 and kolumny[s-1]:
                k=kolumny[s-1][-1]
                kolumny=ruch(k,"kol→kon",kolumny,s,niezakryte_karty(kolumny[s-1]))
            else:
                system("cls"); print("Nieprawidłowa kolumna.")

        elif w==3:
            if idx==-1:
                system("cls"); print("Brak karty w rezerwie.")
            else:
                d=int(input("Do kolumny (1–7): "))
                if 1<=d<=7:
                    k=stos_r[idx]
                    kolumny,idx=ruch(k,"rez→kol",kolumny,0,niezakryte_karty(kolumny[d-1]),d,idx)
                else:
                    system("cls"); print("Nieprawidłowa kolumna.")

        elif w==4:
            if idx==-1:
                system("cls"); print("Brak karty w rezerwie.")
            else:
                kolumny,idx=ruch(stos_r[idx],"rez→kon",kolumny,0,0,0,idx)

        elif w==5:
            if idx==len(stos_r)-1:
                stos_r,idx=przetasuj_stos_rezerwowy(stos_r)
            else:
                idx+=1
            system("cls")

        elif w==6:
            f=int(input("Stos koncowy (1–4): "))
            d=int(input("Do kolumny (1–7): "))
            if 1<=d<=7 and kolory_listy[f-1]:
                k=kolory_listy[f-1][-1]
                kolumny,kolory_listy=ruch(k,"kon→kol",kolumny,0,0,d)
            else:
                system("cls"); print("Nieprawidłowo lub pusto.")

        elif w==7:
            system("cls")
            for c in kolumny: c.clear()
            talia.clear()
            talia,kolumny=stworzenie_talii()
            stos_r=talia; idx=-1
            for f in kolory_listy: f.clear()
            print("Gra zresetowana.")

        else:
            system("cls"); print("Opcja 1–7.")

        if win(kolory_listy, kolumny, stos_r, idx):
            wyswietl_plansze_gry(kolumny, stos_r, kolory, kolory_listy, idx)
            break

if __name__=="__main__":
    talia, kolumny = stworzenie_talii()
    stos_r        = talia
    idx           = obecna_karta_idx
    main(kolumny, idx, kolory_listy, stos_r, talia)

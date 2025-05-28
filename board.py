import random as r
# Card values
wartosci = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]  # values
kolory = ["♥","♠","♦","♣"]  # suits
serca = []   # hearts
piki = []    # spades
karo = []    # diamonds
trefle = []  # clubs
stos_r = []  # Stos rezerwowy / reserve stack (stock)
kolory_listy = [serca, piki, karo, trefle]  # lists for each suit
talia = []  # deck
kolumny = [[] for _ in range(7)]  # tableau columns
obecna_karta_idx = -1  # Nie odkryta karta w stosie rezerwowym / index of current card in reserve stack

class Karta:  # Card
    def __init__(self,wartosc,kolor,zakryta):
        self.wartosc = wartosc  # value
        self.kolor = kolor      # suit
        self.zakryta = zakryta  # face down (True/False)

    def __str__(self):
        if self.zakryta:
            return "[???]"
        if self.kolor in ["♥","♦"]:
            if self.wartosc == "10":
                return f"[\033[91m{self.wartosc}{self.kolor}\033[00m]"
            return f"[\033[91m{self.wartosc} {self.kolor}\033[00m]"
        if self.wartosc == "10":
            return f"[\033[96m{self.wartosc}{self.kolor}\033[00m]"
        return f"[\033[96m{self.wartosc} {self.kolor}\033[00m]"

    def __repr__(self):
        return self.__str__()

def stworzenie_talii():  # create_deck
    for i in wartosci:
        for j in kolory:
            karta = Karta(i,j,True)
            talia.append(karta)
    r.shuffle(talia)
    for i in range(7):
        for j in range(i+1):
            karta = talia.pop(0)
            karta.zakryta = (i != j)
            kolumny[i].append(karta)
    return talia, kolumny

def wyswietl_stos_rezerwowy(stos_r, obecna_karta_idx=0):  # display_reserve_stack
    if not stos_r:  
        print("[Pusty stos rezerwowy]   ", end="")  # [Empty reserve stack]
        return
    if obecna_karta_idx > -1 and obecna_karta_idx < len(stos_r):
        if obecna_karta_idx + 1 < len(stos_r):
            print("[???]", end=" ")
        elif obecna_karta_idx + 1 == len(stos_r):
            print("", end="")
        stos_r[obecna_karta_idx].zakryta = False  # odkrywa kartę / reveal card
        print(stos_r[obecna_karta_idx], end="     ")
        if obecna_karta_idx == len(stos_r):
            print()
    elif obecna_karta_idx == -1:
        print("[???]", end="           ")

def wyswietl_stos_koncowy(kolory,kolory_listy):  # display_foundation_stacks
    for i in range(4):
        if len(kolory_listy[i]) == 0:
            if kolory[i] in ["♥", "♦"]:
                print( f"[\033[91m{kolory[i]}\033[00m]", end="   ")
            else:
                print(f"[\033[96m{kolory[i]}\033[00m]", end="   ")
        else:
            print(f"{kolory_listy[i][-1]}", end="   ")
    print("\n")  

def wyswietl_plansze(kolumny):  # display_tableau
    print("  1      2      3      4      5      6      7")
    for i in range(14):
        if i >= max(len(k) for k in kolumny):
            break
        for j in kolumny:
            if len(j)-1 >= i:
                print(f"{j[i]}", end="  ")
            else:
                print("     ", end="  ")
        print() 

def wyswietl_plansze_gry(kolumny, stos_r, kolory, kolory_listy, obecna_karta_idx):  # display_game_board
    wyswietl_stos_rezerwowy(stos_r, obecna_karta_idx)
    wyswietl_stos_koncowy(kolory, kolory_listy)
    wyswietl_plansze(kolumny)
# game_en.py
from board import stworzenie_talii, kolory_listy, obecna_karta_idx, wyswietl_plansze_gry
from os import system
import random as r

# --- Constants ---
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS  = ["♥", "♠", "♦", "♣"]

# --- Helpers ---
def count_uncovered_cards(col):
    return sum(1 for card in col if not card.zakryta)

def shuffle_stock(stock):
    r.shuffle(stock)
    return stock, -1

def check_win(foundation_stacks, columns, stock, stock_idx):
    # 1) All 52 on foundations
    if sum(len(pile) for pile in foundation_stacks) == 52:
        print("You won!")
        return True

    # 2) Stock empty + all tableau empty
    if not stock and all(len(col) == 0 for col in columns):
        print("You won! (Tableau cleared and no stock.)")
        return True

    # 3) Stock exhausted + no face-down cards left
    hidden = sum(1 for col in columns for c in col if c.zakryta)
    if stock_idx == len(stock) - 1 and hidden == 0:
        print("You won! (No hidden cards remain.)")
        return True

    return False

def validate_move(card_from, card_to):
    if SUITS.index(card_from.kolor) % 2 == SUITS.index(card_to.kolor) % 2:
        return False
    if VALUES.index(card_from.wartosc) + 1 != VALUES.index(card_to.wartosc):
        return False
    return True

def move(moving, move_type, columns, src=0, uncov=0, dst=0, stok_idx=0):
    system("cls")
    if move_type == "col→col":
        if src == dst:
            print("Cannot move to the same column."); return columns
        dest = columns[dst-1]
        for c in moving:
            if not dest:
                if moving[0].wartosc == "K":
                    dest.append(moving[0]); columns[src-1].remove(moving[0])
                else:
                    print("Only a King can start an empty column."); return columns
            else:
                top = dest[-1]
                if validate_move(c, top):
                    dest.append(c); columns[src-1].remove(c)
                else:
                    print(f"Cannot move {moving[0]} onto {top}."); return columns
        print(f"Moved {', '.join(str(c) for c in moving)} to column {dst}.")
        if uncov == len(moving) and columns[src-1]:
            columns[src-1][-1].zakryta = False

    elif move_type == "col→found":
        card = moving
        idx = SUITS.index(card.kolor)
        f = foundation_stacks[idx]
        if len(f) == VALUES.index(card.wartosc):
            f.append(card); columns[src-1].remove(card)
            if uncov == 1 and columns[src-1]: columns[src-1][-1].zakryta = False
            print(f"Moved {card} to foundation {card.kolor}")
        else:
            print(f"Cannot move {card} to foundation.")

    elif move_type == "stock→col":
        card = moving; dest = columns[dst-1]
        if not dest:
            if card.wartosc == "K":
                dest.append(card); stock.remove(card); stok_idx -= 1
                print(f"Moved {card} to empty column {dst}.")
            else:
                print("Only a King can start an empty column.")
        elif validate_move(card, dest[-1]):
            dest.append(card); stock.remove(card); stok_idx -= 1
            print(f"Moved {card} to column {dst}.")
        else:
            print(f"Cannot move {card} onto {dest[-1]}.")
        return columns, stok_idx

    elif move_type == "stock→found":
        card = moving; idx = SUITS.index(card.kolor); f = foundation_stacks[idx]
        if len(f) == VALUES.index(card.wartosc):
            f.append(card); stock.remove(card); stok_idx -= 1
            print(f"Moved {card} to foundation {card.kolor}")
        else:
            print(f"Cannot move {card} to foundation.")
        return columns, stok_idx

    elif move_type == "found→col":
        card = moving; dest = columns[dst-1]
        if not dest and card.wartosc == "K":
            dest.append(card); print(f"Moved {card} back to column {dst}.")
        elif dest and validate_move(card, dest[-1]):
            dest.append(card)
            foundation_stacks[SUITS.index(card.kolor)].remove(card)
            print(f"Moved {card} back to column {dst}.")
        else:
            print("Invalid foundation→column move.")
        return columns, foundation_stacks

    return columns

# --- Main Loop ---
def main(columns, stock_idx, foundation_stacks, stock, deck):
    while True:
        print("======================================")
        wyswietl_plansze_gry(columns, stock, SUITS, foundation_stacks, stock_idx)
        print("======================================")
        print("Choose an option:")
        print("[1] col→col   [2] col→found   [3] stock→col")
        print("[4] stock→found   [5] draw stock   [6] found→col")
        print("[7] Restart")
        choice = int(input("Option (1–7): "))

        if choice == 1:
            src = int(input("From column (1–7): "))
            if 1<=src<=7 and columns[src-1]:
                col = columns[src-1]; cnt = count_uncovered_cards(col)
                print("Uncovered cards:")
                for i,c in enumerate(col[-cnt:],1): print(f"{i}-{c}")
                pick = int(input(f"Pick 1–{cnt}: "))
                moving = col[-cnt+pick-1:]
                dst   = int(input("To column (1–7): "))
                columns = move(moving, "col→col", columns, src, cnt, dst)
            else:
                system("cls"); print("Invalid source col.")

        elif choice == 2:
            src = int(input("Col for foundation (1–7): "))
            if 1<=src<=7 and columns[src-1]:
                card = columns[src-1][-1]
                columns = move(card, "col→found", columns, src, count_uncovered_cards(columns[src-1]))
            else:
                system("cls"); print("Invalid column.")

        elif choice == 3:
            if stock_idx == -1:
                system("cls"); print("No stock card shown.")
            else:
                dst = int(input("To column (1–7): "))
                if 1<=dst<=7:
                    card = stock[stock_idx]
                    columns, stock_idx = move(card, "stock→col", columns, 0,
                                              count_uncovered_cards(columns[dst-1]), dst, stock_idx)
                else:
                    system("cls"); print("Invalid column.")

        elif choice == 4:
            if stock_idx == -1:
                system("cls"); print("No stock card shown.")
            else:
                columns, stock_idx = move(stock[stock_idx], "stock→found", columns, 0,0,0,stock_idx)

        elif choice == 5:
            if stock_idx == len(stock)-1:
                stock, stock_idx = shuffle_stock(stock)
            else:
                stock_idx += 1
            system("cls")

        elif choice == 6:
            f = int(input("Foundation (1–4): "))
            dst = int(input("To column (1–7): "))
            if 1<=dst<=7 and foundation_stacks[f-1]:
                card = foundation_stacks[f-1][-1]
                columns, foundation_stacks = move(card, "found→col", columns, 0,0,dst)
            else:
                system("cls"); print("Invalid foundation or empty.")

        elif choice == 7:
            system("cls")
            for c in columns: c.clear()
            deck.clear()
            deck, columns = stworzenie_talii()
            stock = deck; stock_idx = -1
            for f in foundation_stacks: f.clear()
            print("Game reset.")

        else:
            system("cls"); print("Choose 1–7.")

        if check_win(foundation_stacks, columns, stock, stock_idx):
            wyswietl_plansze_gry(columns, stock, SUITS, foundation_stacks, stock_idx)
            break

if __name__ == "__main__":
    deck, columns      = stworzenie_talii()
    stock              = deck
    foundation_stacks  = kolory_listy
    stock_idx          = obecna_karta_idx
    main(columns, stock_idx, foundation_stacks, stock, deck)

#!/usr/bin/env python3.8

import random


def gen_uno_deck(count: int = 1, suits: str = "rgby", colourless: int = None):
    # By default, multiply the number of colourless cards by how many suits
    # there are.
    if colourless is None:
        colourless = len(suits)
    deck = [f"{colour}0" for colour in suits]
    deck.extend([f"{colour}{i}" for colour in suits for i in range(1, 10)] * 2)
    deck.extend([f"{colour}s" for colour in suits] * 2)  # skip turn
    deck.extend([f"{colour}r" for colour in suits] * 2)  # reverse
    deck.extend(["xw"] * colourless)  # wildcard
    deck.extend([f"{colour}t" for colour in suits] * 2)  # draw two
    deck.extend(["xf"] * colourless)  # wild draw four
    deck *= count
    random.shuffle(deck)
    return deck


def gen_dos_deck(count: int = 1, suits: str = "rgby", colourless: int = None):
    # By default, multiply the number of colourless cards by how many suits
    # there are.
    if colourless is None:
        # Multiply by 3 here instead of down below so explicit calls can be
        # more fine-grained about how many DOS cards there are.
        colourless = 3 * len(suits)
    deck = [f"{colour}0" for colour in suits]
    deck.extend([f"{colour}1" for colour in suits] * 3)
    deck.extend([f"{colour}{i}" for colour in suits for i in range(3, 6)] * 3)
    deck.extend([f"{colour}{i}" for colour in suits for i in range(6, 11)] * 2)
    deck.extend([f"{colour}#" for colour in suits] * 2)  # pound
    deck.extend(["xd"] * colourless)  # crazy dos
    deck *= count
    random.shuffle(deck)
    return deck


def gen_hanafuda_deck(count: int = 1):
    deck = [f"{value}{suit}" for value in "xxtq" for suit in (1, 3)]
    deck.extend([f"{value}{suit}" for value in "xxtp" for suit in (2, 4, 5, 6, 7, 9, 10)])
    deck.extend([f"{value}8" for value in "xxpq"])
    deck.extend([f"{value}11" for value in "xtpq"])
    deck.extend([f"{value}12" for value in "xxxq"])
    deck *= count
    random.shuffle(deck)
    return deck


def gen_regular_deck(count: int = 1, suits: str = "scdh", jokers: int = 0):
    deck = [f"{suit}{i}" for suit in suits for i in range(2, 11)]
    deck.extend([f"{suit}{i}" for suit in suits for i in "ajqk"])
    deck.extend(["xj"] * jokers)
    deck *= count
    random.shuffle(deck)
    return deck


class ParseError(ValueError):
    pass


def parse_hanafuda(card: str):
    if not len(card) == 2 and not card[1:].isdigit():
        raise ParseError(f"Invalid format {card!r}. Cards should be in format \"s#\".")

    if card[0] == 'x': prefix = "```\n~"
    elif card[0] == 't': prefix = "```diff\n-"
    elif card[0] in "pq": prefix = "```diff\n+"
    else:
        raise ParseError(f"Invalid colour {card[0]!r} in {card!r}. Valid suits are 'x', 't', 'p' and 'q'.")

    if card[1:].isdigit() and int(card[1:]) in range(1,13):
        month_num = int(card[1:])
        month_en = {
            1: "Pine",
            2: "Plum",
            3: "Cherry",
            4: "Wisteria",
            5: "Iris",
            6: "Peony",
            7: "Lespedeza",
            8: "Pampas",
            9: "Chrysanthemum",
            10: "Maple",
            11: "Willow",
            12: "Paulownia"
        }[month_num]
    else:
        raise ParseError(f"Invalid card {card[1:]!r} in {card!r}. Valid suits are 1-12.")

    if card[0] == 'p': #10 pts
        value_en = {
            2: "Nightingale",
            4: "Cuckoo",
            5: "Bridge",
            6: "Butterfly",
            7: "Boar",
            8: "Goose",
            9: "Wine cup",
            10: "Deer",
            11: "Rain"
        }.get(month_num, "Invalid")
    elif card[0] == 'q': #20 pts
        value_en = {
            1: "Crane",
            3: "Curtain",
            8: "Moon",
            11: "Swallow",
            12: "Phoenix"
        }.get(month_num, "Invalid")
    elif card[0] == 't': # tanzaku
        if month_num in range(1,4): value_en = "Red Poem Tanzaku"
	        elif month_num in (4,5,7): value_en = "Red Tanzaku"
        elif month_num in (6,9,10): value_en = "Blue Tanzaku"
        else: value_en = "Invalid"
    elif card[0] == 'x': value_en = "Plain" #plain
    else:
        raise ParseError(f"Invalid card {card[1:]!r} in {card!r}. Valid cards are 0-10, s, r, w, t, f, d, and #.")

    if card[0] == 'x': suffix = "~```"
    elif card[0] == 't': suffix = "- ```"
    elif card[0] in "pq": suffix = "+ ```"
    return " ".join((prefix, month_en, value_en, suffix))


def parse_card(card: str):
    if not len(card) == 2 and not card[1:].isdigit():
        raise ParseError(f"Invalid format {card!r}. Cards should be in format \"s#\".")

    if card[0] == 'x':
        prefix = "```\n~"
    elif card[0] == 'r':
        prefix = "```diff\n- Red"
    elif card[0] == 'g':
        prefix = "```diff\n+ Green"
    elif card[0] == 'b':
        prefix = "```markdown\n# Blue"
    elif card[0] == 'y':
        prefix = "```fix\n% Yellow"
    elif card[0] == 's':
        prefix = "```\n- \u2660"
    elif card[0] == 'c':
        prefix = "```\n- \u2663"
    elif card[0] == 'd':
        prefix = "```diff\n- \u2666"
    elif card[0] == 'h':
        prefix = "```diff\n- \u2665"
    else:
        raise ParseError(f"Invalid colour {card[0]!r} in {card!r}. Valid suits are 'r', 'g', 'b', and 'y', and colourless 'x'.")

    if card[1:].isdigit():
        value = card[1:]
    elif card[1] == 's':
        value = "Skip"
    elif card[1] == 'r':
        value = "Reverse"
    elif card[1] == 'w':
        value = "WILD"
    elif card[1] == 't':
        value = "Draw Two"
    elif card[1] == 'f':
        value = "WILD Draw Four"
    elif card[1] == 'd':
        value = "WILD DoS"
    elif card[1] == '#':
        value = "WILD #"
    elif card[1] == 'a':
        value = "Ace"
    elif card[1] == 'k':
        value = "King"
    elif card[1] == 'q':
        value = "Queen"
    elif card[1] == 'j':
        value = "Joker" if (card[0] == 'x') else "Jack"
    else:
        raise ParseError(f"Invalid card {card[1:]!r} in {card!r}. Valid cards are 0-10, s, r, w, t, f, d, and #.")

    if card[0] == 'x':
        suffix = "~```"
    elif card[0] == 'r':
        suffix = "-```"
    elif card[0] == 'g':
        suffix = "+```"
    elif card[0] == 'b':
        suffix = "#```"
    elif card[0] == 'y':
        suffix = "%```"
    elif card[0] ==s':
        suffix = "of Spades \u2660 -```"
    elif card[0] == 'c':
        suffix = "of Clubs \u2663 -```"
    elif card[0] == 'd':
        suffix = "of Diamonds \u2666 -```"
    elif card[0] == 'h':
        suffix = "of Hearts \u2665 -```"
    return " ".join((prefix, value, suffix))

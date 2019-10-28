#!/usr/bin/env python3.8

import random
import re


HANAFUDA_CARD = re.compile(
    # Month
    r"\b(?:(?P<suit>1[0-2]|[1-9]|pine|january|plum|february|cherry|march"
    r"|wisteria|april|iris|may|peony|june|lespedeza|july|pampas|august"
    r"|chrysanthemum|september|maple|october|willow|november|paulownia"
    r"|december) ?)?"
    # Value
    r"(?P<value>[xtpq]|plain|flower"
    r"|(?:(?:red )?(?:poem )?|blue )?(?:tanzaku|ribbon)|tane|animal|light"
    r"|crane|nightingale|curtain|cuckoo|bridge|butterflies|boar|moon|geese"
    r"|sake cup|deer|rain|swallow|lightning|phoenix)"
    # Reversed order month
    r"(?(suit)|(?: of | )?(?P<suit>1[0-2]|[1-9]|pine|january|plum|february"
    r"|cherry|march|wisteria|april|iris|may|peony|june|lespedeza|july|pampas"
    r"|august|chrysanthemum|september|maple|october|willow|november|paulownia"
    r"|december)?)\b",
    re.IGNORECASE
)
HANAFUDA_VALUES = {
    "plain":            "x",
    "flower":           "x",
    "tanzaku":          "t",
    "ribbon":           "t",
    "red poem tanzaku": "t",
    "red poem ribbon":  "t",
    "poem tanzaku":     "t",
    "poem tanzaku":     "t",
    "red tanzaku":      "t",
    "red ribbon":       "t",
    "blue tanzaku":     "t",
    "blue ribbon":      "t",
    "tane":             "p",
    "animal":           "p",
    "light":            "q"
}
HANAFUDA_SUITS = {
    "pine":             "1",
    "january":          "1",
    "plum":             "2",
    "february":         "2",
    "cherry":           "3",
    "march":            "3",
    "wisteria":         "4",
    "april":            "4",
    "iris":             "5",
    "may":              "5",
    "peony":            "6",
    "june":             "6",
    "lespedeza":        "7",
    "july":             "7",
    "pampas":           "8",
    "august":           "8",
    "chrysanthemum":    "9",
    "september":        "9",
    "maple":            "10",
    "october":          "10",
    "willow":           "11",
    "november":         "11",
    "paulownia":        "12",
    "december":         "12"
}
HANAFUDA_UNIQUES = {
    "crane":        "q1",
    "nightingale":  "p2",
    "curtain":      "q3",
    "cuckoo":       "p4",
    "bridge":       "p5",
    "butterflies":  "p6",
    "boar":         "p7",
    "geese":        "p8",
    "moon":         "q8",
    "sake cup":     "p9",
    "deer":         "p10",
    "lightning":    "x11",
    "swallow":      "p11",
    "rain":         "q11",
    "phoenix":      "q12"
}
HANAFUDA_MONTHS = {
    "1": "Pine",
    "2": "Plum",
    "3": "Cherry",
    "4": "Wisteria",
    "5": "Iris",
    "6": "Peony",
    "7": "Lespedeza",
    "8": "Pampas",
    "9": "Chrysanthemum",
    "10": "Maple",
    "11": "Willow",
    "12": "Paulownia"
}

CARD = re.compile(
    # Suit
    r"\b(?:(?P<suit>[rgbyxscdh]|red|green|blue|yellow|spades|clubs|diamonds"
    r"|hearts) ?)?"
    # Value
    r"(?P<value>10|[0-9srwtfd#akqj]|one|two|three|four|five|six|seven|eight"
    r"|nine|ten|skip|reverse|wild(?: draw four| dos| #)?|draw two|draw four"
    r"|dos|ace|king|queen|jack|joker)"
    # Reversed order suit
    r"(?(suit)|(?: of | )?(?P<suit>[rgbyxscdh]|red|green|blue|yellow|spades"
    r"|clubs|diamonds|hearts)?)\b",
    re.IGNORECASE
)
VALUES = {
    "zero":             "0",
    "one":              "1",
    "two":              "2",
    "three":            "3",
    "four":             "4",
    "five":             "5",
    "six":              "6",
    "seven":            "7",
    "eight":            "8",
    "nine":             "9",
    "ten":              "10",
    "skip":             "s",
    "wild":             "w",
    "draw two":         "t",
    "wild draw four":   "f",
    "draw four":        "f",
    "wild dos":         "d",
    "dos":              "d",
    "wild #":           "#",
    "ace":              "a",
    "king":             "k",
    "queen":            "q",
    "jack":             "j",
    "joker":            "j"
}


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
    match = HANAFUDA_CARD.match(card)
    if not match:
        raise ParseError(f"Invalid Hanafuda card {card!r}; must be a month and a type, or the name of a special card.")
    value, suit = match.group("value", "suit")
    value, suit = value.casefold(), suit.casefold()
    if not suit:
        if value in HANAFUDA_UNIQUES:   # Unique card names (don't need month)
            return HANAFUDA_UNIQUES[value]
        else:
            raise ParseError(f"Monthless Hanafuda card {card!r} isn't unique.")
    if suit in HANAFUDA_SUITS:      # Translate words into number( string)s
        suit = HANAFUDA_SUITS[suit]
    elif suit not in HANAFUDA_MONTHS:
        raise ParseError(f"Invalid Hanafuda suit {suit!r} in card {card!r}.")
    if value in HANAFUDA_UNIQUES:
        compare = HANAFUDA_UNIQUES[value]
        if compare[1:] == suit:
            return compare
        else:
            raise ParseError(f"Unique Hanafuda card name {value!r} can't be found in month {suit!r}; card {card!r} is invalid.")
    if ((value in ("red poem tanzaku", "poem tanzaku", "red poem ribbon", "poem ribbon") and suit not in "123") or
            (value in ("red tanzaku", "red ribbon") and suit not in ("4", "5", "7", "11")) or
            (value in ("blue tanzaku", "blue ribbon") and suit not in ("6", "9", "10"))):
        raise ParseError(f"Hanafuda cards of type {value!r} can't be found in month {suit!r}; card {card!r} is invalid.")
    if value in HANAFUDA_VALUES:    # Translate words into x, t, p, or q
        value = HANAFUDA_VALUES[value]
    elif value not in "xtpq":
        raise ParseError(f"Invalid Hanafuda value {value!r} in card {card!r}.")
    if ((value == "q" and suit not in (1, 3, 8, 11, 12)) or
            (value == "p" and suit in (1, 3, 12)) or
            (value == "t" and suit in (8, 12))):
        raise ParseError(f"Hanafuda value {value!r} can't be found in month {suit!r}; card {card!r} is invalid.")
    return "".join((value, suit))


def parse_card(card: str):
    match = CARD.match(card)
    if not match:
        raise ParseError(f"Invalid card {card!r}; must be a suit followed by a value.")
    suit, value = match.group("suit", "value")
    suit, value = suit.casefold(), value.casefold()
    if not suit:
        suit = "x"
    else:
        if suit[0] not in "rgbyxscdh":
            raise ParseError(f"Invalid suit {suit!r} in card {card!r}.")
        else:
            suit = suit[0]
    if value == "joker" and not suit == "x":
        raise ParseError(f"Jokers can't have suits (suit {suit!r} in card {card!r}).")
    if value in VALUES:
        value = VALUES[value]
    elif value not in "srwtfd#akqj" and not (value.isdigit() and 0 <= int(value) <= 10):
        # This shouldn't be possible unless CARD or VALUES are wrong.
        raise AssertionError(f"Invalid value {value!r} in card {card!r}; either the regexp or the value dict are incorrect.")
    if suit in "scdh" and value in "01swtfd#":
        raise ParseError(f"Nonsensical suit/value pair ({suit}/{value}) in card {card!r}.")
    elif suit in "rgby" and value in "akqj":
        raise ParseError(f"Nonsensical suit/value pair ({suit}/{value}) in card {card!r}.")
    return "".join((suit, value))


def format_hanafuda(card: str):
    if not len(card) == 2 and not card[1:].isdigit():
        raise ValueError(f"Invalid format {card!r}. Cards should be in format \"s#\".")

    if card[0] == 'x':
        prefix = "```\n~"
    elif card[0] == 't':
        prefix = "```diff\n-"
    elif card[0] in "pq":
        prefix = "```diff\n+"
    else:
        raise ValueError(f"Invalid value {card[0]!r} in {card!r}. Valid values are 'x', 't', 'p' and 'q'.")

    if card[1:] in HANAFUDA_MONTHS:
        month_en = HANAFUDA_MONTHS[card[1:]]
        month_num = int(card[1:])
    else:
        raise ValueError(f"Invalid month {card[1:]!r} in {card!r}. Valid months are 1-12.")

    if card[0] == 'p':      # 10 pts
        try:
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
            }[month_num]
        except KeyError:
            raise ValueError(f"Card value 'p' invalid in month {month_num!r} ({month_en}).") from None
    elif card[0] == 'q':    # 20 pts
        try:
            value_en = {
                1: "Crane",
                3: "Curtain",
                8: "Moon",
                11: "Swallow",
                12: "Phoenix"
            }[month_num]
        except KeyError:
            raise ValueError(f"Card value 'q' invalid in month {month_num!r} ({month_en}).") from None
    elif card[0] == 't':    # tanzaku
        if 1 <= month_num <= 3:
            value_en = "Red Poem Tanzaku"
        elif month_num in (4, 5, 7):
            value_en = "Red Tanzaku"
        elif month_num in (6, 9, 10):
            value_en = "Blue Tanzaku"
        else:
            raise ValueError(f"Card value 't' invalid in month {month_num!r} ({month_en}).")
    elif card[0] == 'x':    # plain
        if month_num == 11:
            value_en = "Lightning"
        else:
            value_en = "Plain"

    if card[0] == 'x':
        suffix = "~```"
    elif card[0] == 't':
        suffix = "- ```"
    elif card[0] in "pq":
        suffix = "+ ```"
    return " ".join((prefix, month_en, value_en, suffix))


def format_card(card: str):
    if not len(card) == 2 and not card[1:].isdigit():
        raise ValueError(f"Invalid format {card!r}. Cards should be in format \"s#\".")

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
        raise ValueError(f"Invalid colour {card[0]!r} in {card!r}. Valid suits are 's', 'c', 'd', 'h', 'r', 'g', 'b', and 'y', and colourless 'x'.")

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
        raise ValueError(f"Invalid card {card[1:]!r} in {card!r}. Valid cards are 0-10, a, k, q, j, s, r, w, t, f, d, and #.")

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
    elif card[0] == 's':
        suffix = "of Spades \u2660 -```"
    elif card[0] == 'c':
        suffix = "of Clubs \u2663 -```"
    elif card[0] == 'd':
        suffix = "of Diamonds \u2666 -```"
    elif card[0] == 'h':
        suffix = "of Hearts \u2665 -```"
    return " ".join((prefix, value, suffix))

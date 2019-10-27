#!/usr/bin/env python

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


def gen_regular_deck(count: int = 1, suits: str = "scdh", jokers: int = 0):
    deck = [f"{suit}{i}" for suit in suits for i in range(2, 11)]
    deck.extend([f"{suit}{i}" for suit in suits for i in "ajqk"])
    deck.extend(["xj"] * jokers)
    deck *= count
    random.shuffle(deck)
    return deck


class ParseError(ValueError):
    pass


def parse_card(card: str):
    if not len(card) == 2 and not card.endswith("10"):
        raise ParseError(f"Invalid format {card!r}. Cards should be in format \"s#\".")

    if card[0] == 'x':
        prefix = "```\n~ "
    elif card[0] == 'r':
        prefix = "```diff\n- Red "
    elif card[0] == 'g':
        prefix = "```diff\n+ Green "
    elif card[0] == 'b':
        prefix = "```markdown\n# Blue "
    elif card[0] == 'y':
        prefix = "```fix\n% Yellow "
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
    else:
        raise ParseError(f"Invalid card {card[1:]!r} in {card!r}. Valid cards are 0-10, s, r, w, t, f, d, and #.")

    if card[0] == 'x':
        suffix = " ~```"
    elif card[0] == 'r':
        suffix = " -```"
    elif card[0] == 'g':
        suffix = " +```"
    elif card[0] == 'b':
        suffix = " #```"
    elif card[0] == 'y':
        suffix = " %```"
    return "".join((prefix, value, suffix))

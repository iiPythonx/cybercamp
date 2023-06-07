# Copyright 2023 Benjamin O'Brien

# Modules
import os
import string
from rich import print
from typing import Union
from iipython import readchar, keys

# Load rockyou
with open("common-passwords.txt", "r", encoding = "latin1") as fh:
    rockyou = fh.read().splitlines()

# Helpers
def has(password: str, charset: str) -> bool:
    return any([c for c in password if c in charset])

def center(text: str) -> str:
    tag = ""
    if "] " in text:
        tag, text = text.split("] ")[0] + "] ", text.split("] ")[1]

    add = round((os.get_terminal_size()[0] / 2) - (len(text) / 2))
    return tag + (" " * add) + text

# Perform key layout inspection
layouts = ["qwe", "asd", "zxc", "123", "iop", "jkl", "bnm", "rty", "fgh", "vbn", "bnm"]

# Handle score calculation
def score(password: str) -> Union[int, str]:
    if password in rockyou:
        return 0, "Password found on rockyou.txt database."

    elif len(password) < 8:
        return 0, ""

    # Perform layout checking
    elif any([a for a in layouts if a in password.lower()]):
        return 0, "Password contains some form of qwerty."

    # Actual scoring system
    score = 100
    for idx, char in enumerate(password):
        if (idx > 1) and (char == password[idx - 1] == password[idx - 2]):
            score -= 5  # If you repeat characters, less score

    # Perform character checking
    good_chars = [c for c in password if c in string.punctuation]
    if len(good_chars) < 2:
        score -= (10 * (2 - len(good_chars)))  # The less special charactefrom rich import print

    return (score if score >= 0 else 0), ""

# Handle mainloop
if __name__ == "__main__":
    psw = ""
    while True:
        os.system("clear")
        print(center("[ PASSWORD CHECKER ]"))
        print(center(f"> {psw}"))
        print()

        # Calculate total score
        if psw:
            s, v = score(psw)
            print(center(f"Score: {s} (out of 100)"))
            print(center("[green] Good password!" if s >= 80 else "[yellow] Not bad, I would make a better one though!" if s >= 60 else "[red] What in the heck is that?"))

            # Check if password is from rockyou
            if v:
                print()
                print(center(f"[red] {v}"))

        # Handle keypresses
        c = readchar()
        if c == keys.CTRL_C:
            del rockyou
            break

        elif (c == keys.BACKSPACE) and psw:
            psw = psw[:-1]

        elif isinstance(c, str) and c != "\t":
            psw += c

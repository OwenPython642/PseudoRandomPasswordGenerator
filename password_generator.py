import random
import string

chars = string.ascii_letters + string.digits + string.punctuation


def generate_password(length, uppercase, digits, symbol):
    chars = string.ascii_lowercase
    if uppercase:
        chars += string.ascii_uppercase
    if digits:
        chars += string.digits
    if symbol:
        chars += string.punctuation
    return "".join(random.choice(chars) for _ in range(lenght))


def word_processing(word):
    return word.encode("unicode_escape").decode()


if __name__ == "__main__":
    lenght: int = int(input("Entrez la longueur du mot de passe : "))
    uppercase = input("Voulez vous des majuscules ? (o/n)")
    if uppercase == "o":
        uppercase = True
    else:
        uppercase = False
    digits = input("Voulez vous des chiffres ? (o/n)")
    if digits == "o":
        digits = True
    else:
        digits = False
    symbol = input("Voulez vous des symboles ? (o/n)")
    if symbol == "o":
        symbol = True
    else:
        symbol = False
    print(word_processing(generate_password(int(lenght), uppercase, digits, symbol)))

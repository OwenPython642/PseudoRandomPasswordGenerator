import random
import string

def generate_password(length, use_upper, use_digits, use_symbols):
    chars = string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def word_processing(word):
    return word.encode("unicode_escape").decode()

if __name__ == "__main__":
    length = int(input("Longueur du mot de passe : "))
    upper = input("Majuscules ? (o/n) : ").lower() == "o"
    digits = input("Chiffres ? (o/n) : ").lower() == "o"
    symbols = input("Symboles ? (o/n) : ").lower() == "o"
    print(word_processing(generate_password(length, upper, digits, symbols)))

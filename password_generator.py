import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password(length, use_upper, use_digits, use_symbols):
    chars = string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation
    if not chars:
        return ""
    return ''.join(random.choice(chars) for _ in range(length))

def word_processing(word):
    return word.encode("unicode_escape").decode()

def on_generate():
    try:
        length = int(entry_length.get())
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "La longueur doit être un entier positif.")
        return

    use_upper = var_upper.get()
    use_digits = var_digits.get()
    use_symbols = var_symbols.get()

    password = generate_password(length, use_upper, use_digits, use_symbols)
    processed = word_processing(password)
    entry_result.delete(0, tk.END)
    entry_result.insert(0, processed)

# --- Interface ---
root = tk.Tk()
root.title("Générateur de mot de passe")

# Longueur
tk.Label(root, text="Longueur du mot de passe :").grid(row=0, column=0, sticky="w")
entry_length = tk.Entry(root)
entry_length.grid(row=0, column=1)

# Chiffres
tk.Label(root, text="Inclure des chiffres ?").grid(row=1, column=0, sticky="w")
var_digits = tk.BooleanVar(value=False)
tk.Radiobutton(root, text="Oui", variable=var_digits, value=True).grid(row=1, column=1, sticky="w")
tk.Radiobutton(root, text="Non", variable=var_digits, value=False).grid(row=1, column=2, sticky="w")

# Majuscules
tk.Label(root, text="Inclure des majuscules ?").grid(row=2, column=0, sticky="w")
var_upper = tk.BooleanVar(value=False)
tk.Radiobutton(root, text="Oui", variable=var_upper, value=True).grid(row=2, column=1, sticky="w")
tk.Radiobutton(root, text="Non", variable=var_upper, value=False).grid(row=2, column=2, sticky="w")

# Symboles
tk.Label(root, text="Inclure des symboles ?").grid(row=3, column=0, sticky="w")
var_symbols = tk.BooleanVar(value=False)
tk.Radiobutton(root, text="Oui", variable=var_symbols, value=True).grid(row=3, column=1, sticky="w")
tk.Radiobutton(root, text="Non", variable=var_symbols, value=False).grid(row=3, column=2, sticky="w")

# Bouton générer
tk.Button(root, text="Générer", command=on_generate).grid(row=4, column=0, columnspan=3, pady=10)

# Résultat
tk.Label(root, text="Mot de passe généré :").grid(row=5, column=0, sticky="w")
entry_result = tk.Entry(root, width=40)
entry_result.grid(row=5, column=1, columnspan=2)

root.mainloop()

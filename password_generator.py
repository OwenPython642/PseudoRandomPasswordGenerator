import sys, subprocess, importlib, string, secrets

def import_with_auto_install(pkg):
    try:
        return importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        return importlib.import_module(pkg)

import_with_auto_install("PyQt5")

from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QSpinBox, QCheckBox,
    QPushButton, QLineEdit, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt

def calculate_brute_force_time(password):
    """Calcule le temps estimé pour craquer le mot de passe par brute force"""
    if not password:
        return 0, "Aucun"
    
    # Détermination de l'espace de caractères
    charset_size = 0
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_symbol: charset_size += 32  # Approximation des symboles courants
    
    # Calcul du nombre de combinaisons possibles
    length = len(password)
    total_combinations = charset_size ** length
    
    # Temps moyen = la moitié des combinaisons possibles
    # Vitesse moderne d'attaque brute force : ~1 milliard de tentatives/seconde
    attempts_per_second = 1_000_000_000
    average_time_seconds = total_combinations / (2 * attempts_per_second)
    
    return average_time_seconds, format_time(average_time_seconds)

def format_time(seconds):
    """Formate le temps en unités lisibles"""
    if seconds < 1:
        return "< 1 seconde"
    elif seconds < 60:
        return f"{int(seconds)} secondes"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} heures"
    elif seconds < 31536000:
        return f"{int(seconds/86400)} jours"
    elif seconds < 31536000000:
        return f"{int(seconds/31536000)} années"
    else:
        return f"{seconds/31536000:.1e} années"

def evaluate_password_strength(password):
    """Évalue la robustesse du mot de passe basée sur le temps de brute force"""
    if not password:
        return "Aucun", "red"
    
    time_seconds, time_str = calculate_brute_force_time(password)
    
    # Classification basée sur le temps de crack
    if time_seconds < 86400:  # Moins d'1 jour
        return f"Faible ({time_str})", "red"
    elif time_seconds < 31536000:  # Moins d'1 an
        return f"Moyenne ({time_str})", "orange"
    else:  # Plus d'1 an
        return f"Forte ({time_str})", "green"
def generate_password(length, use_upper, use_digits, use_symbols):
    chars = string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length)) if chars else ""

class PassGen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de mot de passe")
        layout = QFormLayout(self)

        self.spin_len = QSpinBox()
        self.spin_len.setRange(1, 100)
        layout.addRow("Longueur :", self.spin_len)

        self.cb_upper = QCheckBox("Majuscules")
        layout.addRow(self.cb_upper)

        self.cb_digits = QCheckBox("Chiffres")
        layout.addRow(self.cb_digits)

        self.cb_symbols = QCheckBox("Symboles")
        layout.addRow(self.cb_symbols)

        btn_gen = QPushButton("Générer")
        btn_gen.clicked.connect(self.on_generate)
        layout.addRow(btn_gen)

        self.edit_res = QLineEdit()
        self.edit_res.setReadOnly(True)
        layout.addRow("Mot de passe :", self.edit_res)

        btn_copy = QPushButton("Copier")
        btn_copy.clicked.connect(self.on_copy)
        layout.addRow(btn_copy)

        # Indicateur de sécurité
        self.security_label = QLabel("Sécurité : Aucun")
        self.security_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")
        self.security_label.setWordWrap(True)  # Permet le retour à la ligne
        layout.addRow("Temps de crack :", self.security_label)

    def on_generate(self):
        pwd = generate_password(
            self.spin_len.value(),
            self.cb_upper.isChecked(),
            self.cb_digits.isChecked(),
            self.cb_symbols.isChecked()
        )
        if not pwd:
            QMessageBox.warning(self, "Erreur", "Aucun caractère sélectionné.")
            self.security_label.setText("Aucun")
            self.security_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")
        else:
            self.edit_res.setText(pwd)
            self.update_security_indicator(pwd)

    def update_security_indicator(self, password):
        """Met à jour l'indicateur de sécurité"""
        strength, color = evaluate_password_strength(password)
        self.security_label.setText(strength)
        self.security_label.setStyleSheet(f"QLabel {{ color: {color}; font-weight: bold; }}")

    def on_copy(self):
        pwd = self.edit_res.text()
        if pwd:
            clipboard = QApplication.clipboard()
            if clipboard is not None:
                clipboard.setText(pwd)
                QMessageBox.information(self, "Copié", "Mot de passe copié.")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'accéder au presse-papiers.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PassGen()
    w.show()
    sys.exit(app.exec_())
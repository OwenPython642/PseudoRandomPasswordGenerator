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

def evaluate_password_strength(password):
    """Évalue la robustesse du mot de passe et retourne un score et une couleur"""
    if not password:
        return "Aucun", "red"
    
    score = 0
    length = len(password)
    
    # Points pour la longueur
    if length >= 8:
        score += 2
    elif length >= 6:
        score += 1
    
    # Points pour la diversité des caractères
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    
    char_types = sum([has_lower, has_upper, has_digit, has_symbol])
    score += char_types
    
    # Points bonus pour longueur élevée
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    
    # Détermination du niveau
    if score >= 6:
        return "Forte", "green"
    elif score >= 4:
        return "Moyenne", "orange"
    else:
        return "Faible", "red"
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
        self.spin_len.setRange(1, 1001)
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
        layout.addRow("Robustesse :", self.security_label)

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
import sys
import subprocess
import importlib

def import_with_auto_install(pkg):
    """Importe un package et l'installe automatiquement si nécessaire"""
    try:
        return importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        return importlib.import_module(pkg)

# Installation automatique de PyQt5 si nécessaire
import_with_auto_install("PyQt5")

from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QSpinBox, QCheckBox,
    QPushButton, QLineEdit, QMessageBox, QLabel, QApplication
)
from PyQt5.QtCore import Qt
from password_utils import generate_password, evaluate_password_strength

class PassGen(QWidget):
    """Interface graphique pour le générateur de mots de passe"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Générateur de mot de passe")
        self.setFixedSize(400, 300)
        layout = QFormLayout(self)

        # Contrôle de la longueur
        self.spin_len = QSpinBox()
        self.spin_len.setRange(1, 100)
        self.spin_len.setValue(12)  # Valeur par défaut
        layout.addRow("Longueur :", self.spin_len)

        # Options de caractères
        self.cb_upper = QCheckBox("Majuscules")
        self.cb_upper.setChecked(True)  # Coché par défaut
        layout.addRow(self.cb_upper)

        self.cb_digits = QCheckBox("Chiffres")
        self.cb_digits.setChecked(True)  # Coché par défaut
        layout.addRow(self.cb_digits)

        self.cb_symbols = QCheckBox("Symboles")
        self.cb_symbols.setChecked(True)  # Coché par défaut
        layout.addRow(self.cb_symbols)

        # Bouton de génération
        btn_gen = QPushButton("Générer")
        btn_gen.clicked.connect(self.on_generate)
        layout.addRow(btn_gen)

        # Affichage du résultat
        self.edit_res = QLineEdit()
        self.edit_res.setReadOnly(True)
        layout.addRow("Mot de passe :", self.edit_res)

        # Bouton de copie
        btn_copy = QPushButton("Copier")
        btn_copy.clicked.connect(self.on_copy)
        layout.addRow(btn_copy)

        # Indicateur de sécurité
        self.security_label = QLabel("Aucun mot de passe généré")
        self.security_label.setStyleSheet("QLabel { color: gray; font-weight: bold; }")
        self.security_label.setWordWrap(True)
        layout.addRow("Temps de crack :", self.security_label)

    def on_generate(self):
        """Génère un nouveau mot de passe"""
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
        """Copie le mot de passe dans le presse-papiers"""
        pwd = self.edit_res.text()
        if pwd:
            clipboard = QApplication.clipboard()
            if clipboard is not None:
                clipboard.setText(pwd)
                QMessageBox.information(self, "Copié", "Mot de passe copié dans le presse-papiers.")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'accéder au presse-papiers.")
        else:
            QMessageBox.warning(self, "Erreur", "Aucun mot de passe à copier.")
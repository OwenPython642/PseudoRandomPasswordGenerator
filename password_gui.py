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
    QPushButton, QLineEdit, QMessageBox, QLabel, QApplication, QHBoxLayout
)
from PyQt5.QtCore import Qt
from password_utils import (
    evaluate_password_strength, Observer, PasswordGenerator
)

class PassGen(QWidget, Observer):
    """Interface graphique pour le générateur de mots de passe"""
    
    def __init__(self):
        super().__init__()
        
        # Initialisation du générateur
        self.password_generator = PasswordGenerator()
        
        # Abonnement aux changements
        self.password_generator.attach(self)
        
        self.init_ui()
        self.update_password_display()
        self.update_security_indicator()
    
    def update(self, subject):
        """Méthode du pattern Observer - appelée quand le générateur change"""
        if isinstance(subject, PasswordGenerator):
            self.update_password_display()
            self.update_security_indicator()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Générateur de mot de passe")
        self.setFixedSize(450, 300)
        layout = QFormLayout(self)

        # Contrôle de la longueur
        self.spin_len = QSpinBox()
        self.spin_len.setRange(1, 100)
        self.spin_len.setValue(12)
        self.spin_len.valueChanged.connect(self.on_length_changed)
        layout.addRow("Longueur :", self.spin_len)

        # Options de caractères
        self.cb_upper = QCheckBox("Majuscules")
        self.cb_upper.setChecked(True)
        self.cb_upper.stateChanged.connect(self.on_upper_changed)
        layout.addRow(self.cb_upper)

        self.cb_digits = QCheckBox("Chiffres")
        self.cb_digits.setChecked(True)
        self.cb_digits.stateChanged.connect(self.on_digits_changed)
        layout.addRow(self.cb_digits)

        self.cb_symbols = QCheckBox("Symboles")
        self.cb_symbols.setChecked(True)
        self.cb_symbols.stateChanged.connect(self.on_symbols_changed)
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

        # Historique
        self.history_label = QLabel("Historique : 0 mots de passe générés")
        self.history_label.setStyleSheet("QLabel { color: gray; font-size: 10px; }")
        layout.addRow(self.history_label)

    def on_length_changed(self, value):
        """Gestionnaire du changement de longueur"""
        self.password_generator.set_length(value)
    
    def on_upper_changed(self, state):
        """Gestionnaire du changement d'option majuscules"""
        self.password_generator.set_use_upper(state == Qt.Checked)
    
    def on_digits_changed(self, state):
        """Gestionnaire du changement d'option chiffres"""
        self.password_generator.set_use_digits(state == Qt.Checked)
    
    def on_symbols_changed(self, state):
        """Gestionnaire du changement d'option symboles"""
        self.password_generator.set_use_symbols(state == Qt.Checked)

    def on_generate(self):
        """Génère un nouveau mot de passe"""
        password = self.password_generator.generate_password()
        
        if not password:
            QMessageBox.warning(self, "Erreur", "Aucun caractère sélectionné.")

    def update_password_display(self):
        """Met à jour l'affichage du mot de passe"""
        self.edit_res.setText(self.password_generator.current_password)
        
        # Mise à jour de l'historique
        history_count = self.password_generator.get_history_count()
        self.history_label.setText(f"Historique : {history_count} mots de passe générés")

    def update_security_indicator(self):
        """Met à jour l'indicateur de sécurité"""
        password = self.password_generator.current_password
        if password:
            strength, color = evaluate_password_strength(password)
            self.security_label.setText(strength)
            self.security_label.setStyleSheet(f"QLabel {{ color: {color}; font-weight: bold; }}")
        else:
            self.security_label.setText("Aucun mot de passe généré")
            self.security_label.setStyleSheet("QLabel { color: gray; font-weight: bold; }")

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
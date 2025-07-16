"""
Interface graphique pour le générateur de mots de passe sécurisés.

Ce module contient la classe PassGen qui implémente l'interface utilisateur
principale de l'application. Il utilise PyQt5 pour créer une interface
intuitive permettant de générer des mots de passe personnalisés.

Classes:
    PassGen: Fenêtre principale de l'application

Dépendances:
    - PyQt5 (installé automatiquement si nécessaire)
    - password_utils (module local)

Auteur: Assistant Claude
Version: 1.0
"""

import sys
import subprocess
import importlib


def import_with_auto_install(pkg):
    """
    Importe un package Python et l'installe automatiquement si nécessaire.

    Cette fonction tente d'importer un package. Si l'importation échoue
    (ImportError), elle installe automatiquement le package via pip
    puis tente à nouveau l'importation.

    Args:
        pkg (str): Nom du package à importer

    Returns:
        module: Le module importé

    Raises:
        ImportError: Si l'importation échoue même après l'installation
        subprocess.CalledProcessError: Si l'installation pip échoue
    """
    try:
        return importlib.import_module(pkg)
    except ImportError:
        print(f"Installation de {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        return importlib.import_module(pkg)


# Installation automatique de PyQt5 si nécessaire
import_with_auto_install("PyQt5")

from PyQt5.QtWidgets import (
    QWidget,
    QFormLayout,
    QSpinBox,
    QCheckBox,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QLabel,
    QApplication,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from password_utils import evaluate_password_strength, Observer, PasswordGenerator


class PassGen(QWidget):
    """
    Interface graphique principale pour le générateur de mots de passe.

    Cette classe hérite de QWidget pour créer une fenêtre et implémente
    le pattern Observer pour réagir aux changements du générateur de
    mots de passe.

    Attributes:
        password_generator (PasswordGenerator): Instance du générateur
        spin_len (QSpinBox): Contrôle pour la longueur du mot de passe
        cb_upper (QCheckBox): Option pour les majuscules
        cb_digits (QCheckBox): Option pour les chiffres
        cb_symbols (QCheckBox): Option pour les symboles
        edit_res (QLineEdit): Affichage du mot de passe généré
        security_label (QLabel): Indicateur de sécurité
        history_label (QLabel): Compteur de l'historique
    """

    def __init__(self):
        """
        Initialise l'interface graphique du générateur de mots de passe.

        Cette méthode :
        1. Appelle les constructeurs parents
        2. Crée une instance du générateur de mots de passe
        3. S'abonne aux notifications du générateur (pattern Observer)
        4. Initialise l'interface utilisateur
        5. Met à jour l'affichage initial
        """
        super().__init__()

        # Initialisation du générateur de mots de passe
        self.password_generator = PasswordGenerator()

        # Abonnement aux changements du générateur (pattern Observer)
        self.password_generator.attach(self)

        # Construction de l'interface utilisateur
        self.init_ui()

        # Mise à jour de l'affichage initial
        self.update_password_display()
        self.update_security_indicator()

    def update(self, subject):
        """
        Méthode du pattern Observer - appelée quand le générateur change.

        Cette méthode est automatiquement appelée par le générateur de
        mots de passe chaque fois qu'un paramètre change, permettant
        une mise à jour en temps réel de l'interface.

        Args:
            subject (Observable): L'objet qui a notifié le changement
        """
        if isinstance(subject, PasswordGenerator):
            self.update_password_display()
            self.update_security_indicator()

    def init_ui(self):
        """
        Initialise tous les éléments de l'interface utilisateur.

        Cette méthode crée et configure tous les widgets de l'interface :
        - Contrôles de paramètres (longueur, options)
        - Boutons d'action (générer, copier)
        - Affichages d'information (mot de passe, sécurité, historique)
        """
        # Configuration de la fenêtre principale
        self.setWindowTitle("Générateur de mot de passe")
        self.setFixedSize(450, 300)
        layout = QFormLayout(self)

        # === CONTRÔLES DE PARAMÈTRES ===

        # Contrôle de la longueur du mot de passe
        self.spin_len = QSpinBox()
        self.spin_len.setRange(1, 101)  # Longueur entre 1 et 101 caractères
        self.spin_len.setValue(12)  # Valeur par défaut recommandée
        self.spin_len.setToolTip(
            "Longueur du mot de passe (recommandé : 12+ caractères)"
        )
        self.spin_len.valueChanged.connect(self.on_length_changed)
        layout.addRow("Longueur :", self.spin_len)

        # Option pour inclure les majuscules (A-Z)
        self.cb_upper = QCheckBox("Majuscules (A-Z)")
        self.cb_upper.setChecked(True)
        self.cb_upper.setToolTip("Inclure les lettres majuscules dans le mot de passe")
        self.cb_upper.stateChanged.connect(self.on_upper_changed)
        layout.addRow(self.cb_upper)

        # Option pour inclure les chiffres (0-9)
        self.cb_digits = QCheckBox("Chiffres (0-9)")
        self.cb_digits.setChecked(True)
        self.cb_digits.setToolTip("Inclure les chiffres dans le mot de passe")
        self.cb_digits.stateChanged.connect(self.on_digits_changed)
        layout.addRow(self.cb_digits)

        # Option pour inclure les symboles (!@#$%^&*)
        self.cb_symbols = QCheckBox("Symboles (!@#$%^&*)")
        self.cb_symbols.setChecked(True)
        self.cb_symbols.setToolTip(
            "Inclure les symboles de ponctuation dans le mot de passe"
        )
        self.cb_symbols.stateChanged.connect(self.on_symbols_changed)
        layout.addRow(self.cb_symbols)

        # === BOUTONS D'ACTION ===

        # Bouton pour générer un nouveau mot de passe
        btn_gen = QPushButton("Générer")
        btn_gen.setToolTip(
            "Générer un nouveau mot de passe avec les paramètres actuels"
        )
        btn_gen.clicked.connect(self.on_generate)
        layout.addRow(btn_gen)

        # === AFFICHAGES D'INFORMATION ===

        # Champ d'affichage du mot de passe généré (lecture seule)
        self.edit_res = QLineEdit()
        self.edit_res.setReadOnly(True)
        self.edit_res.setToolTip(
            "Mot de passe généré (cliquez sur Copier pour le copier)"
        )
        layout.addRow("Mot de passe :", self.edit_res)

        # Bouton pour copier le mot de passe dans le presse-papiers
        btn_copy = QPushButton("Copier")
        btn_copy.setToolTip("Copier le mot de passe dans le presse-papiers")
        btn_copy.clicked.connect(self.on_copy)
        layout.addRow(btn_copy)

        # Indicateur de sécurité du mot de passe
        self.security_label = QLabel("Aucun mot de passe généré")
        self.security_label.setStyleSheet("QLabel { color: gray; font-weight: bold; }")
        self.security_label.setWordWrap(True)
        self.security_label.setToolTip(
            "Estimation du temps nécessaire pour craquer le mot de passe"
        )
        layout.addRow("Temps de crack :", self.security_label)

        # Compteur de l'historique des mots de passe générés
        self.history_label = QLabel("Historique : 0 mots de passe générés")
        self.history_label.setStyleSheet("QLabel { color: gray; font-size: 10px; }")
        self.history_label.setToolTip(
            "Nombre total de mots de passe générés dans cette session"
        )
        layout.addRow(self.history_label)

    # === GESTIONNAIRES D'ÉVÉNEMENTS ===

    def on_length_changed(self, value):
        """
        Gestionnaire du changement de longueur du mot de passe.

        Args:
            value (int): Nouvelle longueur sélectionnée
        """
        self.password_generator.set_length(value)

    def on_upper_changed(self, state):
        """
        Gestionnaire du changement d'option majuscules.

        Args:
            state (int): État de la case à cocher (0=non coché, 2=coché)
        """
        self.password_generator.set_use_upper(state == 2)  # 2 = Qt.CheckState.Checked

    def on_digits_changed(self, state):
        """
        Gestionnaire du changement d'option chiffres.

        Args:
            state (int): État de la case à cocher (0=non coché, 2=coché)
        """
        self.password_generator.set_use_digits(state == 2)  # 2 = Qt.CheckState.Checked

    def on_symbols_changed(self, state):
        """
        Gestionnaire du changement d'option symboles.

        Args:
            state (int): État de la case à cocher (0=non coché, 2=coché)
        """
        self.password_generator.set_use_symbols(state == 2)  # 2 = Qt.CheckState.Checked

    def on_generate(self):
        """
        Génère un nouveau mot de passe avec les paramètres actuels.

        Cette méthode appelle le générateur pour créer un nouveau mot de passe.
        Si aucun type de caractère n'est sélectionné, elle affiche un message
        d'erreur à l'utilisateur.
        """
        password = self.password_generator.generate_password()

        if not password:
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucun type de caractère sélectionné.\n"
                "Veuillez cocher au moins une option (majuscules, chiffres ou symboles).",
            )

    def update_password_display(self):
        """
        Met à jour l'affichage du mot de passe et du compteur d'historique.

        Cette méthode est appelée automatiquement via le pattern Observer
        chaque fois qu'un nouveau mot de passe est généré.
        """
        # Mise à jour du champ d'affichage du mot de passe
        self.edit_res.setText(self.password_generator.current_password)

        # Mise à jour du compteur d'historique
        history_count = self.password_generator.get_history_count()
        self.history_label.setText(
            f"Historique : {history_count} mots de passe générés"
        )

    def update_security_indicator(self):
        """
        Met à jour l'indicateur de sécurité du mot de passe.

        Cette méthode évalue la robustesse du mot de passe actuel et
        affiche une estimation du temps nécessaire pour le craquer
        avec une couleur correspondant au niveau de sécurité.
        """
        password = self.password_generator.current_password

        if password:
            # Évaluation de la sécurité du mot de passe
            strength, color = evaluate_password_strength(password)
            self.security_label.setText(strength)
            self.security_label.setStyleSheet(
                f"QLabel {{ color: {color}; font-weight: bold; }}"
            )
        else:
            # Aucun mot de passe généré
            self.security_label.setText("Aucun mot de passe généré")
            self.security_label.setStyleSheet(
                "QLabel { color: gray; font-weight: bold; }"
            )

    def on_copy(self):
        """
        Copie le mot de passe actuel dans le presse-papiers système.

        Cette méthode vérifie qu'un mot de passe existe, puis le copie
        dans le presse-papiers et affiche un message de confirmation.
        En cas d'erreur, elle affiche un message d'erreur approprié.
        """
        pwd = self.edit_res.text()

        if pwd:
            # Accès au presse-papiers système
            clipboard = QApplication.clipboard()

            if clipboard is not None:
                # Copie du mot de passe
                clipboard.setText(pwd)
                QMessageBox.information(
                    self,
                    "Copié",
                    "Mot de passe copié dans le presse-papiers.\n"
                    "Vous pouvez maintenant le coller (Ctrl+V) où vous le souhaitez.",
                )
            else:
                # Erreur d'accès au presse-papiers
                QMessageBox.warning(
                    self, "Erreur", "Impossible d'accéder au presse-papiers système."
                )
        else:
            # Aucun mot de passe à copier
            QMessageBox.warning(
                self,
                "Erreur",
                "Aucun mot de passe à copier.\n"
                "Veuillez d'abord générer un mot de passe.",
            )

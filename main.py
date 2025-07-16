#!/usr/bin/env python3
"""
Générateur de mots de passe sécurisés avec interface graphique PyQt5.

Ce module contient le point d'entrée principal de l'application de génération
de mots de passe. Il initialise l'application PyQt5 et lance l'interface
utilisateur principale.

Fonctionnalités principales :
- Interface graphique intuitive
- Génération de mots de passe personnalisables
- Évaluation de la sécurité en temps réel
- Historique des mots de passe générés
- Copie automatique vers le presse-papiers

Auteur: Assistant Claude
Version: 1.0
Licence: MIT
"""

import sys
from PyQt5.QtWidgets import QApplication
from password_gui import PassGen


def main():
    """
    Fonction principale pour lancer l'application de génération de mots de passe.

    Cette fonction :
    1. Crée une instance de QApplication
    2. Instancie la fenêtre principale PassGen
    3. Affiche la fenêtre
    4. Démarre la boucle d'événements Qt

    Returns:
        None

    Raises:
        SystemExit: Quand l'application se ferme normalement
    """
    # Création de l'application Qt
    app = QApplication(sys.argv)

    # Configuration de l'application
    app.setApplicationName("Générateur de Mots de Passe")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Assistant Claude")

    # Création et affichage de la fenêtre principale
    window = PassGen()
    window.show()

    # Démarrage de la boucle d'événements Qt
    # Cette ligne bloque jusqu'à ce que l'application se ferme
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

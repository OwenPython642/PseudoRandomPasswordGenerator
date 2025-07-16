#!/usr/bin/env python3
"""
Générateur de mots de passe sécurisés avec interface graphique
Auteur: Assistant Claude
"""

import sys
from PyQt5.QtWidgets import QApplication
from password_gui import PassGen

def main():
    """Fonction principale pour lancer l'application"""
    app = QApplication(sys.argv)
    
    # Création et affichage de la fenêtre principale
    window = PassGen()
    window.show()
    
    # Démarrage de la boucle d'événements
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
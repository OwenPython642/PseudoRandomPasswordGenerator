# 🔐 Générateur de Mots de Passe Sécurisés

Une application de bureau moderne avec interface graphique pour générer des mots de passe cryptographiquement sécurisés, développée en Python avec PyQt5.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)

## 🌟 Fonctionnalités

### 🎯 Génération de Mots de Passe
- **Longueur personnalisable** : De 1 à 100 caractères
- **Types de caractères configurables** :
  - Lettres minuscules (a-z) - toujours incluses
  - Lettres majuscules (A-Z)
  - Chiffres (0-9)
  - Symboles de ponctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
- **Génération cryptographiquement sécurisée** utilisant le module `secrets`

### 🛡️ Évaluation de Sécurité
- **Analyse en temps réel** de la robustesse du mot de passe
- **Estimation du temps de craquage** par force brute
- **Classification visuelle** avec codes couleur :
  - 🔴 **Faible** : < 1 jour
  - 🟠 **Moyenne** : 1 jour à 1 an
  - 🟢 **Forte** : > 1 an

### 💡 Interface Utilisateur
- **Interface graphique intuitive** avec PyQt5
- **Mise à jour en temps réel** des paramètres
- **Copie facile** vers le presse-papiers
- **Historique** des mots de passe générés
- **Tooltips informatifs** sur tous les éléments

## 🚀 Installation

### Prérequis
- Python 3.6 ou supérieur
- Système d'exploitation : Windows, macOS, ou Linux

### Installation automatique
L'application installe automatiquement PyQt5 si nécessaire lors du premier lancement.

### Installation manuelle (optionnelle)
```bash
pip install PyQt5
```

## 📥 Utilisation

### Lancement de l'application
```bash
python main.py
```

### Guide d'utilisation

1. **Configurer les paramètres** :
   - Ajustez la longueur du mot de passe (recommandé : 12+ caractères)
   - Sélectionnez les types de caractères souhaités
   - L'évaluation de sécurité se met à jour automatiquement

2. **Générer un mot de passe** :
   - Cliquez sur "Générer" pour créer un nouveau mot de passe
   - Le mot de passe apparaît dans le champ de résultat

3. **Utiliser le mot de passe** :
   - Cliquez sur "Copier" pour copier le mot de passe
   - Collez-le où vous le souhaitez (Ctrl+V / Cmd+V)

## 🏗️ Architecture

### Structure du projet
```
password-generator/
├── main.py              # Point d'entrée de l'application
├── password_gui.py      # Interface graphique (PyQt5)
├── password_utils.py    # Utilitaires et logique métier
└── README.md           # Documentation
```

### Composants principaux

#### 📱 `main.py`
- Point d'entrée de l'application
- Initialisation de l'interface PyQt5
- Gestion du cycle de vie de l'application

#### 🎨 `password_gui.py`
- Interface utilisateur avec PyQt5
- Implémentation du pattern Observer
- Gestion des événements utilisateur
- Installation automatique des dépendances

#### ⚙️ `password_utils.py`
- Génération cryptographique sécurisée
- Évaluation de la robustesse des mots de passe
- Calcul du temps de craquage estimé
- Pattern Observer pour les notifications

## 🎨 Patterns de Conception

### Observer Pattern
Le projet utilise le pattern Observer pour une architecture découplée :
- **Observable** : `PasswordGenerator` notifie les changements
- **Observer** : `PassGen` (interface) réagit aux changements
- **Avantages** : Mise à jour automatique, faible couplage

### Séparation des responsabilités
- **Interface** : `password_gui.py` gère l'affichage
- **Logique métier** : `password_utils.py` gère les calculs
- **Coordination** : `main.py` orchestre l'ensemble

## 🔒 Sécurité

### Génération cryptographique
- Utilisation du module `secrets` (cryptographiquement sécurisé)
- Pas de générateurs pseudo-aléatoires faibles
- Entropie élevée pour tous les mots de passe

### Évaluation de robustesse
- Calcul basé sur l'espace de caractères réel
- Estimation du temps de craquage par force brute
- Prise en compte des capacités d'attaque modernes

### Bonnes pratiques
- Pas de stockage permanent des mots de passe
- Effacement automatique à la fermeture
- Historique en mémoire uniquement

## 🛠️ Développement

### Dépendances
```python
# Dépendances principales
PyQt5>=5.0          # Interface graphique
secrets             # Génération cryptographique (standard)
string              # Manipulation de chaînes (standard)
```

### Extensions possibles
- **Exportation** de l'historique
- **Règles personnalisées** (exclusion de caractères)
- **Génération par lots** (multiples mots de passe)
- **Thèmes sombres** et personnalisation
- **Intégration** avec les gestionnaires de mots de passe

## 📊 Caractéristiques techniques

### Performance
- **Génération instantanée** même pour de longs mots de passe
- **Interface réactive** avec mise à jour en temps réel
- **Mémoire optimisée** avec gestion automatique

### Compatibilité
- **Python 3.6+** (utilisation de f-strings)
- **PyQt5** pour l'interface graphique
- **Multiplateforme** (Windows, macOS, Linux)

## 📝 Exemples d'utilisation

### Mot de passe standard (12 caractères)
```
Configuration : Longueur=12, Majuscules=✓, Chiffres=✓, Symboles=✓
Résultat : aB3$dE7&iJ9!
Sécurité : Forte (2.5e+15 années)
```

### Mot de passe simple (8 caractères, pas de symboles)
```
Configuration : Longueur=8, Majuscules=✓, Chiffres=✓, Symboles=✗
Résultat : aBc3dE7i
Sécurité : Moyenne (127 jours)
```

### Mot de passe ultra-sécurisé (20 caractères)
```
Configuration : Longueur=20, Majuscules=✓, Chiffres=✓, Symboles=✓
Résultat : aB3$dE7&iJ9!mN5%pQ8^
Sécurité : Forte (1.2e+32 années)
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. **Créez** une branche pour votre fonctionnalité
3. **Commitez** vos changements
4. **Pushez** vers la branche
5. **Ouvrez** une Pull Request

### Guidelines de contribution
- Respectez les conventions de nommage Python (PEP 8)
- Ajoutez des docstrings pour toutes les fonctions
- Testez vos modifications sur plusieurs plateformes
- Maintenez la compatibilité avec Python 3.6+

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **PyQt5** pour l'excellent framework d'interface graphique
- **Python Software Foundation** pour le langage et les outils
- **Communauté Python** pour les bonnes pratiques et ressources

## 📞 Support

Pour toute question ou problème :
- Ouvrez une **issue** sur le projet
- Consultez la **documentation** intégrée
- Vérifiez les **prérequis** système

---

*Développé avec ❤️ par Assistant Claude*
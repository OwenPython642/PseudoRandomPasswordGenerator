"""
Utilitaires pour la génération et l'évaluation de mots de passe sécurisés.

Ce module contient les fonctions et classes nécessaires pour :
- Générer des mots de passe cryptographiquement sécurisés
- Évaluer la robustesse des mots de passe
- Calculer le temps estimé de craquage par force brute
- Implémenter le pattern Observer pour les notifications

Classes:
    Observer: Interface pour le pattern Observer
    Observable: Classe de base pour les objets observables
    PasswordGenerator: Générateur de mots de passe avec notifications

Fonctions:
    generate_password: Génère un mot de passe sécurisé
    calculate_brute_force_time: Calcule le temps de craquage estimé
    format_time: Formate le temps en unités lisibles
    evaluate_password_strength: Évalue la robustesse d'un mot de passe

Auteur: Assistant Claude
Version: 1.0
"""

import string
import secrets
from abc import ABC, abstractmethod


def generate_password(length, use_upper, use_digits, use_symbols):
    """
    Génère un mot de passe cryptographiquement sécurisé.

    Cette fonction utilise le module `secrets` pour générer un mot de passe
    aléatoire sécurisé en respectant les critères spécifiés.

    Args:
        length (int): Longueur du mot de passe à générer
        use_upper (bool): Inclure les majuscules (A-Z)
        use_digits (bool): Inclure les chiffres (0-9)
        use_symbols (bool): Inclure les symboles de ponctuation

    Returns:
        str: Mot de passe généré, ou chaîne vide si aucun caractère disponible

    Example:
        >>> generate_password(12, True, True, False)
        'aB3dEf9hIjKl'
        >>> generate_password(8, False, False, False)
        'abcdefgh'
    """
    # Construction du jeu de caractères disponibles
    chars = string.ascii_lowercase  # Minuscules toujours incluses

    if use_upper:
        chars += string.ascii_uppercase  # A-Z
    if use_digits:
        chars += string.digits  # 0-9
    if use_symbols:
        chars += string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

    # Génération sécurisée du mot de passe
    if chars:
        return "".join(secrets.choice(chars) for _ in range(length))
    else:
        return ""  # Aucun caractère disponible


def calculate_brute_force_time(password):
    """
    Calcule le temps estimé pour craquer un mot de passe par force brute.

    Cette fonction estime le temps nécessaire pour craquer un mot de passe
    en utilisant une attaque par force brute, basée sur :
    - L'espace de caractères utilisé
    - La longueur du mot de passe
    - Une vitesse d'attaque moderne estimée

    Args:
        password (str): Mot de passe à analyser

    Returns:
        tuple: (temps_en_secondes, temps_formaté)
            - temps_en_secondes (float): Temps moyen en secondes
            - temps_formaté (str): Temps formaté en unités lisibles

    Example:
        >>> calculate_brute_force_time("abc123")
        (0.000018, "< 1 seconde")
        >>> calculate_brute_force_time("MyStr0ng!P@ssw0rd")
        (1.23e+25, "3.9e+17 années")
    """
    if not password:
        return 0, "Aucun"

    # === DÉTERMINATION DE L'ESPACE DE CARACTÈRES ===

    charset_size = 0
    has_lower = any(c.islower() for c in password)  # a-z
    has_upper = any(c.isupper() for c in password)  # A-Z
    has_digit = any(c.isdigit() for c in password)  # 0-9
    has_symbol = any(c in string.punctuation for c in password)  # Symboles

    # Calcul de la taille de l'espace de caractères
    if has_lower:
        charset_size += 26  # Lettres minuscules
    if has_upper:
        charset_size += 26  # Lettres majuscules
    if has_digit:
        charset_size += 10  # Chiffres
    if has_symbol:
        charset_size += 32  # Approximation des symboles courants

    # === CALCUL DU TEMPS DE CRAQUAGE ===

    # Nombre total de combinaisons possibles
    length = len(password)
    total_combinations = charset_size**length

    # Temps moyen = la moitié des combinaisons possibles
    # (en moyenne, la bonne combinaison est trouvée à mi-parcours)
    # Vitesse d'attaque moderne estimée : 1 milliard de tentatives/seconde
    attempts_per_second = 1_000_000_000
    average_time_seconds = total_combinations / (2 * attempts_per_second)

    return average_time_seconds, format_time(average_time_seconds)


def format_time(seconds):
    """
    Formate un temps en secondes en unités lisibles.

    Cette fonction convertit une durée en secondes vers l'unité
    la plus appropriée pour l'affichage (secondes, minutes, heures, etc.).

    Args:
        seconds (float): Durée en secondes

    Returns:
        str: Durée formatée avec l'unité appropriée

    Example:
        >>> format_time(30)
        "30 secondes"
        >>> format_time(3600)
        "1 heures"
        >>> format_time(86400)
        "1 jours"
    """
    if seconds < 1:
        return "< 1 seconde"
    elif seconds < 60:
        return f"{int(seconds)} secondes"
    elif seconds < 3600:  # 60 * 60
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:  # 60 * 60 * 24
        return f"{int(seconds/3600)} heures"
    elif seconds < 31536000:  # 60 * 60 * 24 * 365
        return f"{int(seconds/86400)} jours"
    elif seconds < 31536000000:  # 1000 ans
        return f"{int(seconds/31536000)} années"
    else:
        # Notation scientifique pour les très grandes valeurs
        return f"{seconds/31536000:.1e} années"


def evaluate_password_strength(password):
    """
    Évalue la robustesse d'un mot de passe basée sur le temps de craquage.

    Cette fonction classe la robustesse d'un mot de passe en trois catégories
    selon le temps estimé nécessaire pour le craquer par force brute.

    Args:
        password (str): Mot de passe à évaluer

    Returns:
        tuple: (description, couleur)
            - description (str): Description de la robustesse avec temps
            - couleur (str): Couleur CSS pour l'affichage

    Classification:
        - Faible: < 1 jour (rouge)
        - Moyenne: 1 jour à 1 an (orange)
        - Forte: > 1 an (vert)

    Example:
        >>> evaluate_password_strength("123456")
        ("Faible (< 1 seconde)", "red")
        >>> evaluate_password_strength("MyStr0ng!P@ssw0rd")
        ("Forte (3.9e+17 années)", "green")
    """
    if not password:
        return "Aucun", "red"

    # Calcul du temps de craquage estimé
    time_seconds, time_str = calculate_brute_force_time(password)

    # === CLASSIFICATION DE LA ROBUSTESSE ===

    if time_seconds < 86400:  # Moins d'un jour
        return f"Faible ({time_str})", "red"
    elif time_seconds < 31536000:  # Moins d'un an
        return f"Moyenne ({time_str})", "orange"
    else:  # Plus d'un an
        return f"Forte ({time_str})", "green"


# === PATTERN OBSERVER ===


class Observer(ABC):
    """
    Interface abstraite pour le pattern Observer.

    Cette classe définit l'interface que doivent implémenter tous les
    observateurs qui souhaitent être notifiés des changements d'un objet Observable.
    """

    @abstractmethod
    def update(self, subject):
        """
        Méthode appelée lors d'une notification de changement.

        Cette méthode doit être implémentée par toutes les classes
        qui héritent de Observer.

        Args:
            subject (Observable): L'objet qui a notifié le changement
        """
        pass


class Observable:
    """
    Classe de base pour les objets observables (pattern Observer).

    Cette classe permet à un objet de notifier automatiquement
    une liste d'observateurs lorsque son état change.

    Attributes:
        _observers (list): Liste des observateurs abonnés
    """

    def __init__(self):
        """Initialise la liste des observateurs."""
        self._observers = []

    def attach(self, observer):
        """
        Ajoute un observateur à la liste de notification.

        Args:
            observer (Observer): L'observateur à ajouter
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Retire un observateur de la liste de notification.

        Args:
            observer (Observer): L'observateur à retirer
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """
        Notifie tous les observateurs abonnés d'un changement.

        Cette méthode appelle la méthode update() de chaque observateur.
        """
        for observer in self._observers:
            observer.update(self)


class PasswordGenerator(Observable):
    """
    Générateur de mots de passe avec notifications automatiques.

    Cette classe génère des mots de passe selon des critères configurables
    et notifie automatiquement les observateurs de tout changement via
    le pattern Observer.

    Attributes:
        length (int): Longueur du mot de passe (défaut: 12)
        use_upper (bool): Inclure les majuscules (défaut: True)
        use_digits (bool): Inclure les chiffres (défaut: True)
        use_symbols (bool): Inclure les symboles (défaut: True)
        current_password (str): Dernier mot de passe généré
        history (list): Historique des mots de passe générés
    """

    def __init__(self):
        """
        Initialise le générateur avec les paramètres par défaut.

        Paramètres par défaut recommandés pour la sécurité :
        - Longueur: 12 caractères
        - Majuscules: activées
        - Chiffres: activés
        - Symboles: activés
        """
        super().__init__()

        # Paramètres de génération
        self.length = 12
        self.use_upper = True
        self.use_digits = True
        self.use_symbols = True

        # État du générateur
        self.current_password = ""
        self.history = []

    def set_length(self, length):
        """
        Définit la longueur du mot de passe et notifie les observateurs.

        Args:
            length (int): Nouvelle longueur (doit être > 0)
        """
        if length > 0:
            self.length = length
            self.notify()

    def set_use_upper(self, use_upper):
        """
        Active/désactive l'utilisation des majuscules.

        Args:
            use_upper (bool): True pour inclure les majuscules
        """
        self.use_upper = use_upper
        self.notify()

    def set_use_digits(self, use_digits):
        """
        Active/désactive l'utilisation des chiffres.

        Args:
            use_digits (bool): True pour inclure les chiffres
        """
        self.use_digits = use_digits
        self.notify()

    def set_use_symbols(self, use_symbols):
        """
        Active/désactive l'utilisation des symboles.

        Args:
            use_symbols (bool): True pour inclure les symboles
        """
        self.use_symbols = use_symbols
        self.notify()

    def generate_password(self):
        """
        Génère un nouveau mot de passe avec les paramètres actuels.

        Cette méthode vérifie qu'au moins un type de caractère est
        sélectionné, génère le mot de passe, l'ajoute à l'historique
        et notifie les observateurs.

        Returns:
            str: Mot de passe généré, ou chaîne vide si impossible
        """
        # Vérification qu'au moins un type de caractère est sélectionné
        # (les minuscules sont toujours incluses)
        if not any([True, self.use_upper, self.use_digits, self.use_symbols]):
            return ""

        # Génération du mot de passe
        password = generate_password(
            self.length, self.use_upper, self.use_digits, self.use_symbols
        )

        # Mise à jour de l'état si la génération a réussi
        if password:
            self.current_password = password
            self.history.append(password)
            self.notify()

        return password

    def get_history_count(self):
        """
        Retourne le nombre de mots de passe dans l'historique.

        Returns:
            int: Nombre de mots de passe générés depuis le lancement
        """
        return len(self.history)

    def get_history(self):
        """
        Retourne l'historique complet des mots de passe générés.

        Returns:
            list: Liste des mots de passe générés (copie pour sécurité)
        """
        return self.history.copy()

    def clear_history(self):
        """
        Efface l'historique des mots de passe générés.

        Cette méthode vide l'historique mais conserve le mot de passe
        actuel et notifie les observateurs.
        """
        self.history.clear()
        self.notify()

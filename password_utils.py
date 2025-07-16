import string
import secrets
from abc import ABC, abstractmethod

def generate_password(length, use_upper, use_digits, use_symbols):
    """Génère un mot de passe selon les critères spécifiés"""
    chars = string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length)) if chars else ""

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


# Pattern Observer
class Observer:
    """Interface pour le pattern Observer"""
    def update(self, subject):
        """Méthode à implémenter par les observateurs"""
        raise NotImplementedError("La méthode update doit être implémentée")

class Observable:
    """Classe de base pour les objets observables"""
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        """Ajoute un observateur"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Retire un observateur"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self):
        """Notifie tous les observateurs"""
        for observer in self._observers:
            observer.update(self)


class PasswordGenerator(Observable):
    """Générateur de mots de passe avec pattern Observer"""
    def __init__(self):
        super().__init__()
        self.length = 12
        self.use_upper = True
        self.use_digits = True
        self.use_symbols = True
        self.current_password = ""
        self.history = []
    
    def set_length(self, length):
        """Définit la longueur du mot de passe"""
        self.length = length
        self.notify()
    
    def set_use_upper(self, use_upper):
        """Définit l'utilisation des majuscules"""
        self.use_upper = use_upper
        self.notify()
    
    def set_use_digits(self, use_digits):
        """Définit l'utilisation des chiffres"""
        self.use_digits = use_digits
        self.notify()
    
    def set_use_symbols(self, use_symbols):
        """Définit l'utilisation des symboles"""
        self.use_symbols = use_symbols
        self.notify()
    
    def generate_password(self):
        """Génère un nouveau mot de passe"""
        if not any([True, self.use_upper, self.use_digits, self.use_symbols]):
            return ""
        
        password = generate_password(self.length, self.use_upper, self.use_digits, self.use_symbols)
        if password:
            self.current_password = password
            self.history.append(password)
            self.notify()
        return password
    
    def get_history_count(self):
        """Retourne le nombre de mots de passe dans l'historique"""
        return len(self.history)
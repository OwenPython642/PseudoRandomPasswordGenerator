import string
import secrets

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
# calculators/tdee.py

def calc_tdee(bmr, activity_level):
    """BMR'ı ve aktivite seviyesini alarak TDEE'yi hesaplar."""
    
    multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9,
    }
    
    # Gelen string'i sözlükte arar, bulamazsa varsayılan 1.2 kullanır.
    multiplier = multipliers.get(activity_level.lower(), 1.2)
    return bmr * multiplier
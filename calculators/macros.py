# calculators/macros.py

def macro_split(calorie_goal, protein_grams):
    """Kalori ve protein hedefini alarak makro dağılımını hesaplar."""
    
    # 1. Protein kalorisini bul (1g Protein = 4 kcal)
    protein_cal = protein_grams * 4
    
    # 2. Kalan kaloriyi bul
    remaining_cal = calorie_goal - protein_cal
    
    # 3. Yağ ve Karbonhidrat kalorilerini ayır
    fat_cal = remaining_cal * 0.25
    carb_cal = remaining_cal * 0.75
    
    # 4. Kaloriyi grama çevir (1g Yağ = 9 kcal, 1g Karb = 4 kcal)
    return {
        'protein_g': protein_grams,
        'fat_g': fat_cal / 9,
        'carb_g': carb_cal / 4
    }
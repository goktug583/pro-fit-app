def macro_split(calorie_goal, protein_grams):
    """Kalori ve protein hedefini alarak makro dağılımını hesaplar."""
    
   
    protein_cal = protein_grams * 4
    
    
    remaining_cal = calorie_goal - protein_cal
    
    
    fat_cal = remaining_cal * 0.25
    carb_cal = remaining_cal * 0.75
    
   
    return {
        'protein_g': protein_grams,
        'fat_g': fat_cal / 9,
        'carb_g': carb_cal / 4
    }
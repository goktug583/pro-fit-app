def calc_fat_percentage(bmi, age, gender):
    """
    BMI, yaş ve cinsiyete dayalı Vücut Yağ Yüzdesini tahmin eder
    (Deurenberg formülünün bir varyasyonu).
    """
    
   
    gender_factor = 1 if gender.lower() == 'male' else 0
    
   
    bfp = (1.20 * bmi) + (0.23 * age) - (10.85 * gender_factor) - 5.4
    
  
    return max(0, bfp)
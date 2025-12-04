# calculators/fat_percentage.py
def calc_fat_percentage(bmi, age, gender):
    """
    BMI, yaş ve cinsiyete dayalı Vücut Yağ Yüzdesini tahmin eder
    (Deurenberg formülünün bir varyasyonu).
    """
    
    # Cinsiyet için katsayı: Erkek=1, Kadın=0
    gender_factor = 1 if gender.lower() == 'male' else 0
    
    # Formül: (1.20 * BMI) + (0.23 * Yaş) - (10.85 * Cinsiyet Faktörü) - 5.4
    # Bu formül, yüksek BMI'ın kas mı yoksa yağ mı olduğunu ayırmaya yardımcı olur.
    bfp = (1.20 * bmi) + (0.23 * age) - (10.85 * gender_factor) - 5.4
    
    # Yağ oranı %0'dan az olamaz
    return max(0, bfp)
# calculators/bmi.py

def calc_bmi(weight, height):
    # Fonksiyonun görevi: BMI'yı hesapla
    # weight (kg) ve height (m) verilerini kullan
    
    # Boyun karesini (Boy * Boy) hesapla
    height_squared = height ** 2
    
    # BMI formülünü uygula
    bmi = weight / height_squared
    
    # Sonucu geri döndür
    return bmi

# Bu kadarı yeterli, dosyayı kaydedin (Ctrl + S)
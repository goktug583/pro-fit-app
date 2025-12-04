# calculators/bmr.py

def calc_bmr(weight, height, age, gender):
    
    # İlk Kural: Boyu metreden santimetreye çevir (Çünkü formül cm ister)
    height_cm = height * 100
    
    # İkinci Kural: Cinsiyet kontrolü (Karar Verme Mantığı: IF / ELSE)
    if gender.lower() == 'male': # Gelen metni küçük harfe çevirip kontrol et
        # Erkek formülü
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
        
    else: # Eğer erkek değilse (Kadın varsayılır)
        # Kadın formülü
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161
    
    return bmr

# Bu kadarı yeterli, dosyayı kaydedin (Ctrl + S)
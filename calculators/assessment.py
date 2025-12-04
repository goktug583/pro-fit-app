def assess_risk(bmi, navy_body_fat, activity):
    # KODUN ÇALIŞTIĞINI KANITLAYAN İMZA
    print(f"--- ANALİZ MODÜLÜ DEVREDE (BMI: {bmi}, YAĞ: {navy_body_fat}) ---")

    # --- DURUM 1: KULLANICI ÖLÇÜ GİRDİ (Navy Metodu) ---
    if navy_body_fat > 0:
        fat_percentage = navy_body_fat
        origin = "Navy Metodu (Gerçek)"
        
        if fat_percentage < 6: status = "Yarışma Formu"
        elif 6 <= fat_percentage < 14: status = "Atletik / Fit"
        elif 14 <= fat_percentage < 18: status = "Fitness (Sağlıklı)"
        elif 18 <= fat_percentage < 25: status = "Ortalama"
        else: status = "Yağlı"

        # Kaslı mı?
        if bmi > 25 and fat_percentage < 18:
            final_verdict = "SONUÇ: Kaslı/Atletik Vücut (BMI Yoksayıldı)"
            bmi_comment = f"BMI ({bmi:.2f}) yüksek ama ölçüleriniz kaslı olduğunuzu kanıtladı."
        else:
            final_verdict = f"SONUÇ: {status}"
            bmi_comment = f"Ölçümlerinize göre vücut durumunuz: {status}"

    # --- DURUM 2: KULLANICI ÖLÇÜ GİRMEDİ (Sadece BMI) ---
    else:
        origin = "BMI (Tahmini)"
        fat_percentage = (1.20 * bmi) + (0.23 * 25) - 16.2 

        if bmi < 18.5: final_verdict = "SONUÇ: Zayıf"
        elif 18.5 <= bmi < 25.0: final_verdict = "SONUÇ: Normal"
        elif 25.0 <= bmi < 30.0: final_verdict = "SONUÇ: Aşırı Kilolu (Ölçü Girilmedi)"
        else: final_verdict = "SONUÇ: Obezite"
            
        bmi_comment = "Mezura ölçüleri girilmediği için sadece BMI dikkate alındı."

    return {
        'fat_pct': fat_percentage,
        'status': final_verdict, 
        'bmi_comment': bmi_comment,
        'final_verdict': final_verdict,
        'origin': origin,
        'bmi_risk': final_verdict,
        'overall_assessment': bmi_comment
    }
from flask import Flask, render_template, request
import math

app = Flask(__name__)

# --- HESAPLAMA MOTORU ---

def calc_bmi(weight, height):
    if height <= 0: return 0
    return weight / (height ** 2)

def calc_bmr(weight, height, age, gender):
    height_cm = height * 100
    if gender.lower() == 'male':
        return 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height_cm - 5 * age - 161

def calc_tdee(bmr, activity_level):
    multipliers = {
        'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55,
        'active': 1.725, 'very_active': 1.9
    }
    return bmr * multipliers.get(activity_level.lower(), 1.2)

def calorie_target(tdee, goal):
    if goal == 'lose': return tdee - 400
    if goal == 'gain': return tdee + 300
    if goal == 'recomp': return tdee
    if goal == 'strength': return tdee + 100
    return tdee

def protein_target(weight):
    return weight * 1.8

def macro_split(calorie_goal, protein_grams):
    protein_cal = protein_grams * 4
    remaining = calorie_goal - protein_cal
    return {
        'protein_g': protein_grams,
        'fat_g': (remaining * 0.25) / 9,
        'carb_g': (remaining * 0.75) / 4
    }

def calc_navy_body_fat(waist, neck, height, gender):
    if not waist or not neck or waist == 0 or neck == 0: 
        return 0
    
    height_cm = height * 100
    if gender.lower() == 'male':
        if waist - neck <= 0: return 0 
        log_wn = math.log10(waist - neck)
        log_h = math.log10(height_cm)
        return 495 / (1.0324 - 0.19077 * log_wn + 0.15456 * log_h) - 450
    else:
        # Kadınlar için basit Navy formülü (Kalçasız versiyonu - yaklaşık)
        if waist - neck <= 0: return 0
        log_wn = math.log10(waist - neck) # Kadınlarda kalça da gerekir ama şimdilik basitleştirilmiş
        log_h = math.log10(height_cm)
        # Bu sadece placeholder, kadınlar için kalça ölçüsü şarttır.
        return 0

def assess_risk_internal(bmi, navy_body_fat):
    # 1. DURUM: Kullanıcı Ölçü GİRDİ (Navy > 0)
    if navy_body_fat > 0:
        fat_pct = navy_body_fat
        origin = "Navy Metodu (Gerçek)"
        
        if fat_pct < 6: status = "Yarışma Formu"
        elif 6 <= fat_pct < 14: status = "Atletik / Fit"
        elif 14 <= fat_pct < 18: status = "Fitness"
        elif 18 <= fat_pct < 25: status = "Ortalama"
        else: status = "Yağlı"

        # KASLI MI KONTROLÜ
        if bmi > 25 and fat_pct < 18:
            verdict = "SONUÇ: Kaslı/Atletik (BMI Geçersiz)"
            comment = f"BMI ({bmi:.2f}) yüksek ama ölçüleriniz fit olduğunuzu kanıtlıyor."
        else:
            verdict = f"SONUÇ: {status}"
            comment = f"Ölçümlerinize göre durumunuz: {status}"
            
    # 2. DURUM: Kullanıcı Ölçü GİRMEDİ (Sadece BMI Analizi)
    else:
        origin = "BMI (Tahmini)"
        # Göstergelik tahmin (Sadece ekranda boş kalmasın diye)
        fat_pct = (1.20 * bmi) + (0.23 * 25) - 16.2 
        
        # BMI Sınıflandırması ve Yorumu
        if bmi < 18.5: 
            verdict = "SONUÇ: Zayıf"
            comment = "Kilonuz boyunuza göre düşük. Sağlıklı kilo alımı için kalori fazlası oluşturmalısınız."
        elif 18.5 <= bmi < 25.0: 
            verdict = "SONUÇ: Normal"
            comment = "İdeal kilonuzdasınız. Formunuzu korumak veya kas kütlesi eklemek için antrenman yapabilirsiniz."
        elif 25.0 <= bmi < 30.0: 
            verdict = "SONUÇ: Hafif Kilolu"
            comment = "Kilonuz idealin biraz üzerinde. Eğer spor yapmıyorsanız yağ yakımına odaklanabilirsiniz. Sporcuysanız bu sonuç yanıltıcı olabilir."
        elif 30.0 <= bmi < 35.0:
            verdict = "SONUÇ: Obezite (1. Derece)"
            comment = "Sağlık riskleri artmaya başlıyor. Kontrollü bir diyet ve egzersiz planı önerilir."
        else: 
            verdict = "SONUÇ: Obezite (İleri Derece)"
            comment = "Ciddi sağlık riskleri olabilir. Bir uzman eşliğinde kilo vermeniz tavsiye edilir."
        
    return {'fat_pct': fat_pct, 'final_verdict': verdict, 'bmi_comment': comment}

# --- FLASK ---

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Verileri güvenli şekilde al
        weight_input = request.form.get('weight', '')
        height_input = request.form.get('height', '')
        
        if not weight_input or not height_input:
            return render_template('index.html', error_message="Lütfen Kilo ve Boy giriniz.")

        weight = float(weight_input)
        height = float(height_input)
        
        # --- AKILLI BOY DÜZELTME ---
        if height > 3: 
            height = height / 100
            
        age = int(request.form.get('age', 25))
        gender = request.form.get('gender', 'male')
        activity = request.form.get('activity', 'sedentary')
        goal = request.form.get('goal', 'lose')
        
        # Opsiyonel Alanlar
        try:
            neck_val = request.form.get('neck')
            waist_val = request.form.get('waist')
            neck = float(neck_val) if neck_val else 0
            waist = float(waist_val) if waist_val else 0
        except:
            neck = 0
            waist = 0
        
        if height <= 0 or weight <= 0:
            return render_template('index.html', error_message="Hatalı giriş.")

        # Hesaplamalar
        bmi = calc_bmi(weight, height)
        bmr = calc_bmr(weight, height, age, gender)
        tdee = calc_tdee(bmr, activity)
        cal_goal = calorie_target(tdee, goal)
        protein = protein_target(weight)
        macros = macro_split(cal_goal, protein)
        
        real_fat = calc_navy_body_fat(waist, neck, height, gender)
        analysis = assess_risk_internal(bmi, real_fat)

        return render_template('index.html',
                               bmi=round(bmi, 2),
                               bmr=round(bmr),
                               tdee=round(tdee),
                               cal_goal=round(cal_goal),
                               protein=round(macros['protein_g']),
                               fat=round(macros['fat_g']),
                               carbs=round(macros['carb_g']),
                               
                               fat_pct=round(analysis['fat_pct'], 1),
                               bmi_risk=analysis['final_verdict'],         
                               overall_assessment=analysis['bmi_comment']
                              )
    except Exception as e:
        return render_template('index.html', error_message=f"Hata: {e}")

if __name__ == '__main__':
    app.run(debug=True)
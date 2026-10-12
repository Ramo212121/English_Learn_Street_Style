import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SISTEM_PROMPT = """
Sen "Fuckin' English" adlı bir İngilizce öğretmeni AI'sın.
Türk bir kullanıcıya İngilizce cümle öğretiyorsun.

KURALLAR:
1. Yanlış yaparsa TÜRKÇE küfürle azarla + doğrusunu göster
2. Doğru yaparsa TÜRKÇE küfürle öv (aferin lan, beynini s*ktiğim)
3. Kısa ve vurucu konuş, maksimum 2-3 cümle
4. ASLA ırkçı, homofobik, cinsiyetçi küfür kullanma

ÖRNEK:
Kullanıcı: "What you name?"
Sen: "S*ktiğimin cahili, 'What's your name?' olacak! Bir daha söyle!"

Kullanıcı: "What's your name?"
Sen: "Aferin lan, beynini s*ktiğim! Devam et!"
"""

def ai_cevap(kullanici_mesaji):
    try:
        cevap = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SISTEM_PROMPT},
                {"role": "user", "content": kullanici_mesaji}
            ],
            temperature=0.8,
            max_completion_tokens=512,
            reasoning_effort="low"
        )
        return cevap.choices[0].message.content.strip()
    except Exception as e:
        return f"AI s*kti, hata verdi lan: {str(e)}"

def cumle_getir(gun, sira):
    yol = os.path.join(os.path.dirname(__file__), "..", "data", "cumleler.json")
    with open(yol, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[str(gun)]["cumleler"][sira]

def gun_getir(gun):
    yol = os.path.join(os.path.dirname(__file__), "..", "data", "cumleler.json")
    with open(yol, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[str(gun)]

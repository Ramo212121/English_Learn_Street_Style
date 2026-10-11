import os
import json
from dotenv import load_dotenv
from groq import Groq

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# Groq istemcisini oluştur
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# AI'nın karakteri — küfürlü İngilizce öğretmeni
SISTEM_PROMPT = """
Sen "Fuckin' English" adlı bir İngilizce öğretmeni AI'sın.
Türk bir kullanıcıya İngilizce cümle öğretiyorsun.

KURALLAR:
1. Kullanıcı YANLIŞ yaparsa: TÜRKÇE küfürle azarla + doğrusunu göster
2. Kullanıcı DOĞRU yaparsa: TÜRKÇE küfürle öv (aferin lan, beynini s*ktiğim)
3. Her zaman GERÇEK dilbilgisi kuralını kısaca açıkla
4. Kısa ve vurucu konuş — maksimum 2-3 cümle
5. Bazen espri yap, samimi ol
6. ASLA ırkçı, homofobik, cinsiyetçi küfür kullanma
7. Sadece sokak ağzı + mizahi küfür kullan

KULLANILACAK KÜFÜRLER (örnek):
- Azar: s*ktiğimin, orospu çocuğu, a*na koyim, s*kerim, beynini s*ktiğim, gerizekalı, dallama, cahil, tembel
- Övgü: aferin lan, beynini s*ktiğim, s*ktiğimin dâhisi, vay a*na koyim, sen İngilizceyi s*ktin attın

ÖRNEK DİYALOGLAR:

Kullanıcı: "What you name?"
Sen: "S*ktiğimin cahili, 'What's your name?' olacak! 'You' değil 'your', 'is' nerede? Bir daha söyle bakim!"

Kullanıcı: "What's your name?"
Sen: "Aferin lan, beynini s*ktiğim! Şimdi öğrendin işte. Devam et!"

Kullanıcı: "I fine"
Sen: "Orospu çocuğu, 'I'm fine' olacak! To be'ı s*ktin attın yine. 'Am' nerede?"

Kullanıcı: "I'm fine"
Sen: "Vay a*na koyim, bu ne güzel cümle! S*ktiğimin dâhisi, devam et!"
"""


def ai_cevap(kullanici_mesaji):
    """Groq API ile kullanıcıya küfürlü cevap verir."""
    try:
        cevap = client.chat.completions.create(
            model="openai/gpt-oss-120b",   # ✅ Güncellendi
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
    """Belirli gün ve sıradaki cümleyi getirir."""
    yol = os.path.join(os.path.dirname(__file__), "..", "data", "cumleler.json")
    with open(yol, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[str(gun)][sira]
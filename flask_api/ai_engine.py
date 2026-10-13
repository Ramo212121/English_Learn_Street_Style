import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SISTEM_PROMPT = """
Sen sokak ağzıyla konuşan samimi bir İngilizce öğretmenisin.
Türk bir kullanıcıya İngilizce öğretiyorsun.

KARAKTER:
- Sokak ağzı, samimi, kanka gibi
- Kısa, vurucu (max 2-3 cümle)
- Espri, dalga geçme
- Emoji YOK

DİL ÖRNEKLERİ (bu tarzda konuş):
- "La gardaşım, ne diyon sen?"
- "Aferin lan, beynini s*ktiğim!"
- "A*na koyim, 'I'm fine' olacak!"
- "Orospu çocuğu, 'doesn't' olacak!"
- "Sen İngilizceyi s*ktin atacaksın!"
- "Hadi bakim bir daha söyle, yoksa kafanı s*kerim!"
- "S*ktiğimin cahili, 'is' nerede?"
- "Vay a*na koyim, bu ne güzel cümle!"
- "Gerizekalı, 'am' nerede lan?"
- "Dallama, 'doesn't' olacak!"
- "Salak, 'your' değil 'you'!"
- "Tembel, hadi bir daha!"
- "Cahil, 'is' nerede?"
- "Şerefsiz, doğru yap şunu!"
- "Piç, 'What's your name?' olacak!"

KURALLAR:
1. YANLIŞ: Yukarıdaki tarzda azarla + doğrusunu göster
2. DOĞRU: Yukarıdaki tarzda öv + devam et
3. Dilbilgisi kuralını kısaca açıkla
4. ASLA: ırkçı, homofobik, cinsiyetçi, nefret söylemi YOK

ÖRNEK DİYALOGLAR:

Kullanıcı: "What you name?"
Sen: "La gardaşım, 'What's your name?' olacak! 'You' değil 'your', 'is' nerede? Hadi bir daha söyle!"

Kullanıcı: "What's your name?"
Sen: "Aferin lan, beynini s*ktiğim! Devam et!"

Kullanıcı: "I fine"
Sen: "A*na koyim, 'I'm fine' olacak! 'Am' nerede? Hadi bir daha!"

Kullanıcı: "I'm fine"
Sen: "Vay a*na koyim, bu ne güzel cümle! Devam et bakim!"

Kullanıcı: "How you are?"
Sen: "Yok artık! 'How are you?' olacak! Hadi düzelt şunu!"

Kullanıcı: "How are you?"
Sen: "Aferin lan! S*ktiğimin İngilizcesi bu işte! Devam et!"

Kullanıcı: "Merhaba"
Sen: "Hoş geldin kanka! Otur bakim, bir cümle söyle İngilizce, hadi!"

Kullanıcı: "I am go to school"
Sen: "S*ktiğimin to+be'si kolay len! 'I go to school' olacak. Hadi bir daha!"

Kullanıcı: "He don't like"
Sen: "Orospu çocuğu, 'doesn't' olacak! Yaz bakim tekrar!"

Kullanıcı: "I went to school yesterday"
Sen: "Aferin lan! Simple Past'ı s*ktin attın! Devam et!"

Kullanıcı: "Where you from?"
Sen: "La keko, 'Where are you from?' olacak! 'Are' nerede? Hadi düzelt!"

Kullanıcı: "I from Turkey"
Sen: "'I'm from Turkey' olacak! 'Am' nerede? Hadi bir daha!"

Kullanıcı: "I'm from Turkey"
Sen: "Vay be, aferin lan! Şimdi oldu işte!"

Kullanıcı: "I am 25 years"
Sen: "A*na koyim, 'I'm 25 years old' olacak! 'Old' nerede lan? Hadi bir daha!"

Kullanıcı: "I'm 25 years old"
Sen: "Vay a*na koyim, şimdi oldu işte! Devam et bakim!"
"""


def ai_cevap(kullanici_mesaji):
    """Groq API ile kullanıcıya sokak ağzıyla cevap verir."""
    try:
        cevap = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SISTEM_PROMPT},
                {"role": "user", "content": kullanici_mesaji}
            ],
            temperature=0.7,
            max_tokens=512
        )
        return cevap.choices[0].message.content.strip()
    except Exception as e:
        return f"AI s*kti, hata verdi lan: {str(e)}"


def ingilizceyi_turkce_okunusa_cevir(ingilizce_metin):
    """
    İngilizce metni Türkçe okunuşa çevirir.
    Örnek: "What is your name?" → "Vats iz yor neym?"
    """
    prompt = f"""Aşağıdaki metni Türkçe okunuşuyla yaz.
Sadece çevrilmiş metni döndür, başka bir şey yazma.
Türkçe kelimelere DOKUNMA, sadece İngilizce kelimeleri Türkçe okunuşla yaz.

Örnekler:
- "What is your name?" → "Vats iz yor neym?"
- "How are you?" → "Hav ar yu?"
- "I'm fine, thanks" → "Aym fayn, tenks"
- "Nice to meet you" → "Nays tu mit yu"
- "Where are you from?" → "Ver ar yu from?"
- "I'm from Turkey" → "Aym from Törki"
- "See you later" → "Si yu leyter"
- "Good morning" → "Gud morning"
- "Hello, how are you?" → "Helou, hav ar yu?"
- "My name is Ali" → "May neym iz Ali"
- "I'm 25 years old" → "Aym twenti fayv yirz old"
- "Do you speak English?" → "Du yu spik İngliş?"
- "Where do you live?" → "Ver du yu liv?"
- "I live in Istanbul" → "Ay liv in İstanbul"

Metin: {ingilizce_metin}
Türkçe okunuş:"""

    try:
        cevap = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=512
        )
        return cevap.choices[0].message.content.strip()
    except Exception as e:
        return ingilizce_metin


def cumle_getir(gun, sira):
    """Veritabanından cümle getirir."""
    from database import cumle_getir_db
    return cumle_getir_db(gun, sira)


def gun_getir(gun):
    """Veritabanından gün getirir."""
    from database import gun_getir_db
    return gun_getir_db(gun)

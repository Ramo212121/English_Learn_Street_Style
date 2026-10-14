from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ai_engine import (
    ai_cevap, cumle_getir, gun_getir,
    ingilizceyi_turkce_okunusa_cevir
)
from database import (
    kullanici_olustur, kullanici_getir,
    cevap_kaydet, tekrar_listesi, baglanti,
    rastgele_cumle, quiz_cevap_kontrol, quiz_istatistik
)
from tts import ses_uret
import hashlib
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def ana_sayfa():
    return jsonify({
        "mesaj": "S*ktiğimin İngilizcesi API çalışıyor!",
        "durum": "aktif",
        "versiyon": "0.8",
        "endpointler": [
            "/",
            "/gun/<int:gun>",
            "/cumle/<int:gun>/<int:sira>",
            "/sohbet",
            "/kullanici (POST)",
            "/kullanici/<int:id>",
            "/cevapla (POST)",
            "/tekrar/<int:id>",
            "/quiz?gun=<int>",
            "/quiz/cevapla (POST)",
            "/quiz/cevapla-sesli (POST)",
            "/istatistik/<int:id>",
            "/ses?metin=<metin>"
        ]
    })


@app.route("/gun/<int:gun>", methods=["GET"])
def gun(gun):
    try:
        return jsonify(gun_getir(gun))
    except Exception as e:
        return jsonify({"hata": f"Gün bulunamadı: {e}"}), 404


@app.route("/cumle/<int:gun>/<int:sira>", methods=["GET"])
def cumle(gun, sira):
    try:
        return jsonify(cumle_getir(gun, sira))
    except Exception as e:
        return jsonify({"hata": f"Cümle bulunamadı: {e}"}), 404


@app.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json()
    if not data or "mesaj" not in data:
        return jsonify({"hata": "Mesaj boş!"}), 400
    return jsonify({"kullanici": data["mesaj"], "ai": ai_cevap(data["mesaj"])})


@app.route("/kullanici", methods=["POST"])
def kullanici():
    data = request.get_json()
    if not data or "isim" not in data:
        return jsonify({"hata": "İsim gerekli lan!"}), 400
    kullanici_id = kullanici_olustur(data["isim"])
    return jsonify({
        "kullanici_id": kullanici_id,
        "isim": data["isim"],
        "mesaj": f"Hoş geldin {data['isim']}! Artık küfür yemeye hazırsın!"
    })


@app.route("/kullanici/<int:kullanici_id>", methods=["GET"])
def kullanici_bilgi(kullanici_id):
    k = kullanici_getir(kullanici_id)
    if not k:
        return jsonify({"hata": "Kullanıcı bulunamadı lan!"}), 404
    return jsonify(k)


@app.route("/cevapla", methods=["POST"])
def cevapla():
    data = request.get_json()
    if not data or "kullanici_id" not in data or "cumle_id" not in data or "dogru_mu" not in data:
        return jsonify({"hata": "Eksik bilgi lan!"}), 400
    sonuc = cevap_kaydet(
        data["kullanici_id"], data["cumle_id"], data["dogru_mu"]
    )
    return jsonify({
        "mesaj": "Kaydedildi!",
        "sonraki_tekrar": sonuc["sonraki_tarih"],
        "aralik_gun": sonuc["aralik"]
    })


@app.route("/tekrar/<int:kullanici_id>", methods=["GET"])
def tekrar(kullanici_id):
    cumle_idler = tekrar_listesi(kullanici_id)
    cumleler = []
    conn = baglanti()
    cursor = conn.cursor()
    for cid in cumle_idler:
        cursor.execute("SELECT * FROM cumleler WHERE id = ?", (cid,))
        row = cursor.fetchone()
        if row:
            cumleler.append({
                "id": row["id"],
                "ingilizce": row["ingilizce"],
                "turkce": row["turkce"],
                "baglam": row["baglam"],
                "ipucu": row["ipucu"]
            })
    conn.close()
    return jsonify({
        "kullanici_id": kullanici_id,
        "tekrar_sayisi": len(cumleler),
        "cumleler": cumleler
    })


# ============ QUIZ ENDPOINT'LERİ ============

@app.route("/quiz", methods=["GET"])
def quiz():
    """Rastgele bir quiz sorusu getirir."""
    gun = request.args.get("gun", type=int)
    cumle = rastgele_cumle(gun)

    if not cumle:
        return jsonify({"hata": "S*ktiğimin cümlesi bulunamadı!"}), 404

    return jsonify({
        "cumle_id": cumle["id"],
        "turkce": cumle["turkce"],
        "baglam": cumle["baglam"],
        "ipucu": cumle["ipucu"],
        "soru": "Bunun İngilizcesi ne?",
        "cumle_uzunlugu": len(cumle["ingilizce"].split())
    })


@app.route("/quiz/cevapla", methods=["POST"])
def quiz_cevapla():
    """Quiz cevabını kontrol eder, JSON döner."""
    data = request.get_json()
    if not data or "kullanici_id" not in data or "cumle_id" not in data or "cevap" not in data:
        return jsonify({"hata": "Eksik bilgi lan!"}), 400

    sonuc = quiz_cevap_kontrol(data["cumle_id"], data["cevap"])
    if not sonuc:
        return jsonify({"hata": "Cümle bulunamadı!"}), 404

    cevap_kaydet(data["kullanici_id"], data["cumle_id"], sonuc["dogru_mu"])

    if sonuc["dogru_mu"]:
        ai_mesaj = ai_cevap(
            f"Kullanıcı doğru cevap verdi: '{data['cevap']}'. "
            f"Ona kısa bir övgü küfürü yaz ve doğru cümleyi tekrarla."
        )
    else:
        ai_mesaj = ai_cevap(
            f"Kullanıcı yanlış cevap verdi: '{data['cevap']}'. "
            f"Doğrusu: '{sonuc['dogru_cevap']}'. "
            f"Ona kısa bir azar küfürü yaz, doğru cümleyi söyle ve tekrar ettir."
        )

    return jsonify({
        "dogru_mu": sonuc["dogru_mu"],
        "dogru_cevap": sonuc["dogru_cevap"],
        "ai_mesaj": ai_mesaj
    })


@app.route("/quiz/cevapla-sesli", methods=["POST"])
def quiz_cevapla_sesli():
    """Quiz cevabını kontrol eder, AI mesajını SESLİ okur."""
    data = request.get_json()
    if not data or "kullanici_id" not in data or "cumle_id" not in data or "cevap" not in data:
        return jsonify({"hata": "Eksik bilgi lan!"}), 400

    sonuc = quiz_cevap_kontrol(data["cumle_id"], data["cevap"])
    if not sonuc:
        return jsonify({"hata": "Cümle bulunamadı!"}), 404

    cevap_kaydet(data["kullanici_id"], data["cumle_id"], sonuc["dogru_mu"])

    # AI mesajı
    if sonuc["dogru_mu"]:
        ai_mesaj = ai_cevap(
            f"Kullanıcı doğru cevap verdi: '{data['cevap']}'. "
            f"Ona kısa bir övgü küfürü yaz ve doğru cümleyi tekrarla."
        )
    else:
        ai_mesaj = ai_cevap(
            f"Kullanıcı yanlış cevap verdi: '{data['cevap']}'. "
            f"Doğrusu: '{sonuc['dogru_cevap']}'. "
            f"Ona kısa bir azar küfürü yaz, doğru cümleyi söyle ve tekrar ettir."
        )

    # Türkçe okunuşa çevir
    try:
        ai_mesaj_okunus = ingilizceyi_turkce_okunusa_cevir(ai_mesaj)
    except Exception as e:
        ai_mesaj_okunus = ai_mesaj

    # Metni temizle (yıldız, markdown, özel karakter)
    temiz_metin = ai_mesaj_okunus.replace("*", "").replace("#", "").replace("`", "").replace("_", "")
    temiz_metin = temiz_metin.replace('"', '').replace("'", "")
    temiz_metin = temiz_metin.strip()
    temiz_metin = temiz_metin[:500]  # Max 500 karakter

    # Boş kontrolü
    if len(temiz_metin) < 3:
        temiz_metin = "La gardasim, dogrusu: " + sonuc["dogru_cevap"]

    # Debug
    print(f"🔍 OKUNUŞ: {temiz_metin!r}")

    # Ses üret
    dosya_adi = hashlib.md5(ai_mesaj.encode()).hexdigest() + ".mp3"
    try:
        ses_yolu = ses_uret(temiz_metin, dosya_adi)
    except Exception as e:
        # Fallback: basit metin
        try:
            basit_mesaj = "La gardasim, dogrusu: " + sonuc["dogru_cevap"]
            dosya_adi = hashlib.md5(basit_mesaj.encode()).hexdigest() + ".mp3"
            ses_yolu = ses_uret(basit_mesaj, dosya_adi)
        except Exception as e2:
            return jsonify({"hata": f"Ses üretilemedi: {e2}"}), 500

    return jsonify({
        "dogru_mu": sonuc["dogru_mu"],
        "dogru_cevap": sonuc["dogru_cevap"],
        "ai_mesaj": ai_mesaj,
        "ai_mesaj_okunus": ai_mesaj_okunus,
        "ses_url": f"/ses-dinle/{dosya_adi}"
    })


@app.route("/ses-dinle/<dosya_adi>", methods=["GET"])
def ses_dinle(dosya_adi):
    """Üretilmiş ses dosyasını döner."""
    klasor = os.path.join(os.path.dirname(__file__), "..", "data", "sesler")
    yol = os.path.join(klasor, dosya_adi)
    try:
        return send_file(yol, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"hata": f"Ses bulunamadı: {e}"}), 404


@app.route("/istatistik/<int:kullanici_id>", methods=["GET"])
def istatistik(kullanici_id):
    ist = quiz_istatistik(kullanici_id)
    if not ist:
        return jsonify({"hata": "Kullanıcı bulunamadı!"}), 404
    return jsonify(ist)


# ============ TTS ENDPOINT'İ ============

@app.route("/ses", methods=["GET"])
def ses():
    """Metni sese çevirir ve MP3 döndürür."""
    metin = request.args.get("metin")
    if not metin:
        return jsonify({"hata": "Metin gerekli lan!"}), 400

    # Metni temizle
    metin = metin.replace("*", "").replace("#", "").replace("`", "")
    metin = metin.strip()[:500]

    dosya_adi = hashlib.md5(metin.encode()).hexdigest() + ".mp3"

    try:
        yol = ses_uret(metin, dosya_adi)
        return send_file(yol, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"hata": f"Ses üretilemedi: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

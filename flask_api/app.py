from flask import Flask, request, jsonify
from ai_engine import ai_cevap, cumle_getir, gun_getir
from database import (
    kullanici_olustur, kullanici_getir,
    cevap_kaydet, tekrar_listesi, baglanti
)

app = Flask(__name__)


@app.route("/")
def ana_sayfa():
    return jsonify({
        "mesaj": "S*ktiğimin İngilizcesi API çalışıyor!",
        "durum": "aktif",
        "versiyon": "0.3",
        "endpointler": [
            "/",
            "/gun/<int:gun>",
            "/cumle/<int:gun>/<int:sira>",
            "/sohbet",
            "/kullanici (POST)",
            "/kullanici/<int:kullanici_id>",
            "/cevapla (POST)",
            "/tekrar/<int:kullanici_id>"
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
    """Yeni kullanıcı oluşturur."""
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
    """Kullanıcı bilgilerini getirir."""
    k = kullanici_getir(kullanici_id)
    if not k:
        return jsonify({"hata": "Kullanıcı bulunamadı lan!"}), 404
    return jsonify(k)


@app.route("/cevapla", methods=["POST"])
def cevapla():
    """Kullanıcının cevabını kaydeder."""
    data = request.get_json()
    if not data or "kullanici_id" not in data or "cumle_id" not in data or "dogru_mu" not in data:
        return jsonify({"hata": "Eksik bilgi lan!"}), 400

    sonuc = cevap_kaydet(
        data["kullanici_id"],
        data["cumle_id"],
        data["dogru_mu"]
    )
    return jsonify({
        "mesaj": "Kaydedildi!",
        "sonraki_tekrar": sonuc["sonraki_tarih"],
        "aralik_gun": sonuc["aralik"]
    })


@app.route("/tekrar/<int:kullanici_id>", methods=["GET"])
def tekrar(kullanici_id):
    """Kullanıcının tekrar etmesi gereken cümleleri getirir."""
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


if __name__ == "__main__":
    app.run(debug=True, port=5001)

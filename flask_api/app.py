from flask import Flask, request, jsonify
from ai_engine import ai_cevap, cumle_getir

app = Flask(__name__)


@app.route("/")
def ana_sayfa():
    return jsonify({
        "mesaj": "S*ktiğimin İngilizcesi API çalışıyor!",
        "durum": "aktif",
        "versiyon": "0.1"
    })


@app.route("/cumle/<int:gun>/<int:sira>", methods=["GET"])
def cumle(gun, sira):
    """Belirli gün ve sıradaki cümleyi getirir."""
    try:
        c = cumle_getir(gun, sira)
        return jsonify(c)
    except Exception as e:
        return jsonify({"hata": f"S*ktiğimin cümlesi bulunamadı: {e}"}), 404


@app.route("/sohbet", methods=["POST"])
def sohbet():
    """Kullanıcı mesajına AI cevabı verir."""
    data = request.get_json()
    if not data or "mesaj" not in data:
        return jsonify({"hata": "Mesaj boş olamaz lan!"}), 400

    mesaj = data["mesaj"]
    cevap = ai_cevap(mesaj)
    return jsonify({
        "kullanici": mesaj,
        "ai": cevap
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)  
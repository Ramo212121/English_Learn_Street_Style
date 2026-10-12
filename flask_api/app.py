from flask import Flask, request, jsonify
from ai_engine import ai_cevap, cumle_getir, gun_getir

app = Flask(__name__)

@app.route("/")
def ana_sayfa():
    return jsonify({
        "mesaj": "S*ktiğimin İngilizcesi API çalışıyor!",
        "durum": "aktif",
        "versiyon": "0.2",
        "endpointler": ["/", "/gun/<int:gun>", "/cumle/<int:gun>/<int:sira>", "/sohbet"]
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

if __name__ == "__main__":
    app.run(debug=True, port=5001)

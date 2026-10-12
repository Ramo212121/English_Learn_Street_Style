import sqlite3
import os
import json

# Veritabanı yolu
DB_YOL = os.path.join(os.path.dirname(__file__), "..", "data", "fuckin_english.db")


def baglanti():
    """Veritabanına bağlantı açar."""
    conn = sqlite3.connect(DB_YOL)
    conn.row_factory = sqlite3.Row  # Dict gibi erişim için
    return conn


def tablolari_olustur():
    """Tabloları oluşturur (yoksa)."""
    conn = baglanti()
    cursor = conn.cursor()

    # Cümleler tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cumleler (
            id INTEGER PRIMARY KEY,
            gun INTEGER NOT NULL,
            seviye TEXT NOT NULL,
            ingilizce TEXT NOT NULL,
            turkce TEXT NOT NULL,
            baglam TEXT,
            ipucu TEXT,
            varyasyonlar TEXT
        )
    """)

    # Kullanıcılar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            seviye TEXT DEFAULT 'A1',
            kufur_sayisi INTEGER DEFAULT 0,
            dogru_sayisi INTEGER DEFAULT 0,
            yanlis_sayisi INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            son_aktivite TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Cevaplar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cevaplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_id INTEGER NOT NULL,
            cumle_id INTEGER NOT NULL,
            dogru_mu BOOLEAN NOT NULL,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sonraki_sorulma TIMESTAMP,
            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id),
            FOREIGN KEY (cumle_id) REFERENCES cumleler(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablolar oluşturuldu!")


def json_to_db():
    """JSON'daki cümleleri veritabanına aktarır."""
    json_yol = os.path.join(os.path.dirname(__file__), "..", "data", "cumleler.json")
    with open(json_yol, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = baglanti()
    cursor = conn.cursor()

    # Önce mevcut cümleleri sil (yeniden yüklemek için)
    cursor.execute("DELETE FROM cumleler")

    toplam = 0
    for gun_str, gun_data in data.items():
        gun = int(gun_str)
        seviye = gun_data.get("seviye", "A1")
        for cumle in gun_data["cumleler"]:
            cursor.execute("""
                INSERT INTO cumleler (id, gun, seviye, ingilizce, turkce, baglam, ipucu, varyasyonlar)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cumle["id"],
                gun,
                seviye,
                cumle["ingilizce"],
                cumle["turkce"],
                cumle.get("baglam", ""),
                cumle.get("ipucu", ""),
                json.dumps(cumle.get("varyasyonlar", []), ensure_ascii=False)
            ))
            toplam += 1

    conn.commit()
    conn.close()
    print(f"✅ {toplam} cümle veritabanına aktarıldı!")


def cumle_getir_db(gun, sira):
    """Veritabanından belirli gün ve sıradaki cümleyi getirir."""
    conn = baglanti()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM cumleler
        WHERE gun = ?
        ORDER BY id
        LIMIT 1 OFFSET ?
    """, (gun, sira))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "ingilizce": row["ingilizce"],
        "turkce": row["turkce"],
        "baglam": row["baglam"],
        "ipucu": row["ipucu"],
        "varyasyonlar": json.loads(row["varyasyonlar"]) if row["varyasyonlar"] else []
    }


def gun_getir_db(gun):
    """Veritabanından belirli günün tüm bilgilerini getirir."""
    conn = baglanti()
    cursor = conn.cursor()

    # Günün seviyesi ve teması
    cursor.execute("""
        SELECT DISTINCT seviye FROM cumleler WHERE gun = ?
    """, (gun,))
    seviye_row = cursor.fetchone()
    if not seviye_row:
        conn.close()
        return None

    # Günün cümleleri
    cursor.execute("""
        SELECT * FROM cumleler
        WHERE gun = ?
        ORDER BY id
    """, (gun,))
    rows = cursor.fetchall()
    conn.close()

    cumleler = []
    for row in rows:
        cumleler.append({
            "id": row["id"],
            "ingilizce": row["ingilizce"],
            "turkce": row["turkce"],
            "baglam": row["baglam"],
            "ipucu": row["ipucu"],
            "varyasyonlar": json.loads(row["varyasyonlar"]) if row["varyasyonlar"] else []
        })

    return {
        "seviye": seviye_row["seviye"],
        "cumleler": cumleler
    }


if __name__ == "__main__":
    print("🔧 Veritabanı kuruluyor...")
    tablolari_olustur()
    json_to_db()
    print("✅ Hazır!")
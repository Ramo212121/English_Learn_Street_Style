import sqlite3
import os
import json
from spaced_repetition import sm2_hesapla, tekrar_zamani_geldi_mi

DB_YOL = os.path.join(os.path.dirname(__file__), "..", "data", "fuckin_english.db")


def baglanti():
    """Veritabanına bağlantı açar."""
    conn = sqlite3.connect(DB_YOL)
    conn.row_factory = sqlite3.Row
    return conn


def tablolari_olustur():
    """Tabloları oluşturur (yoksa)."""
    conn = baglanti()
    cursor = conn.cursor()

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cevaplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_id INTEGER NOT NULL,
            cumle_id INTEGER NOT NULL,
            dogru_mu BOOLEAN NOT NULL,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sonraki_sorulma TIMESTAMP,
            aralik INTEGER DEFAULT 0,
            kolaylik REAL DEFAULT 2.5,
            tekrar INTEGER DEFAULT 0,
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
                cumle["id"], gun, seviye,
                cumle["ingilizce"], cumle["turkce"],
                cumle.get("baglam", ""), cumle.get("ipucu", ""),
                json.dumps(cumle.get("varyasyonlar", []), ensure_ascii=False)
            ))
            toplam += 1

    conn.commit()
    conn.close()
    print(f"✅ {toplam} cümle veritabanına aktarıldı!")


def cumle_getir_db(gun, sira):
    """Belirli gün ve sıradaki cümleyi getirir."""
    conn = baglanti()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM cumleler WHERE gun = ?
        ORDER BY id LIMIT 1 OFFSET ?
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
    """Belirli günün tüm bilgilerini getirir."""
    conn = baglanti()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT seviye FROM cumleler WHERE gun = ?", (gun,))
    seviye_row = cursor.fetchone()
    if not seviye_row:
        conn.close()
        return None

    cursor.execute("SELECT * FROM cumleler WHERE gun = ? ORDER BY id", (gun,))
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

    return {"seviye": seviye_row["seviye"], "cumleler": cumleler}


def kullanici_olustur(isim):
    """Yeni kullanıcı oluşturur."""
    conn = baglanti()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kullanicilar (isim) VALUES (?)", (isim,))
    kullanici_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return kullanici_id


def kullanici_getir(kullanici_id):
    """Kullanıcı bilgilerini getirir."""
    conn = baglanti()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kullanicilar WHERE id = ?", (kullanici_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "isim": row["isim"],
        "seviye": row["seviye"],
        "kufur_sayisi": row["kufur_sayisi"],
        "dogru_sayisi": row["dogru_sayisi"],
        "yanlis_sayisi": row["yanlis_sayisi"],
        "streak": row["streak"],
        "son_aktivite": row["son_aktivite"]
    }


def cevap_kaydet(kullanici_id, cumle_id, dogru_mu):
    """Cevabı kaydeder ve SM-2 ile sonraki tarihi hesaplar."""
    conn = baglanti()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM cevaplar
        WHERE kullanici_id = ? AND cumle_id = ?
    """, (kullanici_id, cumle_id))
    mevcut = cursor.fetchone()

    if mevcut:
        mevcut_aralik = mevcut["aralik"] or 0
        mevcut_kolaylik = mevcut["kolaylik"] or 2.5
        mevcut_tekrar = mevcut["tekrar"] or 0

        sonuc = sm2_hesapla(dogru_mu, mevcut_aralik, mevcut_kolaylik, mevcut_tekrar)

        cursor.execute("""
            UPDATE cevaplar
            SET dogru_mu = ?, tarih = CURRENT_TIMESTAMP, sonraki_sorulma = ?,
                aralik = ?, kolaylik = ?, tekrar = ?
            WHERE kullanici_id = ? AND cumle_id = ?
        """, (
            dogru_mu, sonuc["sonraki_tarih"],
            sonuc["aralik"], sonuc["kolaylik"], sonuc["tekrar"],
            kullanici_id, cumle_id
        ))
    else:
        sonuc = sm2_hesapla(dogru_mu)
        cursor.execute("""
            INSERT INTO cevaplar
            (kullanici_id, cumle_id, dogru_mu, sonraki_sorulma, aralik, kolaylik, tekrar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            kullanici_id, cumle_id, dogru_mu,
            sonuc["sonraki_tarih"], sonuc["aralik"],
            sonuc["kolaylik"], sonuc["tekrar"]
        ))

    if dogru_mu:
        cursor.execute("""
            UPDATE kullanicilar
            SET dogru_sayisi = dogru_sayisi + 1, son_aktivite = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (kullanici_id,))
    else:
        cursor.execute("""
            UPDATE kullanicilar
            SET yanlis_sayisi = yanlis_sayisi + 1,
                kufur_sayisi = kufur_sayisi + 1,
                son_aktivite = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (kullanici_id,))

    conn.commit()
    conn.close()
    return sonuc


def tekrar_listesi(kullanici_id):
    """Kullanıcının tekrar etmesi gereken cümleleri getirir."""
    conn = baglanti()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cumle_id, sonraki_sorulma FROM cevaplar
        WHERE kullanici_id = ?
    """, (kullanici_id,))
    cevaplar = cursor.fetchall()
    conn.close()

    liste = []
    for c in cevaplar:
        if tekrar_zamani_geldi_mi(c["sonraki_sorulma"]):
            liste.append(c["cumle_id"])
    return liste


# ============ QUIZ FONKSİYONLARI ============

import random


def rastgele_cumle(gun=None):
    """Rastgele bir cümle getirir. Gün belirtilirse o günden."""
    conn = baglanti()
    cursor = conn.cursor()

    if gun:
        cursor.execute("""
            SELECT * FROM cumleler WHERE gun = ?
            ORDER BY RANDOM() LIMIT 1
        """, (gun,))
    else:
        cursor.execute("SELECT * FROM cumleler ORDER BY RANDOM() LIMIT 1")

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


def quiz_cevap_kontrol(cumle_id, kullanici_cevabi):
    """Kullanıcının cevabını kontrol eder."""
    conn = baglanti()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cumleler WHERE id = ?", (cumle_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    dogru_cevap = row["ingilizce"]

    def normalize(s):
        return s.lower().strip().replace("'", "'").replace("?", "").replace(".", "").replace("!", "")

    dogru_mu = normalize(kullanici_cevabi) == normalize(dogru_cevap)

    if not dogru_mu:
        varyasyonlar = json.loads(row["varyasyonlar"]) if row["varyasyonlar"] else []
        for v in varyasyonlar:
            if normalize(kullanici_cevabi) == normalize(v):
                dogru_mu = True
                break

    return {
        "dogru_mu": dogru_mu,
        "dogru_cevap": dogru_cevap,
        "cumle_id": cumle_id
    }


def quiz_istatistik(kullanici_id):
    """Kullanıcının quiz istatistiklerini getirir."""
    conn = baglanti()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kullanicilar WHERE id = ?", (kullanici_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    toplam = row["dogru_sayisi"] + row["yanlis_sayisi"]
    basari_orani = round((row["dogru_sayisi"] / toplam * 100), 1) if toplam > 0 else 0

    return {
        "isim": row["isim"],
        "seviye": row["seviye"],
        "dogru_sayisi": row["dogru_sayisi"],
        "yanlis_sayisi": row["yanlis_sayisi"],
        "kufur_sayisi": row["kufur_sayisi"],
        "streak": row["streak"],
        "toplam": toplam,
        "basari_orani": basari_orani
    }


if __name__ == "__main__":
    print("🔧 Veritabanı kuruluyor...")
    tablolari_olustur()
    json_to_db()
    print("✅ Hazır!")

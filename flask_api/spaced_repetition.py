from datetime import datetime, timedelta


def sm2_hesapla(dogru_mu, mevcut_aralik=0, mevcut_kolaylik=2.5, mevcut_tekrar=0):
    """
    SM-2 algoritması ile bir sonraki tekrar zamanını hesaplar.

    Args:
        dogru_mu (bool): Cevap doğru mu?
        mevcut_aralik (int): Şu anki aralık (gün)
        mevcut_kolaylik (float): Kolaylık faktörü (başlangıç: 2.5)
        mevcut_tekrar (int): Kaç kez üst üste doğru

    Returns:
        dict: {
            "aralik": int,          # Yeni aralık (gün)
            "kolaylik": float,      # Yeni kolaylık faktörü
            "tekrar": int,          # Yeni tekrar sayısı
            "sonraki_tarih": str    # Sonraki tekrar tarihi (ISO)
        }
    """
    kolaylik = mevcut_kolaylik

    if not dogru_mu:
        # Yanlış → başa dön
        tekrar = 0
        aralik = 1  # Yarın tekrar sor
        kolaylik = max(1.3, kolaylik - 0.2)  # Kolaylığı azalt (min 1.3)
    else:
        # Doğru
        tekrar = mevcut_tekrar + 1

        if tekrar == 1:
            aralik = 1  # 1 gün sonra
        elif tekrar == 2:
            aralik = 3  # 3 gün sonra
        else:
            aralik = round(mevcut_aralik * kolaylik)

        # Kolaylığı güncelle (SM-2 formülü basitleştirilmiş)
        kolaylik = kolaylik + (0.1 - (5 - 5) * (0.08 + (5 - 5) * 0.02))
        kolaylik = max(1.3, kolaylik)

    sonraki_tarih = datetime.now() + timedelta(days=aralik)

    return {
        "aralik": aralik,
        "kolaylik": round(kolaylik, 2),
        "tekrar": tekrar,
        "sonraki_tarih": sonraki_tarih.isoformat()
    }


def tekrar_zamani_geldi_mi(sonraki_sorulma):
    """
    Bir cümlenin tekrar zamanı geldi mi?

    Args:
        sonraki_sorulma (str): ISO formatında tarih (veya None)

    Returns:
        bool: True ise tekrar zamanı geldi
    """
    if not sonraki_sorulma:
        return True  # Hiç sorulmamış → tekrar zamanı

    try:
        tarih = datetime.fromisoformat(sonraki_sorulma)
        return datetime.now() >= tarih
    except (ValueError, TypeError):
        return True  # Hatalı tarih → tekrar zamanı
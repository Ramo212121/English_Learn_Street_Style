import asyncio
import edge_tts
import os

# Tek ses: Türkçe (Ahmet)
SES = "tr-TR-AhmetNeural"


async def _ses_uret_tek(metin, dosya_yolu, deneme=3):
    """Ses üretir. Boş dönerse tekrar dener."""
    for i in range(deneme):
        try:
            iletisim = edge_tts.Communicate(metin, SES)
            await iletisim.save(dosya_yolu)

            if os.path.exists(dosya_yolu) and os.path.getsize(dosya_yolu) > 0:
                return True

            print(f"⚠️ Deneme {i+1}: Boş dosya")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"⚠️ Deneme {i+1} hata: {e}")
            await asyncio.sleep(1)

    return False


def ses_uret(metin, dosya_adi="cikti.mp3"):
    """Senkron ses üretimi (tek ses, Türkçe)."""
    klasor = os.path.join(os.path.dirname(__file__), "..", "data", "sesler")
    os.makedirs(klasor, exist_ok=True)
    dosya_yolu = os.path.join(klasor, dosya_adi)

    ok = asyncio.run(_ses_uret_tek(metin, dosya_yolu))

    if not ok:
        raise Exception("Ses üretilemedi")

    return dosya_yolu


if __name__ == "__main__":
    yol = ses_uret("La gardaşım, Vats iz yor neym? Hadi bir daha söyle!", "test.mp3")
    print(f"✅ Oluşturuldu: {yol}")
    print(f"📦 Boyut: {os.path.getsize(yol)} bytes")

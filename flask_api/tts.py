import asyncio
import edge_tts
import os

SES = "tr-TR-AhmetNeural"  # Türkçe erkek ses
# Alternatif: "tr-TR-EmelNeural" (kadın)


async def _ses_uret(metin, dosya_yolu):
    """Edge-TTS ile ses üretir."""
    iletisim = edge_tts.Communicate(metin, SES)
    await iletisim.save(dosya_yolu)


def ses_uret(metin, dosya_adi="cikti.mp3"):
    """Senkron ses üretimi."""
    klasor = os.path.join(os.path.dirname(__file__), "..", "data", "sesler")
    os.makedirs(klasor, exist_ok=True)
    dosya_yolu = os.path.join(klasor, dosya_adi)

    asyncio.run(_ses_uret(metin, dosya_yolu))
    return dosya_yolu


if __name__ == "__main__":
    yol = ses_uret("Aferin lan, beynini s*ktiğim!", "test.mp3")
    print(f"✅ Ses oluşturuldu: {yol}")

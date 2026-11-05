"""
.exe için başlangıç noktası.
İlk açılışta veritabanını kurar, tarayıcıyı açar ve sunucuyu başlatır.
"""
import threading
import webbrowser

from app import app
from veri.veritabani import VERITABANI_YOLU
from veri.ornek_veri import ornek_veri_ekle

ADRES = "http://127.0.0.1:5000"

if __name__ == "__main__":
    if not VERITABANI_YOLU.exists():
        ornek_veri_ekle()          # ilk açılış: tabloları kur + örnek veri ekle

    print("Butce Asistani calisiyor:", ADRES)
    print("Kapatmak icin bu pencereyi kapatin.")

    threading.Timer(1.5, lambda: webbrowser.open(ADRES)).start()   # 1,5 sn sonra tarayıcıyı aç
    app.run(debug=False)           # exe'de debug KAPALI olmalı
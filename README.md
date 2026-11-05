# 💰 Kişisel Bütçe ve Harcama Analiz Asistanı

Kullanıcıların gelir ve giderlerini kaydedip kategorilere ayırabildiği, bütçe hedefi koyup aşıldığında uyarı alabildiği bir web uygulaması.

**Ders:** Bilgisayar Uygulamaları I — Proje P29
**Geliştiren:** Hilal İsen
**Okul:** Bingöl Üniversitesi, Bilgisayar Programcılığı

## 🛠️ Kullanılan Teknolojiler
- **Python 3.13**
- **Flask** (web çatısı)
- **SQLite** (veritabanı)

## 📁 Klasör Yapısı (Katmanlı Mimari)
- `sunum/` → Kullanıcının gördüğü sayfalar (sunum katmanı)
- `is_katmani/` → İş kuralları ve hesaplamalar (iş katmanı)
- `veri/` → Veritabanı işlemleri (veri katmanı)
- `belgeler/` → ER diyagramı ve mimari şema

## 🚀 Kurulum
1. Depoyu klonla: `git clone https://github.com/Hilalisen44/butce-asistani.git`
2. Sanal ortam oluştur: `python -m venv venv`
3. Etkinleştir: `.\venv\Scripts\Activate.ps1`
4. Paketleri yükle: `pip install -r requirements.txt`

## ▶️ Çalıştırma
1. `.\venv\Scripts\Activate.ps1`
2. `python -m veri.ornek_veri` (veritabanını örnek veriyle oluşturur)
3. `python app.py`
4. Tarayıcıda `127.0.0.1:5000`

## 👤 Test hesapları (uydurma, KVKK'ya uygun)
| Rol | E-posta | Parola |
|---|---|---|
| Kullanıcı | test@ornek.com | Test123 |
| Yönetici | yonetici@ornek.com | Yonetici123 |

## ✅ Tamamlanan modüller (v0.1-vize)
- Hafta 3: Katmanlı mimari, ER diyagramı
- Hafta 4: Veritabanı şeması, kısıtlar, CRUD
- Hafta 5: Kayıt/giriş, parola hash, rol tabanlı erişim
- Hafta 6: Gelir/gider kaydı, filtre, arama
- Hafta 7: Bütçe hedefi ve aşım uyarısı

## 📌 Durum
Ara sürüm (vize): v0.1-vize
# Güvenlik Notu (Hafta 5)

## 1. Parola güvenliği
- Parolalar veritabanında **düz metin olarak saklanmaz**.
- `werkzeug.security.generate_password_hash` ile **tuzlanmış (salt) hash** olarak saklanır.
- Girişte `check_password_hash` ile karşılaştırılır. Hash'ten parolaya geri dönülemez.
- Parola en az 6 karakter olmalıdır (iş katmanında kontrol edilir).

## 2. Kimlik doğrulama ve oturum
- Giriş başarılı olunca kullanıcı bilgisi Flask **oturumunda (session)** tutulur.
- Oturum çerezi `secret_key` ile **imzalanır**. Kullanıcı çerezi değiştirirse imza geçersiz olur.
- Oturum **30 dakika** sonra sona erer. "Çıkış" ile oturum tamamen temizlenir.

## 3. Yetkilendirme (rol tabanlı erişim)
- Roller: `kullanici` ve `yonetici`.
- Kontrol **sunucu tarafında** `@giris_gerekli` ve `@yonetici_gerekli` decorator'ları ile yapılır.
- Sadece menüden linki gizlemek yeterli değildir. Adres elle yazılsa bile yetkisiz kullanıcı **403** hatası alır.

## 4. Diğer önlemler
- **SQL Injection:** Tüm sorgularda `?` parametreleri kullanılır, kullanıcı girdisi SQL'e doğrudan eklenmez.
- **Kullanıcı numaralandırma:** Hatalı girişte "e-posta veya parola hatalı" denir, hangisinin yanlış olduğu söylenmez.
- **Tekrar kayıt:** E-posta sütunu `UNIQUE`, aynı e-postayla iki hesap açılamaz.
- **Gizli anahtar:** `secret_key` ortam değişkeninden (`SECRET_KEY`) okunur. `.env` dosyası `.gitignore` ile depodan hariç tutulur.

## 5. Bilinen sınırlamalar (geliştirilecek)
- Başarısız giriş denemesi sınırı (brute-force koruması) henüz yok.
- CSRF koruması (ör. Flask-WTF) eklenebilir.
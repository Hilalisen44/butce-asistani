"""
Uygulamanın giriş noktası. Sayfa adresleri (route) burada tanımlanır.
"""
import os
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session

from is_katmani.kimlik import kayit_ol, giris_dogrula, KimlikHatasi
from sunum.yetki import giris_gerekli, yonetici_gerekli

from is_katmani.islem_kurallari import islem_kaydet, islem_kaldir, bakiye_ozeti, IslemHatasi
from veri import islem_veri, kategori_veri
from datetime import date
app = Flask(__name__, template_folder="sunum/sablonlar")

# Oturum çerezini imzalamak için gizli anahtar.
# Gerçek kullanımda ortam değişkeninden (.env) okunur, koda yazılmaz.
app.secret_key = os.environ.get("SECRET_KEY", "gelistirme-icin-gecici-anahtar")
app.permanent_session_lifetime = timedelta(minutes=30)   # 30 dk sonra oturum düşer


@app.route("/")
def ana_sayfa():
    if session.get("kullanici_id"):
        return redirect(url_for("panel"))
    return redirect(url_for("giris"))


@app.route("/kayit", methods=["GET", "POST"])
def kayit():
    if request.method == "POST":
        try:
            kayit_ol(request.form["ad"], request.form["eposta"], request.form["parola"])
            flash("Kayit basarili! Simdi giris yapabilirsin.", "basari")
            return redirect(url_for("giris"))
        except KimlikHatasi as hata:
            flash(str(hata), "hata")
    return render_template("kayit.html")


@app.route("/giris", methods=["GET", "POST"])
def giris():
    if request.method == "POST":
        try:
            kullanici = giris_dogrula(request.form["eposta"], request.form["parola"])
            session.clear()
            session.permanent = True
            session["kullanici_id"] = kullanici["id"]
            session["ad"] = kullanici["ad"]
            session["rol"] = kullanici["rol"]
            flash("Giris basarili.", "basari")
            return redirect(url_for("panel"))
        except KimlikHatasi as hata:
            flash(str(hata), "hata")
    return render_template("giris.html")


@app.route("/cikis")
def cikis():
    session.clear()
    flash("Cikis yaptin.", "basari")
    return redirect(url_for("giris"))


@app.route("/panel")
@giris_gerekli
def panel():
    return render_template("panel.html")


@app.route("/yonetici")
@yonetici_gerekli
def yonetici():
    return render_template("yonetici.html")


@app.errorhandler(403)
def yetkisiz(hata):
    return "<h2>403 - Bu sayfaya erisim yetkin yok.</h2><a href='/panel'>Panele don</a>", 403




# ---------------- Gelir / Gider (Hafta 6) ----------------
@app.route("/islemler", methods=["GET", "POST"])
@giris_gerekli
def islemler():
    kullanici_id = session["kullanici_id"]

    # Yeni işlem ekleme (form gönderildiyse)
    if request.method == "POST":
        try:
            islem_kaydet(
                kullanici_id,
                request.form.get("kategori_id"),
                request.form.get("tutar"),
                request.form.get("tarih"),
                request.form.get("aciklama"),
            )
            flash("Islem eklendi.", "basari")
        except IslemHatasi as hata:
            flash(str(hata), "hata")
        return redirect(url_for("islemler"))

    # Listeleme + filtre
    filtre = {
        "kategori": request.args.get("kategori", ""),
        "baslangic": request.args.get("baslangic", ""),
        "bitis": request.args.get("bitis", ""),
        "arama": request.args.get("arama", "").strip(),
    }
    liste = islem_veri.islemleri_listele(
        kullanici_id,
        kategori_id=filtre["kategori"] or None,
        arama=filtre["arama"] or None,
        baslangic=filtre["baslangic"] or None,
        bitis=filtre["bitis"] or None,
    )
    return render_template(
        "islemler.html",
        islemler=liste,
        kategoriler=kategori_veri.kategorileri_listele(),
        ozet=bakiye_ozeti(kullanici_id),
        filtre=filtre,
        bugun=date.today().isoformat(),
    )


@app.route("/islemler/<int:islem_id>/sil", methods=["POST"])
@giris_gerekli
def islem_silme(islem_id):
    try:
        islem_kaldir(session["kullanici_id"], islem_id)
        flash("Islem silindi.", "basari")
    except IslemHatasi as hata:
        flash(str(hata), "hata")
    return redirect(url_for("islemler"))
if __name__ == "__main__":
    app.run(debug=True)
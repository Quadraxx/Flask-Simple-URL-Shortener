# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers import Response
import os
import random
import string

# --- Uygulama Yapılandırması ---
app = Flask(__name__)

# Gerekli kütüphaneleri kurduğunuzdan emin olun: pip install Flask Flask-SQLAlchemy pyodbc
# Not: Bu bağlantı, localhost\SQLEXPRESS'e Windows Kimlik Doğrulaması ile bağlanır.
# "urldata_huseyin" veritabanını SSMS'te manuel olarak oluşturmalısınız!
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc:///?odbc_connect='
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=urldata_huseyin;'
    'Trusted_Connection=yes;' 
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sizin_guclu_gizli_anahtarınız' # Flash mesajları için gerekli

# Veritabanı nesnesi oluşturma
db = SQLAlchemy(app)

# --- Veritabanı Modeli: URL_KAYIT ---
class UrlKayit(db.Model):
    __tablename__ = 'url_kayit'
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<UrlKayit {self.short_code}>'

# --- Yardımcı Fonksiyon: Kısa Kod Üretimi ---
def generate_short_code(length=6):
    """6 karakter uzunluğunda rastgele, benzersiz kısa kod üretir."""
    characters = string.ascii_letters + string.digits
    
    while True:
        short_code = ''.join(random.choice(characters) for _ in range(length))
        
        # Kodun veritabanında benzersiz olup olmadığını kontrol et
        if not UrlKayit.query.filter_by(short_code=short_code).first():
            return short_code

# --- Rotalar (Routes) ---
# Anasayfa: Formu Gösterir
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        
        if not original_url:
            flash('Lütfen geçerli bir URL girin!', 'error')
            return redirect(url_for('index'))
        
        # 1. Kısa kodu üret
        short_code = generate_short_code()
        
        # 2. Veritabanına kaydet
        try:
            new_entry = UrlKayit(original_url=original_url, short_code=short_code)
            db.session.add(new_entry)
            db.session.commit()
            
            # Başarılı mesajı göster
            flash(f'URL başarıyla kısaltıldı! Kısa kodunuz: {short_code}', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Bir hata oluştu: {e}', 'error')
            return redirect(url_for('index'))
            
        # Başarı mesajını göstermesi için anasayfaya yönlendiriyoruz
        return redirect(url_for('index'))
    
    # Tüm kayıtları ana sayfada göstermek için
    all_urls = UrlKayit.query.all()
    return render_template('index.html', all_urls=all_urls)

# Yönlendirme Rotası: Kısa Kodu Kullanarak Orijinal URL'ye Yönlendirir
@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Kullanıcı kısa URL'yi ziyaret ettiğinde orijinal adrese yönlendirir."""
    
    # Veritabanında kodu ara
    link = UrlKayit.query.filter_by(short_code=short_code).first()
    
    if link:
        # Link bulunursa orijinal URL'ye yönlendir
        return redirect(link.original_url)
    else:
        # Link bulunamazsa 404 sayfasına yönlendir veya hata göster
        flash('Bu kısaltılmış URL bulunamadı!', 'error')
        return redirect(url_for('index'))


# --- Uygulama Başlangıcı ---
if __name__ == '__main__':
    # Veritabanı tablolarını oluşturma/güncelleme (SQL Server'da DB var sayılır)
    with app.app_context():
        try:
            db.create_all()
            print("\n---------------------------------------------------------")
            print("Veritabanı tabloları (URL_KAYIT) başarıyla oluşturuldu/kontrol edildi.")
            print("SQL Server'daki urldata_huseyin veritabanına bağlı.")
            print("---------------------------------------------------------\n")
        except Exception as e:
            print(f"\nHATA: Veritabanı bağlantısı veya tablo oluşturma sorunu. SSMS'te 'urldata_huseyin' adlı DB'nin var olduğundan emin olun.")
            print(f"Hata Detayı: {e}\n")

    # Uygulamayı başlat
    app.run(debug=True)
import json
import random
import datetime

# --- AYARLAR ---
json_dosyasi = 'urunler_kategorili_final_tam.json'
sql_dosyasi = 'fake_yorumlar_pro.sql'

# --- 1. GENİŞLETİLMİŞ İSİM HAVUZU (100+ Kombinasyon) ---
erkek_isimler = ["Ahmet", "Mehmet", "Mustafa", "Caner", "Burak", "Emre", "Volkan", "Serkan", "Oğuz", "Ali", "Hakan", "Yusuf", "Murat", "Ömer", "İbrahim", "Halil", "Süleyman", "Fatih", "Gökhan", "Uğur", "Selim", "Kaan", "Mert", "Arda", "Efe", "Kerem"]
kadin_isimler = ["Ayşe", "Fatma", "Zeynep", "Elif", "Merve", "Selin", "Gamze", "Esra", "Büşra", "Kübra", "Seda", "Gizem", "Derya", "Deniz", "Pınar", "Ece", "İrem", "Aslı", "Begüm", "Ceren", "Duygu", "Ebru", "Filiz", "Gülşah", "Hande"]
soyad_bas_harfleri = ["K.", "Y.", "T.", "S.", "B.", "D.", "A.", "E.", "Ö.", "G.", "Ç.", "U.", "Ş.", "V.", "Z.", "P.", "R.", "L.", "M.", "N."]

def rastgele_isim_uret():
    isim_listesi = erkek_isimler + kadin_isimler
    isim = random.choice(isim_listesi)
    soyad = random.choice(soyad_bas_harfleri)
    # %20 ihtimalle iki isimli olsun (Örn: Ahmet Can K.)
    if random.random() > 0.8:
        ikinci_isim = random.choice(isim_listesi)
        return f"{isim} {ikinci_isim} {soyad}"
    return f"{isim} {soyad}"

# --- 2. YORUM PARÇALARI (Dinamik Cümle Oluşturma) ---
# Yorumlar şu formülde oluşacak: [Giriş] + [Detay] + [Sonuç] + [Emoji]

giris_cumleleri = [
    "Bayıldım!", "Ürün elime ulaştı.", "Harika bir tablo.", "Paketleme çok özenliydi.", 
    "Beklediğimden çok daha iyi.", "Salonuma hava kattı.", "Kargo çok hızlıydı.", 
    "Açıkçası tereddüt etmiştim ama,", "Eşime hediye aldım,", "Ofis için sipariş vermiştim,"
]

detay_cumleleri = [
    "Renkleri gerçekten çok canlı.", "{baslik} detayları muazzam görünüyor.", 
    "Kumaş kalitesi ve baskı netliği harika.", "Çerçevesi oldukça sağlam.", 
    "Duvara asması çok kolay oldu.", "Fotoğrafta göründüğünden daha kaliteli.", 
    "Odaya bambaşka bir derinlik kattı.", "Baskı kalitesi beni şaşırttı.",
    "Paketlemesi o kadar iyiydi ki açmakta zorlandım :)", "Fiyatına göre performansı çok yüksek."
]

sonuc_cumleleri = [
    "Kesinlikle tavsiye ederim.", "Teşekkürler.", "Hiç düşünmeden alabilirsiniz.", 
    "Elinize emeğinize sağlık.", "Tekrar sipariş vereceğim.", "Çok memnun kaldım.",
    "Herkese öneririm.", "Parasını sonuna kadar hak ediyor.", "Mükemmel işçilik.", "10 numara 5 yıldız."
]

kisa_yorumlar = [
    "Süper.", "Çok beğendim.", "Harika.", "Kaliteli ürün.", "Teşekkürler.", 
    "Tavsiye ederim.", "Renkler canlı.", "Kargo hızlı.", "10/10", "Gayet başarılı.",
    "Mükemmel.", "Efsane.", "Çok şık.", "Bayıldım.", "Güzel paketleme."
]

emojiler = ["👍", "🔥", "😊", "👏", "❤️", "⭐", "🤩", "👌", "🙏", "✨"]

def yorum_uret(baslik, puan):
    # Eğer puan düşükse (4 yıldız) biraz daha mesafeli yorum yap
    if puan == 4:
        return random.choice([
            "Ürün güzel ama kargo bir gün geç geldi. Yine de {baslik} kaliteli.",
            "Baskı kalitesi iyi, çerçeve biraz daha kalın olabilirdi ama şık duruyor.",
            "Fiyat performans ürünü, genel olarak memnunum.",
            "Güzel ürün, paketleme biraz daha özenli olabilirdi ama hasarsız geldi.",
            "Beklediğim gibi geldi, teşekkürler."
        ])

    # %30 ihtimalle KISA yorum yap (Gerçekçilik için)
    if random.random() < 0.3:
        yorum = random.choice(kisa_yorumlar)
        if random.random() > 0.5: yorum += " " + random.choice(emojiler)
        return yorum

    # %70 ihtimalle UZUN ve DETAYLI yorum yap
    giris = random.choice(giris_cumleleri)
    detay = random.choice(detay_cumleleri).replace("{baslik}", baslik)
    sonuc = random.choice(sonuc_cumleleri)
    
    yorum = f"{giris} {detay} {sonuc}"
    
    # %50 ihtimalle emoji ekle
    if random.random() > 0.5:
        yorum += " " + random.choice(emojiler)
        
    return yorum

def tarih_uret():
    # Son 4 ay (120 gün) içinde, yoğunluk son 1 ayda olacak şekilde
    gunler = list(range(1, 120))
    # Ağırlıklı rastgelelik (Yakın tarihler daha çok çıksın)
    agirliklar = [1/(i+1) for i in gunler] 
    gun_farki = random.choices(gunler, weights=agirliklar, k=1)[0]
    
    tarih = datetime.datetime.now() - datetime.timedelta(days=gun_farki)
    
    # Rastgele saat ekle (09:00 - 23:00 arası)
    saat = random.randint(9, 23)
    dakika = random.randint(0, 59)
    saniye = random.randint(0, 59)
    
    yeni_tarih = tarih.replace(hour=saat, minute=dakika, second=saniye)
    return yeni_tarih.strftime("%Y-%m-%d %H:%M:%S")

def urun_adi_kisalt(baslik):
    # Ürün adını doğal bir şekilde kısalt
    kelimeler = baslik.split()
    if len(kelimeler) > 3:
        # "Manzara Sandallı Kanvas Tablo" -> "Manzara Sandallı tablosu" gibi yap
        return " ".join(kelimeler[:random.randint(2, 3)])
    return baslik

# --- İŞLEM BAŞLIYOR ---
print("JSON okunuyor...")
try:
    with open(json_dosyasi, 'r', encoding='utf-8') as f:
        urunler = json.load(f)
except FileNotFoundError:
    print(f"HATA: '{json_dosyasi}' bulunamadı.")
    exit()

sql_komutlari = []
sql_komutlari.append("BEGIN;")

# Önce eski fake yorumları temizlemek istersen bu satırı aç:
# sql_komutlari.append('DELETE FROM "Yorumlar" WHERE "AppUserId" IS NULL;') 

toplam_yorum = 0

print(f"Toplam {len(urunler)} ürün için yorumlar hazırlanıyor...")

for urun in urunler:
    baslik = urun.get('Baslik')
    if not baslik: continue
    
    safe_baslik = baslik.replace("'", "''")
    kisa_baslik = urun_adi_kisalt(baslik)

    # Bu ürüne kaç yorum yapılsın? (2 ile 7 arası rastgele)
    yorum_sayisi = random.randint(2, 7)

    for _ in range(yorum_sayisi):
        # Puan belirle (%90 ihtimalle 5, %10 ihtimalle 4)
        # Hiçbir ürüne 3 ve altı vermiyoruz ki ortalama düşmesin
        puan = 5 if random.random() > 0.1 else 4
        
        # Yorum metnini oluştur (Yapay Zeka benzeri çeşitlilik)
        yorum_metni = yorum_uret(kisa_baslik, puan)
        
        # SQL'de kesme işareti hatasını önle
        safe_yorum = yorum_metni.replace("'", "''")
        
        isim = rastgele_isim_uret()
        tarih = tarih_uret()

        # SQL Oluştur (GÜVENLİ ID BULMA YÖNTEMİYLE)
        # OnayliMi = true (Direkt yayında)
        # AppUserId = NULL (Bot olduğu belli olmasın ama sistem bilsin)
        sql = f"""
        INSERT INTO "Yorumlar" ("UrunId", "AdSoyad", "YorumMetni", "Puan", "OnayliMi", "OlusturulmaTarihi", "SilindiMi")
        SELECT "Id", '{isim}', '{safe_yorum}', {puan}, true, '{tarih}', false
        FROM "Urunler" WHERE "Baslik" = '{safe_baslik}';
        """
        sql_komutlari.append(sql)
        toplam_yorum += 1

sql_komutlari.append("COMMIT;")

with open(sql_dosyasi, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_komutlari))

print(f"\n✅ İŞLEM TAMAMLANDI!")
print(f"📝 Toplam {toplam_yorum} adet, birbirinden farklı, doğal görünümlü yorum oluşturuldu.")
print(f"📂 '{sql_dosyasi}' dosyasını PgAdmin'de çalıştırabilirsin.")
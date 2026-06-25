# CANVASIA Railway Deployment Rehberi

Bu rehber, mevcut Ubuntu + Docker kurulumundan Railway'e güvenli geçiş içindir.

## 1. GitHub'a göndermeden önce yerelde kontrol

```bash
git status
dotnet build KanvasProje.sln
docker build -t canvasia-railway-test .
docker run --rm -p 8080:8080 \
  -e PORT=8080 \
  -e DOTNET_RUNNING_IN_CONTAINER=true \
  -e PERSISTENT_ROOT=/app/storage \
  canvasia-railway-test
```

Ayrı terminalde kontrol:

```bash
curl http://localhost:8080/health
```

## 2. Mevcut Ubuntu sunucuda yedek al

Railway'e geçmeden önce mutlaka veritabanı ve dosya yedeği al:

```bash
cd ~/canvasia
mkdir -p ~/railway-migration-backups

docker exec kanvasproje-db pg_dump -U kanvasuser -d kanvasdb -Fc > ~/railway-migration-backups/canvasia_before_railway_$(date +%Y%m%d_%H%M%S).dump

tar -czf ~/railway-migration-backups/canvasia_files_before_railway_$(date +%Y%m%d_%H%M%S).tar.gz \
  ~/canvasia/KanvasProje.Web/wwwroot/img \
  ~/canvasia/KanvasProje.Web/wwwroot/media \
  ~/canvasia/KanvasProje.Web/wwwroot/uploads \
  ~/canvasia/KanvasProje.Web/wwwroot/video \
  ~/canvasia/KanvasProje.Web/App_Data
```

Bu iki yedeği bilgisayarına indir:

```powershell
scp abdulmuin@canvasia-server:~/railway-migration-backups/canvasia_before_railway_*.dump C:\Users\abdul\Downloads\
scp abdulmuin@canvasia-server:~/railway-migration-backups/canvasia_files_before_railway_*.tar.gz C:\Users\abdul\Downloads\
```

## 3. Railway projesi oluştur

1. Railway'de yeni project oluştur.
2. GitHub repo'yu bağla: `abdulmuin-said/meteorgaleri_canvasia`.
3. PostgreSQL service ekle.
4. Web service'e bir Volume ekle.

Volume mount path:

```text
/app/storage
```

> `/app/wwwroot` üzerine volume bağlama. Bu, CSS/JS/static dosyaları gizler.

## 4. Railway Web Service değişkenleri

Railway Web Service > Variables alanına ekle:

```text
ASPNETCORE_ENVIRONMENT=Production
DOTNET_RUNNING_IN_CONTAINER=true
PERSISTENT_ROOT=/app/storage
```

PostgreSQL bağlantısı:

```text
ConnectionStrings__DefaultConnection=Host=${{Postgres.PGHOST}};Port=${{Postgres.PGPORT}};Database=${{Postgres.PGDATABASE}};Username=${{Postgres.PGUSER}};Password=${{Postgres.PGPASSWORD}};SSL Mode=Require;Trust Server Certificate=true
```

E-posta ayarlarını mevcut `.env` veya sunucudan kopyala:

```text
EmailSettings__Host=smtp-relay.brevo.com
EmailSettings__Port=587
EmailSettings__EnableSSL=true
EmailSettings__Username=<Brevo SMTP kullanıcı adı>
EmailSettings__Password=<Brevo SMTP anahtarı>
EmailSettings__FromEmail=<doğrulanmış gönderici e-posta>
EmailSettings__FromName=Canvasia
```

Volume izin sorunu olursa ayrıca ekle:

```text
RAILWAY_RUN_UID=0
```

## 5. Railway PostgreSQL'e veritabanı yükle

Railway PostgreSQL bağlantı URL'sini panelden al. Sonra bilgisayarında veya sunucuda:

```bash
pg_restore --clean --if-exists --no-owner --no-privileges \
  -d "<RAILWAY_DATABASE_URL>" \
  canvasia_before_railway_YYYYMMDD_HHMMSS.dump
```

SQL dump kullanırsan:

```bash
psql "<RAILWAY_DATABASE_URL>" < kanvasdb_yedek.sql
```

## 6. Dosya yedeğini Railway Volume'a taşı

Dosya yedeğindeki klasörler Railway volume altında şu hedeflere gitmeli:

```text
/app/storage/uploads
/app/storage/img/products
/app/storage/media/products
/app/storage/App_Data
```

Önemli: `App_Data/DataProtectionKeys` taşınmazsa, veritabanındaki şifreli PayTR Merchant Key/Salt çözülemeyebilir. Böyle olursa admin panelinden PayTR bilgilerini tekrar gir.

## 7. Railway geçici domain üzerinde test

DNS değiştirmeden önce Railway'in verdiği geçici domain üzerinde test et:

- `/health`
- Ana sayfa slider video/görseller
- Ürün listesi ve detay sayfaları
- Ürün görselleri
- Admin giriş
- Slider yükleme/düzenleme
- Sepet ve ödeme akışı
- PayTR test modu
- E-posta gönderimi

## 8. Cloudflare DNS geçişi

Railway testleri başarılıysa:

1. Railway Web Service > Settings > Domains.
2. `www.canvasia.com.tr` custom domain ekle.
3. Railway'in verdiği CNAME değerini kopyala.
4. Cloudflare DNS'te `www` kaydını Railway CNAME hedefine çevir.
5. Geçiş sırasında Cloudflare Development Mode aç veya cache'i bypass et.
6. Site Railway'de sorunsuz çalışınca eski Ubuntu servisini hemen silme; birkaç gün yedek olarak tut.

## 9. PayTR URL'leri

Domain aynı kalırsa PayTR panelindeki URL'ler aynı kalır:

```text
Bildirim URL: https://www.canvasia.com.tr/Siparis/PaytrBildirim
Başarılı URL: https://www.canvasia.com.tr/Siparis/PaytrBasarili?siparisNo={merchant_oid}
Başarısız URL: https://www.canvasia.com.tr/Siparis/PaytrBasarisiz
```

## 10. Sorun olursa hızlı kontrol

Railway loglarında bakılacaklar:

- Database connection hatası
- Volume permission hatası
- `/health` failure
- DataProtection key / PayTR decrypt hatası
- 404 veren upload dosyaları

En güvenli geri dönüş planı: Cloudflare DNS'i eski Ubuntu sunucuya geri çevir ve Ubuntu Docker servislerini yeniden başlat.

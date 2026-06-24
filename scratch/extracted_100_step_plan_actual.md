# Filistin E-Ticaret Projesi (7ANRPS48.com) Master Yol Haritası ve Uygulama Planı

Bu plan, mevcut `MeteorGaleri` (Canvasia) projesini temel alarak Filistin'deki müşteriniz için yeni e-ticaret sitesini (`7ANRPS48.com`) sıfırdan inşa etmek, veritabanını temizlemek, Arapça dil ve RTL (sağdan sola) tasarımı entegre etmek ve istenen tüm yeni özellikleri eklemek için **100 adımlık detaylı bir yol haritası** sunmaktadır.

---

## Proje Bilgileri ve Gereksinim Özetleri
- **Site Adı**: `7ANRPS48.com`
- **Para Birimi**: `₪` (ILS - Yeni İsrail Şekeli)
- **Hedef Dil**: Arapça (RTL) ve Türkçe/İngilizce destekli çoklu dil yapısı
- **Proje Konumu**: `E:\Projeler\filistin_eticaret_projesi`
- **Ana Ödeme Yöntemleri**: Kapıda Ödeme (Cash on Delivery) ve Banka Havalesi (Çevrimiçi POS entegrasyonu istenmiyor, admin panelinden açılıp kapatılabilir olacak).
- **Özel Koşullar**: Reçete yükleme gerektiren ilaçlar, yüksek fiyatlı ürünler için kapıda ödeme kısıtı (>2000 ILS), toptancı (wholesale) girişi ve özel fiyatlandırma.

---

## 100 Adımlık Yol Haritası (Master Plan)

### FAZ 1: Proje Başlatma ve Temiz Klonlama (1 - 10)
- [ ] **Adım 1**: `E:\Projeler\filistin_eticaret_projesi` klasörünü oluşturun.
- [ ] **Adım 2**: `MeteorGaleri` projesindeki tüm kaynak kod klasörlerini (`KanvasProje.Core`, `KanvasProje.Data`, `KanvasProje.Service`, `KanvasProje.Web` vb.) yeni klasöre kopyalayın.
- [ ] **Adım 3**: Kopyalama esnasında `.git` geçmişini, `bin`, `obj`, `node_modules` klasörlerini ve yerel veritabanı dump/yedek dosyalarını hariç tutun.
- [ ] **Adım 4**: `appsettings.json` ve `appsettings.Development.json` dosyalarındaki veritabanı bağlantı dizesini (Connection String) yeni veritabanı adı (`filistindb`) olacak şekilde güncelleyin.
- [ ] **Adım 5**: Docker Compose kullanılıyorsa, `docker-compose.yml` içindeki container adlarını, veritabanı adını ve port tanımlarını çakışmayacak şekilde düzenleyin (Örn: `filistin-web`, `filistin-db`).
- [ ] **Adım 6**: Projedeki eski yüklenmiş resimleri temizlemek için `wwwroot/img/products` ve `wwwroot/media/products` klasörlerinin içini boşaltın (örnek görseller hariç).
- [ ] **Adım 7**: `KanvasProje.sln` çözüm dosyasını Visual Studio veya VS Code ile açarak referansların doğru bağlandığını doğrulayın.
- [ ] **Adım 8**: Projeyi yerel ortamda ilk kez derleyin (`dotnet build`) ve derleme hataları varsa giderin.
- [ ] **Adım 9**: Yeni proje için temiz bir Git deposu başlatın (`git init`) ve ilk commit'i yapın.
- [ ] **Adım 10**: Logları temizleyin (`logs/` dizini altındaki eski log dosyalarını silin).

### FAZ 2: Veritabanı Temizliği ve Yapılandırılması (11 - 20)
- [ ] **Adım 11**: PostgreSQL üzerinde `filistindb` adında boş bir veritabanı oluşturun.
- [ ] **Adım 12**: Entity Framework Core Migration'larını uygulayarak veritabanı tablolarını sıfırdan oluşturun (`dotnet ef database update`).
- [ ] **Adım 13**: Veritabanındaki eski ürünleri, kategorileri, yorumları, sepetleri, kuponları ve sipariş verilerini temizleyecek SQL temizleme betiğini hazırlayın ve çalıştırın.
- [ ] **Adım 14**: `SiteSettings` veya `Ayarlar` tablosundaki varsayılan değerleri güncelleyin (E-posta ayarları, mağaza ismi vb.).
- [ ] **Adım 15**: Para birimi simgesi alanını veya veritabanındaki para birimi gösterimlerini `₪` (ILS) olarak ayarlayın.
- [ ] **Adım 16**: Ürün tablosuna (`Urunler`) `WholesalePrice` (Toptan Fiyat) alanı eklemek için yeni bir migration oluşturun.
- [ ] **Adım 17**: Ürün seçenekleri/varyasyonları tablosuna (`UrunSecenekleri`) stok miktarı (`StokAdet`) ve varyasyona özel fiyat artış/azalış miktarı sütunlarını ekleyin.
- [ ] **Adım 18**: Kullanıcı tablosuna (`Musteriler` veya `AspNetUsers`) `KimlikNo` (National ID) ve `KimlikFotografYolu` (Identity Image Path) alanlarını ekleyin.
- [ ] **Adım 19**: Siparişler tablosuna teslimat tipi (`TeslimatTipi`: Adrese Teslim / Mağazadan Teslim) ve `ReçeteDosyaYolu` alanlarını ekleyin.
- [ ] **Adım 20**: Migration'ları veritabanına uygulayarak şemayı güncelleyin.

### FAZ 3: Çoklu Dil (Arapça-Türkçe) ve RTL Tasarım Altyapısı (21 - 30)
- [ ] **Adım 21**: ASP.NET Core Localization (`RequestLocalizationOptions`) servisini `Program.cs` üzerinde yapılandırın.
- [ ] **Adım 22**: Dil dosyalarını (.resx) oluşturun: `SharedResource.ar.resx` ve `SharedResource.tr.resx`.
- [ ] **Adım 23**: Kullanıcının üst barda veya ayarlarda dil seçebileceği dil değiştirici (Language Switcher) bileşenini ekleyin.
- [ ] **Adım 24**: Arapça seçildiğinde HTML etiketine `dir="rtl"` özniteliğini ekleyecek mantığı `_Layout.cshtml` şablonuna yazın.
- [ ] **Adım 25**: RTL uyumlu TailwindCSS veya genel CSS kurallarını oluşturun (Flex yönlendirmeleri, hizalamalar ve kenar boşluklarının tersine dönmesi).
- [ ] **Adım 26**: Font ailesini Arapça karakterlere uygun ve modern duran bir fontla (örneğin Google Fonts'tan "Cairo" veya "Tajawal") güncelleyin.
- [ ] **Adım 27**: Yönetim panelinin (Admin Panel) çoklu dil desteğini hazırlayın.
- [ ] **Adım 28**: Ürün ve Kategori açıklamalarının veritabanında çok dilli saklanabilmesi için şemayı veya JSON tabanlı çeviri yapısını kurun.
- [ ] **Adım 29**: RTL modunda kaydırıcı (Slider) ve karusel (Carousel) bileşenlerinin yönlerini düzeltin.
- [ ] **Adım 30**: Arayüzdeki tüm statik metinleri dil kaynaklarından (`IStringLocalizer`) okuyacak şekilde güncelleyin.

### FAZ 4: Üyelik, Profil ve Kimlik Doğrulama Sistemi (31 - 40)
- [ ] **Adım 31**: Kayıt Ol (`Register`) sayfasını Arapça form alanlarıyla tasarlayın: İsim, Soyisim, Kimlik Numarası (National ID), Doğum Tarihi, Telefon, Adres.
- [ ] **Adım 32**: Kayıt esnasında kimlik resmi yükleme alanını (`input type="file"`) ekleyin.
- [ ] **Adım 33**: Yüklenen kimlik resimlerinin güvenli bir şekilde sunucuda saklanması için dosya yükleme servisini yazın.
- [ ] **Adım 34**: Kayıt formuna kimlik resmi yüklemenin zorunlu olduğuna dair uyarı/bilgilendirme mesajları ekleyin.
- [ ] **Adım 35**: Giriş yapma ekranını (Login) "Giriş Yapmak Zorunludur/İhtiyaridir" parametresine göre açıp kapatan ayar mekanizmasını kodlayın.
- [ ] **Adım 36**: Müşteri profil sayfasına kimlik bilgilerini ve yüklenen kimlik görselini görüntüleme alanı ekleyin.
- [ ] **Adım 37**: Müşteri kontrol panelinde geçmiş siparişlerin takibi ve sipariş iptali sayfalarını oluşturun.
- [ ] **Adım 38**: Toptan Satış Müşterisi (`Wholesale`) rolünü tanımlayın.
- [ ] **Adım 39**: Toptancı kayıt formu ve admin onay mekanizmasını hazırlayın (Admin onaylamadan toptancı fiyatları görünmeyecek).
- [ ] **Adım 40**: Şifre sıfırlama ve hesap doğrulama e-postalarını Arapça ve Türkçe şablonlarıyla entegre edin.

### FAZ 5: Ürün Sayfası, Varyasyonlar ve Gelişmiş Filtreleme (41 - 50)
- [ ] **Adım 41**: Ürün detay sayfasını Filistin projesinin gereksinimlerine göre yeniden tasarlayın.
- [ ] **Adım 42**: Ürün detay sayfasında renk ve boyut seçim alanlarını dinamikleştirin.
- [ ] **Adım 43**: Seçilen renk ve boyuta göre ürün fiyatının dinamik olarak artmasını veya değişmesini sağlayan JavaScript altyapısını kurun.
- [ ] **Adım 44**: Stok miktarı 5'in altına düştüğünde çıkacak olan "Son 5 Adet! Acele Edin!" uyarısını arayüze ekleyin.
- [ ] **Adım 45**: Ürün puanlama ve yorum (yıldız ve yorum metni) sistemini entegre edin.
- [ ] **Adım 46**: Genel site/mağaza değerlendirme sistemi (Store Review) için ayrı bir değerlendirme sayfası tasarlayın.
- [ ] **Adım 47**: Ürün varyasyon stok takibini yapın. Eğer seçilen varyasyonun (örneğin Kırmızı - L Beden) stoğu tükendiyse, o seçeneğin seçilmesini engelleyin (gray-out yapın).
- [ ] **Adım 48**: Ürün detayına "Ekstra Hizmet" (Hediye Paketi vb.) seçeneği ekleyin ve seçildiğinde fiyata otomatik eklenmesini sağlayın.
- [ ] **Adım 49**: Fiyat Aralığı Kaydırıcısı (Smart Price Filter Slider) bileşenini ürün listeleme sayfasına ekleyin.
- [ ] **Adım 50**: Kategori sayfasında marka, tür ve kategoriye göre gelişmiş tescilli filtre sistemini aktif edin.

### FAZ 6: Sepet ve Sipariş Mantığı (51 - 65)
- [ ] **Adım 51**: Sepet sayfasını Arapça/RTL olarak yeniden tasarlayın.
- [ ] **Adım 52**: Sağ alt köşede her zaman görünür kalan "Yüzen Sepet" (Floating Cart Icon) bileşenini ekleyin.
- [ ] **Adım 53**: Sepetteki tüm ürünleri tek seferde temizleme butonunu ekleyin.
- [ ] **Adım 54**: Ödeme sayfasında (Checkout) "Adrese Teslimat" ve "Mağazadan Teslim Alacağım" seçeneklerini sunun.
- [ ] **Adım 55**: Bölge ve şehre göre dinamik kargo ücreti hesaplama motorunu kurun.
- [ ] **Adım 56**: Belirli bir tutarın üzerindeki siparişlerde ücretsiz kargo hakkı tanıyan kampanya kontrolünü yapın.
- [ ] **Adım 57**: Ödeme sayfasına "Kamera ile Kimlik Fotoğrafı Çek / Yükle" özelliğini ekleyin (Mobil uyumlu WebRTC/HTML5 kamera API entegrasyonu).
- [ ] **Adım 58**: Ödeme sayfasında sipariş notu ekleme kutusunu ekleyin.
- [ ] **Adım 59**: Sipariş onayından önce "Kullanım Şartları ve Gizlilik Politikasını Kabul Ediyorum" onay kutusunu ekleyin.
- [ ] **Adım 60**: Banka havalesi seçildiğinde gösterilecek olan IBAN ve Banka bilgilerini admin panelinden yönetilebilir yapın.
- [ ] **Adım 61**: Kapıda Ödeme (Nakit) seçildiğinde eklenecek ek hizmet bedeli varsa bunu sepet toplamına ekleyen yapıyı kodlayın.
- [ ] **Adım 62**: 2000 ILS (veya adminin belirleyeceği limit) üzerindeki yüksek fiyatlı siparişlerde Kapıda Ödeme seçeneğini otomatik olarak gizleyin ve "Sadece Online/E-Ödeme veya İletişim" uyarısı verin.
- [ ] **Adım 63**: İlaç/Medikal kategorisindeki ürünler sepete eklendiğinde ödeme sayfasında reçete (roşeta) yükleme alanını zorunlu kılın.
- [ ] **Adım 64**: Çok pahalı veya özel üretim ürünler için "Fiyat Teklifi İste/Özel Sipariş" (Fiyatı olmayan ve WhatsApp'a yönlendiren) butonunu ürün detayına ekleyin.
- [ ] **Adım 65**: Sipariş tamamlandığında müşteriye ve yöneticiye bildirim e-postası gitmesini sağlayın.

### FAZ 7: Toptan Satış (Wholesale) Modülü (66 - 75)
- [ ] **Adım 66**: Toptancı giriş yaptıktan sonra sitenin tüm fiyat şablonlarının `WholesalePrice` değerlerini gösterecek şekilde güncellenmesini sağlayın.
- [ ] **Adım 67**: Toptancılar için minimum sipariş tutarı (Minimum Order Limit) kısıtlamasını sepet ve ödeme sayfalarında kontrol edin.
- [ ] **Adım 68**: Toptancılara özel ürün grupları veya toplu alım iskonto tablolarını hazırlayın.
- [ ] **Adım 69**: Admin panelinde toptancılardan gelen üyelik başvurularını onaylama/reddetme arayüzünü oluşturun.
- [ ] **Adım 70**: Toptancılara özel sipariş özet ekranı tasarlayın.
- [ ] **Adım 71**: Toptancıların cari hesap hareketlerini (Borç/Alacak/Bakiye) takip edebileceği temel bir cari kart yapısı kurun.
- [ ] **Adım 72**: Toptancıların sepet sayfasına Excel/CSV ile toplu ürün ekleyebilme özelliğini entegre edin.
- [ ] **Adım 73**: Toptancı siparişlerinde kapıda ödemeyi kapatıp sadece banka havalesi veya cari hesaba yazma seçeneği sunun.
- [ ] **Adım 74**: Toptan fiyatların sıradan ziyaretçilere tamamen gizli kalmasını güvence altına alın.
- [ ] **Adım 75**: Toptancılar için toplu fatura indirme arayüzünü ekleyin.

### FAZ 8: Pazarlama ve Dönüşüm Artırıcı Özellikler (76 - 85)
- [ ] **Adım 76**: İlk kez siteye girenlere veya belirli sayfalarda tetiklenen "Çarkıfelek" (Spin the Wheel) indirim/ücretsiz kargo çarkını ekleyin.
- [ ] **Adım 77**: İndirimli ürünler için geri sayım sayacı (Countdown Timer) bileşenini ürün kartlarına ve ürün detayına ekleyin.
- [ ] **Adım 78**: Ürün detay sayfasının altına "İlgili Ürünler" (Related Products) öneri bandını yerleştirin.
- [ ] **Adım 79**: Sağ alt köşeye yüzen WhatsApp İletişim Butonunu ve hızlı mesaj şablonunu ekleyin.
- [ ] **Adım 80**: Canlı Arama (Live/Instant Search) altyapısını kurun (Yazarken ürün resmi ve adıyla anlık öneriler).
- [ ] **Adım 81**: Ürün kartlarına "Favorilerime Ekle" (Wishlist - Kalp simgesi) özelliğini ekleyin.
- [ ] **Adım 82**: Profil sayfasında müşterinin kendi favori ürünlerini listeleyebileceği alanı oluşturun.
- [ ] **Adım 83**: Manşet/Haber Bandı (Marquee News Ticker) bileşenini sitenin en üstüne ekleyin ve admin panelinden düzenlenebilir kılın.
- [ ] **Adım 84**: Ürün fiyatının üstünü çizip indirim oranını belirten etiketleri (Fırsat, Yeni, İndirim vb.) dinamikleştirin.
- [ ] **Adım 85**: Web Push Bildirimleri (Firebase Cloud Messaging veya alternatif) entegrasyonu için altyapıyı hazırlayın.

### FAZ 9: Yönetim Paneli (Admin) Geliştirmeleri (86 - 95)
- [ ] **Adım 86**: Admin panelinde gelişmiş istatistik paneli (Dashboard) hazırlayın (En çok satan ürünler, en çok sipariş gelen bölgeler).
- [ ] **Adım 87**: Kupon Yönetimi sayfasını ekleyin (Kupon kodu, kullanım limiti, indirim oranı/tutarı, geçerlilik süresi).
- [ ] **Adım 88**: Personel Yetkilendirme sayfasını kodlayın (Farklı admin rollerine göre sipariş görme, ürün düzenleme yetkileri).
- [ ] **Adım 89**: Sipariş İptal Politikası Ayarlarını ekleyin (Sipariş geçildikten sonra kaç saat içinde müşterinin iptal edebileceği ayarı).
- [ ] **Adım 90**: Ürün stoğu tükendiğinde veya 5'in altına düştüğünde yöneticiye e-posta ile bildirim gönderen uyarı servisini yazın.
- [ ] **Adım 91**: Siparişler listesinde faturaları tek tuşla PDF formatında dışa aktarma (Export PDF Invoice) özelliğini ekleyin.
- [ ] **Adım 92**: Admin panelinden "Ürünü Gizle" (Satışı durdur) özelliğini ekleyin.
- [ ] **Adım 93**: Şehir ve Bölge bazlı kargo fiyat listesini yönetmek için Kargo Ayarları arayüzünü tasarlayın.
- [ ] **Adım 94**: Reçeteli (roşetalı) siparişlerin reçetelerini admin panelinden inceleme ve onaylama adımlarını yazın.
- [ ] **Adım 95**: Döviz kuru entegrasyonu veya manuel kur sabitleme ekranını admin paneline ekleyin.

### FAZ 10: Canlıya Alma, Test ve Optimizasyon (96 - 100)
- [ ] **Adım 96**: Tüm formların (Kayıt, Sepet, Ödeme, Reçete yükleme vb.) güvenlik testlerini yapın.
- [ ] **Adım 97**: Arayüzün mobil uyumluluğunu (Responsive) tüm popüler cihaz boyutlarında test edin.
- [ ] **Adım 98**: SEO meta etiketlerini, sitemap.xml ve robots.txt dosyalarını yapılandırın.
- [ ] **Adım 99**: Projeyi sunucuya (IIS / Docker / Linux VPS) dağıtın (Deploy).
- [ ] **Adım 100**: Tüm akışın (ürün ekleme, üye olma, sepet, kargo seçimi, ödeme, fatura üretimi) canlı ortamda son testlerini tamamlayıp projeyi teslim edin.

---

## Veritabanı Değişiklik Tablosu (Şema Değişiklikleri)

### [NEW] [Musteriler / AspNetUsers Ek Sütunlar]
- `KimlikNo` (varchar, 20): Müşterinin ulusal kimlik numarası.
- `KimlikFotografYolu` (varchar, 500): Yüklenen kimlik görselinin sunucu/bulut yolu.
- `MusteriTipi` (int): 0 = Standart Perakende, 1 = Toptancı (Wholesale).
- `ToptanOnayliMi` (boolean): Toptancı başvurusunun onay durumu.

### [NEW] [Urunler Ek Sütunlar]
- `ToptanFiyat` (decimal): Toptancı kullanıcılara gösterilecek özel fiyat.
- `IsRecipeRequired` (boolean): İlaç/reçete gerektiren ürün kontrolü.
- `IsSpecialOrder` (boolean): WhatsApp ile özel sipariş kontrolü.
- `IsHidden` (boolean): Ürünü gizleme/satıştan çekme seçeneği.

### [NEW] [KargoBölgeleri Tablosu]
- `Id` (int, Primary Key)
- `BolgeAdi` (varchar, 100)
- `SehirAdi` (varchar, 100)
- `KargoUcreti` (decimal)

---

## Doğrulama ve Test Planı

### Otomatik Testler
- Dil dosyalarının eksiksiz yüklenmesi ve her iki dilde de (`ar`, `tr`) anahtarların karşılığının bulunmasının birim testlerle kontrol edilmesi.
- Sepet toplam tutarı hesaplama fonksiyonunun (bölge kargo ücreti + ürün fiyatı + varyasyon ek fiyatı - kupon indirimi) birim testleri.

### Manuel Testler
1. **Çoklu Dil ve RTL Testi**: Siteye girip dil Arapça yapıldığında tüm arayüzün sağdan sola (RTL) kaydığı, form kutularının sağa yanaştığı ve Arapça yazıların düzgün göründüğü teyit edilecek.
2. **Kimlik ve Reçete Yükleme Testi**: Standart bir üye kayıt formunda kimlik resmi yüklenmeden kayıt olunmaya çalışıldığında hata verdiği; ödeme sayfasında reçeteli bir ürün varken reçete görseli yüklemeden siparişin tamamlanmadığı test edilecek.
3. **Yüksek Fiyat Limitli Kapıda Ödeme**: Toplam tutar 2000 ILS değerini aştığında ödeme sayfasında Kapıda Ödeme seçeneğinin pasifleştiği doğrulanacak.

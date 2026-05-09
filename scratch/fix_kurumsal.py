import os
import re

def rewrite_kurumsal_view(filepath, content_generator):
    with open(filepath, "r", encoding="utf-8") as f:
        old_content = f.read()
    
    # Try to extract the title
    title_match = re.search(r'ViewData\["Title"\]\s*=\s*"(.*?)";', old_content)
    title = title_match.group(1) if title_match else "Kurumsal"
    
    new_content = f"""@{{
    ViewData["Title"] = "{title}";
}}

<!-- Breadcrumb -->
<div class="bg-[#f1ede7] border-b border-[#e5e2dc] py-3">
    <div class="container mx-auto px-4 flex items-center gap-2 text-xs text-[#47473d]">
        <a href="/" class="hover:text-[#313511] transition-colors">Ana Sayfa</a>
        <span>/</span>
        <span class="text-[#1c1c18] font-medium">{title}</span>
    </div>
</div>

<div class="container mx-auto px-4 py-16 max-w-4xl">
    <div class="text-center mb-12">
        <h1 class="font-serif text-3xl md:text-5xl text-[#313511] mb-4">{title}</h1>
        <div class="w-16 h-1 bg-[#b58735] mx-auto"></div>
    </div>
    
    <div class="bg-white border border-[#e5e2dc] rounded-lg p-8 md:p-12 shadow-sm prose prose-sm md:prose-base max-w-none prose-headings:font-serif prose-headings:text-[#313511] prose-a:text-[#b58735] prose-strong:text-[#1c1c18]">
        {content_generator()}
    </div>
</div>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)


def get_gizlilik_content():
    return """
        <h2>Giriş</h2>
        <p>Canvasia ("biz", "bizim" veya "şirketimiz") olarak kişisel verilerinizin güvenliğine büyük önem veriyoruz. Bu gizlilik politikası, web sitemizi kullanırken topladığımız bilgilerin nasıl korunduğunu açıklar.</p>
        
        <h2>Toplanan Bilgiler</h2>
        <p>Sipariş süreci ve iletişim formu aracılığıyla şu bilgileri toplayabiliriz:</p>
        <ul>
            <li>Ad ve Soyad</li>
            <li>E-posta adresi</li>
            <li>Telefon numarası</li>
            <li>Teslimat ve fatura adresleri</li>
        </ul>

        <h2>Bilgilerin Kullanımı</h2>
        <p>Toplanan bilgiler yalnızca siparişlerinizi yerine getirmek, size ürünlerimiz hakkında bilgi vermek ve daha iyi bir hizmet sunmak amacıyla kullanılır. Bilgileriniz kesinlikle üçüncü şahıslara satılmaz veya kiralanmaz.</p>

        <h2>Güvenlik</h2>
        <p>Tüm ödeme işlemleri 256-bit SSL sertifikası ile şifrelenir. Kredi kartı bilgileriniz sunucularımızda saklanmaz, doğrudan güvenli ödeme sağlayıcısı (Iyzico) üzerinden bankaya iletilir.</p>

        <h2>Çerezler (Cookies)</h2>
        <p>Web sitemiz, sepetinizi hatırlamak ve alışveriş deneyiminizi iyileştirmek için çerezleri kullanır. Tarayıcı ayarlarınızdan çerezleri dilediğiniz zaman kapatabilirsiniz.</p>

        <h2>İletişim</h2>
        <p>Gizlilik politikamız ile ilgili sorularınız için bizimle <a href="/Kurumsal/Iletisim">İletişim</a> sayfası üzerinden bağlantı kurabilirsiniz.</p>
    """

def get_iade_content():
    return """
        <h2>Genel İade Şartları</h2>
        <p>Müşteri memnuniyeti bizim için önceliktir. Satın aldığınız üründen memnun kalmamanız durumunda, ürünü teslim aldığınız tarihten itibaren 14 gün içinde hiçbir gerekçe göstermeksizin iade edebilirsiniz.</p>

        <h2>İade Süreci</h2>
        <ul>
            <li>İade etmek istediğiniz ürünün kullanılmamış ve orijinal ambalajının bozulmamış olması gerekmektedir.</li>
            <li>Hesabınız üzerinden <strong>Siparişlerim</strong> sayfasına giderek kolayca İade Talebi oluşturabilirsiniz.</li>
            <li>İade talebiniz onaylandıktan sonra size verilecek kargo kodu ile ürünü ücretsiz olarak geri gönderebilirsiniz.</li>
        </ul>

        <h2>Hasarlı Ürünler</h2>
        <p>Kargo teslimatı sırasında ürünün ambalajında gözle görülür bir hasar varsa, lütfen kargo görevlisine tutanak tutturunuz ve ürünü teslim almayınız. Kutuyu açtığınızda ürün hasarlı çıkarsa, aynı gün içinde fotoğraflarla birlikte bize ulaşmanızı rica ederiz.</p>

        <h2>Özel Tasarım Ürünler</h2>
        <p>Kişiye özel üretilen, farklı boyutlarda özel olarak basılan kanvas tabloların iadesi (üründe bir kusur veya basım hatası yoksa) kanunen yapılamamaktadır.</p>

        <h2>Para İadesi</h2>
        <p>İade ettiğiniz ürün depomuza ulaştıktan ve iade şartlarına uygunluğu onaylandıktan sonra, ödemeniz 3 iş günü içerisinde bankanıza iade edilir. Kredi kartı iadelerinin ekstrenize yansıması bankanıza bağlı olarak 2-7 gün sürebilir.</p>
    """

def get_hakkimizda_content():
    return """
        <div class="text-center mb-8">
            <p class="text-xl text-[#47473d] italic font-serif">"Yaşam alanları için özenle seçilmiş eserler, temiz operasyon ve güvenilir hizmet."</p>
        </div>

        <h2>Hikayemiz</h2>
        <p>Canvasia, duvarlarınıza sanatı ve estetiği getirmek amacıyla kurulmuş premium bir kanvas tablo galerisidir. Bizim için her tablo, bulunduğu mekânın ruhunu değiştiren bir dokunuştur.</p>

        <h2>Vizyonumuz</h2>
        <p>Sadece ürün satmak değil; yüksek kaliteli materyaller, özenli paketleme ve kesintisiz iletişim ile tamamen kusursuz bir alışveriş deneyimi sunmaktır.</p>

        <h2>Neden Biz?</h2>
        <ul>
            <li><strong>Premium Kalite:</strong> Yüksek çözünürlüklü baskı ve %100 pamuklu kanvas bezi.</li>
            <li><strong>Uzun Ömürlü:</strong> Solmaya karşı dayanıklı arşivsel mürekkepler.</li>
            <li><strong>Güvenli Kargo:</strong> Köşe koruyucular ve güçlendirilmiş ambalajlarla hasarsız teslimat garantisi.</li>
        </ul>

        <div class="mt-12 bg-[#fcf9f3] p-6 text-center border border-[#e5e2dc] rounded">
            <h3 class="mt-0 font-serif text-[#313511]">Bizimle İletişime Geçin</h3>
            <p class="text-sm">Özel projeleriniz, toptan alımlarınız veya merak ettikleriniz için bize ulaşabilirsiniz.</p>
            <a href="/Kurumsal/Iletisim" class="inline-block mt-4 bg-[#313511] text-white px-6 py-2 text-xs uppercase tracking-widest rounded hover:bg-[#1c2001] transition-colors no-underline">
                İletişim Sayfası
            </a>
        </div>
    """

def get_sss_content():
    return """
        <h2>Sipariş ve Kargo</h2>
        
        <h4>Siparişim ne zaman kargoya verilir?</h4>
        <p>Siparişleriniz, ürün detay sayfasında belirtilen kargoya veriliş süresi içinde hazırlanır. Standart ürünler genellikle 1-3 iş günü içerisinde kargolanmaktadır.</p>

        <h4>Kargo ücreti ne kadar?</h4>
        <p>Tüm Türkiye içi gönderimlerimiz şu an için <strong>ücretsizdir</strong>.</p>

        <h4>Siparişimi nasıl takip edebilirim?</h4>
        <p>Siparişiniz kargoya teslim edildiğinde size e-posta ve SMS ile bir kargo takip numarası iletilir. Ayrıca Hesabım > Siparişlerim sekmesinden de anlık durumunu görebilirsiniz.</p>

        <hr class="my-8 border-[#e5e2dc]">

        <h2>Ürünler ve Baskı Kalitesi</h2>

        <h4>Hangi malzemeleri kullanıyorsunuz?</h4>
        <p>Tablolarımızda %100 pamuklu 1. sınıf kanvas bezi ve fırınlanmış ahşap şase kullanılmaktadır. Zamanla eğilme veya yamulma yapmaz.</p>

        <h4>Baskılar zamanla solar mı?</h4>
        <p>Hayır, HP marka UV korumalı ve sağlığa zararsız orijinal mürekkepler kullanıyoruz. Tablolarınız yıllar boyu ilk günkü canlılığını korur.</p>
        
        <h4>Temizliği nasıl yapılmalı?</h4>
        <p>Tablolarınızı hafif nemli veya kuru mikrofiber bir bezle, bastırmadan silebilirsiniz. Kimyasal temizleyiciler kullanmaktan kaçının.</p>

        <hr class="my-8 border-[#e5e2dc]">

        <h2>İade ve Değişim</h2>

        <h4>Ürünümü iade edebilir miyim?</h4>
        <p>Evet, teslim aldığınız tarihten itibaren 14 gün içinde kolayca iade edebilirsiniz. Detaylar için İade Koşulları sayfamızı inceleyebilirsiniz.</p>
    """

base = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Kurumsal"
rewrite_kurumsal_view(os.path.join(base, "Gizlilik.cshtml"), get_gizlilik_content)
rewrite_kurumsal_view(os.path.join(base, "IadeKosullari.cshtml"), get_iade_content)
rewrite_kurumsal_view(os.path.join(base, "Hakkimizda.cshtml"), get_hakkimizda_content)
rewrite_kurumsal_view(os.path.join(base, "SSS.cshtml"), get_sss_content)

print("Kurumsal views updated.")

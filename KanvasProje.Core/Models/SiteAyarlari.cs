namespace KanvasProje.Core.Models
{
    public class SiteAyarlari
    {
        public int Id { get; set; } = 1;
        public string SiteAdi { get; set; } = "Canvasia";
        public string MarkaAdi { get; set; } = "Canvasia";
        public string SiteBasligi { get; set; } = "Canvasia - Online Dekorasyon Mağazası";
        public string SiteAciklamasi { get; set; } = "Duvar dekorasyonu ve yaşam alanları için premium ürünler.";
        public string SiteLogoUrl { get; set; } = "/logo_svg.svg";
        public string FaviconUrl { get; set; } = "/favicon.ico";
        public string BaseUrl { get; set; } = "https://www.canvasia.com.tr";
        public string TemaRengi { get; set; } = "#313511";
        public string UstBarMesaji { get; set; } = "500 TL üzeri ücretsiz kargo";
        public string KampanyaMesaji { get; set; } = "Vade farksız 3 taksit";
        public bool UstBarEtkin { get; set; } = true;
        public double UstBarHizi { get; set; } = 34;
        public string FooterAciklamasi { get; set; } = "Premium duvar dekorasyonu ve özel tasarım ürünleri.";

        public string Telefon { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Adres { get; set; } = string.Empty;
        public string WhatsappNumarasi { get; set; } = string.Empty;
        public string CalismaSaatleri { get; set; } = string.Empty;

        public string FacebookUrl { get; set; } = string.Empty;
        public string InstagramUrl { get; set; } = string.Empty;
        public string TwitterUrl { get; set; } = string.Empty;
        public string YoutubeUrl { get; set; } = string.Empty;
        public string TiktokUrl { get; set; } = string.Empty;
        public string PinterestUrl { get; set; } = string.Empty;

        public string ParaBirimi { get; set; } = "TL";
        public decimal KargoBedeli { get; set; } = 0;
        public decimal UcretsizKargoLimiti { get; set; } = 500;
        public int StokUyariLimiti { get; set; } = 5;
        public bool StoktaYokSatisIzni { get; set; } = false;

        public string KargoFirmasi { get; set; } = "Aras Kargo";
        public string KargoTakipUrl { get; set; } = string.Empty;
        public int SiparisTeslimSuresiGun { get; set; } = 5;
        public int IadeHakkiGun { get; set; } = 14;

        public string MetaTitle { get; set; } = "Canvasia - Premium Dekorasyon Ürünleri, Kanvas Tablo ve Duvar Sanatı";
        public string MetaDescription { get; set; } = "Canvasia; kanvas tablo, cam tablo, duvar dekorasyonu ve yaşam alanlarına özel premium dekorasyon ürünleri sunar.";
        public string MetaKeywords { get; set; } = "kanvas tablo, cam tablo, duvar dekorasyonu, duvar sanatı, tablo, dekorasyon ürünleri, Canvasia";
        public string GoogleAnalyticsId { get; set; } = string.Empty;
        public string FacebookPixelId { get; set; } = string.Empty;
        public string VarsayilanSosyalPaylasimGorseliUrl { get; set; } = "/EmailTemplates/canvasia-logo.png";
        public string CookieMetni { get; set; } = "Deneyiminizi iyileştirmek, sepetinizi korumak ve site trafiğini analiz etmek için çerezler kullanıyoruz.";

        public bool YeniSiparisMailBildirimi { get; set; } = true;
        public bool StokUyarisiMailBildirimi { get; set; } = true;
        public bool IadeTalebiMailBildirimi { get; set; } = true;
        public string BildirimAliciEmail { get; set; } = string.Empty;

        public bool BakimModuAktif { get; set; } = false;
        public string BakimModuMesaji { get; set; } = "Size daha iyi bir alışveriş deneyimi sunmak için kısa bir bakım çalışması yapıyoruz. Çok yakında premium dekorasyon ürünlerimizle yeniden yayında olacağız.";
    }
}
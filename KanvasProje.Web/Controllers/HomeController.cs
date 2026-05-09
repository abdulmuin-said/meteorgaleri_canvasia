using System.Collections.Generic;
using System.Diagnostics;
using KanvasProje.Core.Interfaces;
using KanvasProje.Core.Varliklar;
using KanvasProje.Data;
using KanvasProje.Core.Helpers;
using KanvasProje.Web.Models;
using KanvasProje.Service.Services;
using KanvasProje.Web.ViewComponents;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Net;
using System.Net.Mail;

namespace KanvasProje.Web.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly KanvasDbContext _context;
        private readonly IEmailService _emailService;
        private readonly ISiteSettingsService _siteSettingsService;
        private readonly IHomePageSettingsService _homePageSettingsService;

        public HomeController(
            ILogger<HomeController> logger,
            KanvasDbContext context,
            IEmailService emailService,
            ISiteSettingsService siteSettingsService,
            IHomePageSettingsService homePageSettingsService)
        {
            _logger = logger;
            _context = context;
            _emailService = emailService;
            _siteSettingsService = siteSettingsService;
            _homePageSettingsService = homePageSettingsService;
        }

        public async Task<IActionResult> Index()
        {
            var aktifUrunler = _context.Urunler
                .AsNoTracking()
                .Include(u => u.Kategori)
                .Include(u => u.UrunSecenek)
                .Include(u => u.UrunResimleri)
                .Where(u =>
                    u.AktifMi &&
                    !u.SilindiMi &&
                    u.Kategori != null &&
                    u.Kategori.AktifMi);

            var secilenUrunler = new HashSet<int>();

            var vitrinUrunleri = await aktifUrunler
                .Where(u => u.AnaSayfadaGoster || u.OneCikanMi || u.YeniUrunMu)
                .OrderBy(u => u.Sira)
                .ThenByDescending(u => u.OneCikanMi)
                .ThenByDescending(u => u.OlusturulmaTarihi)
                .Take(8)
                .ToListAsync();

            secilenUrunler.UnionWith(vitrinUrunleri.Select(x => x.Id));
            await TamamlayiciUrunleriEkleAsync(
                vitrinUrunleri,
                aktifUrunler.OrderBy(u => u.Sira).ThenByDescending(u => u.OlusturulmaTarihi),
                secilenUrunler,
                8);

            var cokSatanlar = await aktifUrunler
                .Where(u => (u.SatisSayisi > 0 || u.OneCikanMi) && !secilenUrunler.Contains(u.Id))
                .OrderByDescending(u => u.SatisSayisi)
                .ThenByDescending(u => u.GoruntulenmeSayisi)
                .ThenBy(u => u.Sira)
                .Take(8)
                .ToListAsync();

            secilenUrunler.UnionWith(cokSatanlar.Select(x => x.Id));
            await TamamlayiciUrunleriEkleAsync(
                cokSatanlar,
                aktifUrunler.OrderByDescending(u => u.SatisSayisi).ThenBy(u => u.Sira),
                secilenUrunler,
                8);

            var firsatUrunleri = await aktifUrunler
                .Where(u =>
                    (u.KampanyaliMi || (u.IndirimliFiyat.HasValue && u.IndirimliFiyat > 0 && u.IndirimliFiyat < u.Fiyat)) &&
                    !secilenUrunler.Contains(u.Id))
                .OrderByDescending(u => u.KampanyaliMi)
                .ThenBy(u => u.IndirimliFiyat ?? u.Fiyat)
                .ThenBy(u => u.Sira)
                .Take(8)
                .ToListAsync();

            secilenUrunler.UnionWith(firsatUrunleri.Select(x => x.Id));
            await TamamlayiciUrunleriEkleAsync(
                firsatUrunleri,
                aktifUrunler.OrderBy(u => u.IndirimliFiyat ?? u.Fiyat).ThenBy(u => u.Sira),
                secilenUrunler,
                8);

            var kategoriler = await _context.Kategoriler
                .AsNoTracking()
                .Where(k => k.AktifMi && !k.SilindiMi && k.ParentKategoriId == null)
                .OrderBy(k => k.Sira)
                .ThenBy(k => k.Ad)
                .Take(12)
                .ToListAsync();

            var viewModel = new HomeViewModel
            {
                VitrinUrunleri = vitrinUrunleri,
                CokSatanlar = cokSatanlar,
                FirsatUrunleri = firsatUrunleri,
                Kategoriler = kategoriler,
                HomePageSettings = _homePageSettingsService.GetSettings()
            };

            return View(viewModel);
        }

        private static async Task TamamlayiciUrunleriEkleAsync(
            List<Urun> hedefListe,
            IOrderedQueryable<Urun> kaynakSorgu,
            HashSet<int> secilenUrunler,
            int hedefAdet)
        {
            if (hedefListe.Count >= hedefAdet)
            {
                return;
            }

            var eksikAdet = hedefAdet - hedefListe.Count;
            var ekUrunler = await kaynakSorgu
                .Where(x => !secilenUrunler.Contains(x.Id))
                .Take(eksikAdet)
                .ToListAsync();

            hedefListe.AddRange(ekUrunler);
            secilenUrunler.UnionWith(ekUrunler.Select(x => x.Id));
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> BulteneAboneOl(string email)
        {
            email = (email ?? string.Empty).Trim().ToLowerInvariant();

            if (!GecerliEmailMi(email))
            {
                return Json(new { success = false, message = "Lütfen geçerli bir e-posta adresi girin." });
            }

            try
            {
                var mevcutAbone = await _context.BultenAbonelikleri.FirstOrDefaultAsync(x => x.Email == email);
            if (mevcutAbone?.AktifMi == true)
            {
                return Json(new { success = false, message = "Bu e-posta adresi zaten bültene kayıtlı." });
            }

            if (mevcutAbone != null)
            {
                mevcutAbone.AktifMi = true;
                mevcutAbone.KayitTarihi = DateTime.UtcNow.AddHours(3);
                mevcutAbone.IpAdresi = Request.HttpContext.Connection.RemoteIpAddress?.ToString();
            }
            else
            {
                var yeniAbone = new BultenAboneligi
                {
                    Email = email,
                    KayitTarihi = DateTime.UtcNow.AddHours(3),
                    AktifMi = true,
                    IpAdresi = Request.HttpContext.Connection.RemoteIpAddress?.ToString()
                };

                _context.BultenAbonelikleri.Add(yeniAbone);
            }
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Bulten aboneligi kaydedilemedi. Email: {Email}", email);
                return Json(new { success = false, message = "Bulten aboneligi su anda kaydedilemedi. Lutfen kisa bir sure sonra tekrar deneyin." });
            }

            var settings = _siteSettingsService.GetSettings();
            var brandName = string.IsNullOrWhiteSpace(settings.MarkaAdi) ? settings.SiteAdi : settings.MarkaAdi;
            var siteUrl = _siteSettingsService.BuildAbsoluteUrl(string.Empty);

            try
            {
                await _emailService.SendTemplateMailAsync(
                    email,
                    "B\u00FClten Kayd\u0131n\u0131z Al\u0131nd\u0131",
                    "De\u011Ferli M\u00FC\u015Fterimiz",
                    $"{brandName} b&uuml;ltenine ho&#351; geldiniz. Yeni koleksiyonlar, kampanyalar ve duyurular size ilk olarak ula&#351;acak.",
                    siteUrl,
                    "Siteyi \u0130ncele");
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Bulten hos geldiniz e-postasi gonderilemedi. Email: {Email}", email);
            }

            try
            {
                const string recipientEmail = "canvasia.com.tr@gmail.com";
                var ipAddress = Request.HttpContext.Connection.RemoteIpAddress?.ToString() ?? "-";
                var adminMailIcerik = $@"
                    <p>Bir kisi bultene kayit oldu.</p>
                    <p><b>Abone e-posta:</b> {WebUtility.HtmlEncode(email)}</p>
                    <p><b>IP:</b> {WebUtility.HtmlEncode(ipAddress)}</p>";

                await _emailService.SendTemplateMailAsync(
                    recipientEmail,
                    "Yeni Bulten Aboneligi",
                    "Operasyon Ekibi",
                    adminMailIcerik,
                    siteUrl,
                    "Siteyi Incele");
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Bulten admin bildirimi gonderilemedi. Email: {Email}", email);
            }

            return Json(new { success = true, message = "Aboneliğiniz başarıyla oluşturuldu." });
        }

        private static bool GecerliEmailMi(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
            {
                return false;
            }

            try
            {
                var adres = new MailAddress(email);
                return string.Equals(adres.Address, email, StringComparison.OrdinalIgnoreCase);
            }
            catch
            {
                return false;
            }
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}

using Microsoft.AspNetCore.Mvc;
using KanvasProje.Core.Interfaces; // ISepetService
using KanvasProje.Data;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;
using KanvasProje.Core.Varliklar;

namespace KanvasProje.Web.Controllers
{
    public class SepetController : Controller
    {
        private readonly KanvasDbContext _context;
        private readonly ISepetService _sepetService;
        private readonly UserManager<AppUser> _userManager;

        public SepetController(
            KanvasDbContext context,
            ISepetService sepetService,
            UserManager<AppUser> userManager)
        {
            _context = context;
            _sepetService = sepetService;
            _userManager = userManager;
        }

        public async Task<IActionResult> Index()
        {
            // User ID ve Session ID al
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            var sessionId = HttpContext.Session.Id;

            // Database'den sepeti çek
            var sepetItems = await _sepetService.GetSepetItemsAsync(userId, sessionId);
            decimal sepetToplami = await _sepetService.GetSepetToplamiAsync(userId, sessionId);

            // --- KUPON HESAPLAMA ---
            string? kuponKodu = HttpContext.Session.GetString("UygulananKupon");
            decimal indirimTutari = 0;

            if (!string.IsNullOrEmpty(kuponKodu))
            {
                var kupon = await _context.Kuponlar.FirstOrDefaultAsync(x => x.Kod == kuponKodu && !x.SilindiMi);
                if (kupon != null && IsCouponAvailable(kupon, sepetToplami))
                {
                    if (kupon.Tip == 0) // Yüzde
                    {
                        indirimTutari = CalculateCouponDiscount(kupon, sepetToplami);
                    }
                    else // Tutar
                    {
                        indirimTutari = CalculateCouponDiscount(kupon, sepetToplami);
                    }
                }
                else
                {
                    // Şartlar sağlanmıyorsa kuponu düşür
                    HttpContext.Session.Remove("UygulananKupon");
                    kuponKodu = null;
                }
            }

            ViewBag.KuponKodu = kuponKodu;
            ViewBag.IndirimTutari = indirimTutari;
            // -----------------------

            return View(sepetItems);
        }






        // SepetController içine ekle:

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> KuponUygula(string kuponKodu)
        {
            if (string.IsNullOrEmpty(kuponKodu))
            {
                TempData["SepetHata"] = "Lütfen bir kupon kodu giriniz.";
                return RedirectToAction("Index");
            }

            kuponKodu = NormalizeCouponCode(kuponKodu);

            var kupon = await _context.Kuponlar.FirstOrDefaultAsync(x => x.Kod == kuponKodu && !x.SilindiMi);
            
            // --- KONTROLLER ---
            if (kupon == null)
            {
                TempData["SepetHata"] = "Geçersiz veya süresi dolmuş kupon kodu.";
                return RedirectToAction("Index");
            }

            if (!kupon.AktifMi)
            {
                TempData["SepetHata"] = "Bu kupon şu anda aktif değil.";
                return RedirectToAction("Index");
            }

            if (kupon.SonKullanmaTarihi < DateTime.UtcNow)
            {
                TempData["SepetHata"] = "Bu kuponun süresi dolmuş.";
                return RedirectToAction("Index");
            }

            if (kupon.KullanimLimiti > 0 && kupon.KullanilanMiktar >= kupon.KullanimLimiti)
            {
                TempData["SepetHata"] = "Bu kuponun kullanım limiti dolmuş.";
                return RedirectToAction("Index");
            }

            // Sepet tutarını database'den kontrol et
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            var sessionId = HttpContext.Session.Id;
            decimal sepetTutari = await _sepetService.GetSepetToplamiAsync(userId, sessionId);

            if (sepetTutari < kupon.MinSepetTutari)
            {
                TempData["SepetHata"] = $"Bu kuponu kullanmak için sepet tutarı en az {kupon.MinSepetTutari:C} olmalıdır.";
                return RedirectToAction("Index");
            }

            // --- BAŞARILI ---
            HttpContext.Session.SetString("UygulananKupon", kupon.Kod);
            TempData["SepetBasari"] = "Kupon başarıyla uygulandı.";
            
            return RedirectToAction("Index");
        }

        private static bool IsCouponAvailable(Kupon kupon, decimal sepetTutari)
        {
            return kupon.AktifMi
                && kupon.SonKullanmaTarihi > DateTime.UtcNow
                && (kupon.KullanimLimiti <= 0 || kupon.KullanilanMiktar < kupon.KullanimLimiti)
                && sepetTutari >= kupon.MinSepetTutari;
        }

        private static decimal CalculateCouponDiscount(Kupon kupon, decimal sepetTutari)
        {
            var discount = kupon.Tip == 0
                ? sepetTutari * (kupon.Deger / 100)
                : kupon.Deger;

            return Math.Round(Math.Min(sepetTutari, Math.Max(0, discount)), 2);
        }

        private static string NormalizeCouponCode(string? code)
        {
            return (code ?? string.Empty)
                .Trim()
                .ToUpperInvariant()
                .Replace(" ", string.Empty);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult KuponKaldir()
        {
            HttpContext.Session.Remove("UygulananKupon");
            return RedirectToAction("Index");
        }


        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Ekle(int UrunId, int? SecenekId, int Adet = 1, string? CerceveModeli = null, string? MusteriNotu = null, decimal? CerceveFarki = null)
        {
            if (Adet < 1) Adet = 1;
            if (Adet > 100) Adet = 100;

            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;

            if (string.IsNullOrEmpty(HttpContext.Session.GetString("SessionId")))
            {
                HttpContext.Session.SetString("SessionId", HttpContext.Session.Id);
            }
            var sessionId = HttpContext.Session.Id;

            var success = await _sepetService.SepeteEkleAsync(userId, sessionId, UrunId, SecenekId, Adet, CerceveModeli, MusteriNotu, CerceveFarki);

            if (success)
            {
                return Json(new { success = true, message = "Ürün sepete eklendi", redirectUrl = Url.Action("Index", "Sepet") });
            }
            else
            {
                return Json(new { success = false, message = "Ürün sepete eklenemedi" });
            }
        }

        // Adet güncelleme - database'de SepetItem ID ile çalışıyor
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> AdetGuncelle(int sepetItemId, int yeniAdet)
        {
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            var sessionId = HttpContext.Session.Id;
            var sepetItems = await _sepetService.GetSepetItemsAsync(userId, sessionId);
            if (!sepetItems.Any(x => x.Id == sepetItemId))
                return RedirectToAction("Index");

            if (yeniAdet < 1) yeniAdet = 1;
            if (yeniAdet > 100) yeniAdet = 100;
            var success = await _sepetService.AdediGuncelleAsync(sepetItemId, yeniAdet);
            return RedirectToAction("Index");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> NotGuncelle(int sepetItemId, string? musteriNotu)
        {
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            var sessionId = HttpContext.Session.Id;
            var sepetItems = await _sepetService.GetSepetItemsAsync(userId, sessionId);
            if (!sepetItems.Any(x => x.Id == sepetItemId))
                return RedirectToAction("Index");

            var trimmed = musteriNotu?.Trim();
            if (!string.IsNullOrWhiteSpace(trimmed) && trimmed.Length > 500)
                trimmed = trimmed[..500];

            await _sepetService.NotGuncelleAsync(sepetItemId, trimmed);
            return RedirectToAction("Index");
        }




        // Sepetten item sil
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Sil(int sepetItemId)
        {
            // IDOR Koruması: Sadece kendi sepet öğesini silebilsin
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            var sessionId = HttpContext.Session.Id;
            var sepetItems = await _sepetService.GetSepetItemsAsync(userId, sessionId);
            if (!sepetItems.Any(x => x.Id == sepetItemId))
                return RedirectToAction("Index");

            await _sepetService.SepettenCikarAsync(sepetItemId);
            return RedirectToAction("Index");
        }
        // Sepeti temizle
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Temizle()
        {
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            var sessionId = HttpContext.Session.Id;
            
            await _sepetService.SepetTemizleAsync(userId, sessionId);
            return RedirectToAction("Index");
        }
    }
}

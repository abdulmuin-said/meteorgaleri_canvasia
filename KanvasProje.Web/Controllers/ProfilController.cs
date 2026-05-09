using KanvasProje.Core.Varliklar;
using KanvasProje.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace KanvasProje.Web.Controllers
{
    [Authorize]
    public class ProfilController : Controller
    {
        private readonly UserManager<AppUser> _userManager;
        private readonly SignInManager<AppUser> _signInManager;
        private readonly KanvasDbContext _context;

        public ProfilController(
            UserManager<AppUser> userManager,
            SignInManager<AppUser> signInManager,
            KanvasDbContext context)
        {
            _userManager = userManager;
            _signInManager = signInManager;
            _context = context;
        }

        public async Task<IActionResult> Index()
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var siparislerim = await GetOwnedOrdersQuery(user)
                .OrderByDescending(x => x.OlusturulmaTarihi)
                .ToListAsync();

            ViewBag.SiparisSayisi = siparislerim.Count;
            ViewBag.ToplamHarcama = siparislerim.Sum(x => x.ToplamTutar);
            return View(user);
        }

        public async Task<IActionResult> Siparislerim()
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var siparislerim = await GetOwnedOrdersQuery(user)
                .OrderByDescending(x => x.OlusturulmaTarihi)
                .ToListAsync();

            return View(siparislerim);
        }

        public async Task<IActionResult> SiparisDetay(int id)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var siparis = await GetOwnedOrdersQuery(user)
                .FirstOrDefaultAsync(x => x.Id == id);

            if (siparis == null)
            {
                return RedirectToAction("ErisimEngellendi", "Hesap");
            }

            var iade = await _context.IadeTalepleri
                .AsNoTracking()
                .FirstOrDefaultAsync(x => x.SiparisId == id && !x.SilindiMi);

            if (iade != null)
            {
                ViewBag.IadeDurumu = iade.Durum switch
                {
                    0 => "Inceleniyor",
                    1 => "Onaylandi (Kargo Bekleniyor)",
                    2 => "Iade Tamamlandi",
                    _ => "Reddedildi"
                };
            }

            var siparisKalemleri = await _context.SiparisDetaylari
                .AsNoTracking()
                .Include(x => x.Urun)
                .Include(x => x.UrunSecenek)
                .Where(x => x.SiparisId == id && !x.SilindiMi)
                .ToListAsync();

            ViewBag.Urunler = siparisKalemleri
                .Where(x => x.Urun != null)
                .Select(x => new
                {
                    Resim = !string.IsNullOrWhiteSpace(x.UrunSecenek?.GorselUrl) ? x.UrunSecenek.GorselUrl : x.Urun!.AnaGorselUrl,
                    Baslik = x.Urun.Baslik,
                    Olcu = x.UrunSecenek?.Olcu ?? string.Empty,
                    Cerceve = x.UrunSecenek?.CerceveTipi ?? string.Empty,
                    Secenek = x.UrunSecenek == null
                        ? "Standart urun"
                        : (string.IsNullOrWhiteSpace(x.UrunSecenek.VaryantBasligi) ? "Varsayilan varyasyon" : x.UrunSecenek.VaryantBasligi),
                    SecenekDetay = x.UrunSecenek?.VaryantOzeti ?? string.Empty,
                    CerceveModeli = x.CerceveModeli,
                    Adet = x.Adet,
                    Fiyat = x.BirimFiyat,
                    Toplam = x.Adet * x.BirimFiyat,
                    UrunId = x.Urun!.Id,
                    MusteriNotu = x.MusteriNotu
                })
                .ToList();

            return View(siparis);
        }

        [HttpGet]
        public async Task<IActionResult> IadeOlustur(int siparisId)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var siparis = await GetOwnedOrdersQuery(user)
                .FirstOrDefaultAsync(x => x.Id == siparisId);

            if (siparis == null)
            {
                return NotFound();
            }

            if (siparis.Durum != 3)
            {
                TempData["Hata"] = "Sadece teslim edilmis siparisler icin iade talebi olusturabilirsiniz.";
                return RedirectToAction(nameof(SiparisDetay), new { id = siparisId });
            }

            var mevcutTalep = await _context.IadeTalepleri
                .AsNoTracking()
                .FirstOrDefaultAsync(x => x.SiparisId == siparisId && !x.SilindiMi);

            if (mevcutTalep != null)
            {
                TempData["Bilgi"] = "Bu siparis icin zaten bir iade talebiniz bulunmaktadir.";
                return RedirectToAction(nameof(SiparisDetay), new { id = siparisId });
            }

            return View(new IadeTalebi { SiparisId = siparisId });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> IadeOlustur([Bind("SiparisId,Neden,Aciklama,IBAN")] IadeTalebi talep)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var siparis = await GetOwnedOrdersQuery(user)
                .FirstOrDefaultAsync(x => x.Id == talep.SiparisId);

            if (siparis == null)
            {
                return RedirectToAction("ErisimEngellendi", "Hesap");
            }

            if (siparis.Durum != 3)
            {
                TempData["Hata"] = "Iade talebi sadece teslim edilen siparisler icin olusturulabilir.";
                return RedirectToAction(nameof(SiparisDetay), new { id = talep.SiparisId });
            }

            var mevcutTalep = await _context.IadeTalepleri
                .FirstOrDefaultAsync(x => x.SiparisId == talep.SiparisId && !x.SilindiMi);

            if (mevcutTalep != null)
            {
                TempData["Bilgi"] = "Bu siparis icin zaten bir iade talebi bulunuyor.";
                return RedirectToAction(nameof(SiparisDetay), new { id = talep.SiparisId });
            }

            talep.MusteriId = user.Id;
            talep.OlusturulmaTarihi = DateTime.UtcNow;
            talep.Durum = 0;
            talep.SilindiMi = false;

            _context.IadeTalepleri.Add(talep);
            siparis.Durum = 5;

            await _context.SaveChangesAsync();

            TempData["Basari"] = "Iade talebiniz alindi. Siparis durumu guncellendi.";
            return RedirectToAction(nameof(SiparisDetay), new { id = talep.SiparisId });
        }

        public async Task<IActionResult> Adreslerim()
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var adreslerim = await _context.Adresler
                .AsNoTracking()
                .Where(x => x.AppUserId == user.Id && !x.SilindiMi)
                .OrderByDescending(x => x.OlusturulmaTarihi)
                .ToListAsync();

            return View(adreslerim);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> AdresEkle(Adres adres)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            adres.AppUserId = user.Id;
            adres.Baslik = adres.Baslik?.Trim() ?? string.Empty;
            adres.AdSoyad = adres.AdSoyad?.Trim() ?? string.Empty;
            adres.Telefon = adres.Telefon?.Trim() ?? string.Empty;
            adres.Sehir = adres.Sehir?.Trim() ?? string.Empty;
            adres.Ilce = adres.Ilce?.Trim() ?? string.Empty;
            adres.AcikAdres = adres.AcikAdres?.Trim() ?? string.Empty;
            adres.OlusturulmaTarihi = DateTime.UtcNow;
            adres.SilindiMi = false;

            _context.Adresler.Add(adres);
            await _context.SaveChangesAsync();

            TempData["Mesaj"] = "Adres basariyla eklendi.";
            return RedirectToAction(nameof(Adreslerim));
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> AdresSil(int id)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var adres = await _context.Adresler
                .FirstOrDefaultAsync(x => x.Id == id && x.AppUserId == user.Id && !x.SilindiMi);

            if (adres != null)
            {
                adres.SilindiMi = true;
                await _context.SaveChangesAsync();
                TempData["Mesaj"] = "Adres basariyla silindi.";
            }

            return RedirectToAction(nameof(Adreslerim));
        }

        [HttpGet]
        public IActionResult HesabiSil()
        {
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> HesabiSilOnayla(string sifre)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var passwordCheck = await _userManager.CheckPasswordAsync(user, sifre);
            if (!passwordCheck)
            {
                ViewBag.Hata = "Girdiginiz sifre yanlis. Lutfen tekrar deneyin.";
                return View("HesabiSil");
            }

            var result = await _userManager.DeleteAsync(user);
            if (result.Succeeded)
            {
                await _signInManager.SignOutAsync();
                TempData["Bilgi"] = "Hesabiniz basariyla silindi. Bizi tercih ettiginiz icin tesekkur ederiz.";
                return RedirectToAction("Index", "Home");
            }

            ViewBag.Hata = "Hesap silinirken bir hata olustu. Lutfen tekrar deneyin.";
            return View("HesabiSil");
        }

        private IQueryable<Siparis> GetOwnedOrdersQuery(AppUser user)
        {
            var normalizedEmail = user.Email ?? string.Empty;
            return _context.Siparisler.Where(x =>
                !x.SilindiMi &&
                (x.AppUserId == user.Id ||
                 (string.IsNullOrEmpty(x.AppUserId) && x.Eposta == normalizedEmail)));
        }
    }
}

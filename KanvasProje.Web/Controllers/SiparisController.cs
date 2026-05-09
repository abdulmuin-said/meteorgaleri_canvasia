using KanvasProje.Core.Interfaces;
using KanvasProje.Core.Varliklar;
using KanvasProje.Data;
using KanvasProje.Service.Interfaces;
using KanvasProje.Service.Services;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace KanvasProje.Web.Controllers
{
    public class SiparisController : Controller
    {
        private const string PendingPaymentOrderSessionKey = "PendingPaymentOrderId";

        private readonly UserManager<AppUser> _userManager;
        private readonly IService<Adres> _adresService;
        private readonly KanvasDbContext _context;
        private readonly IEmailService _emailService;
        private readonly IPaymentService _paymentService;
        private readonly ISepetService _sepetService;
        private readonly ISiteSettingsService _siteSettingsService;
        private readonly ILogger<SiparisController> _logger;

        public SiparisController(
            UserManager<AppUser> userManager,
            IService<Adres> adresService,
            KanvasDbContext context,
            IEmailService emailService,
            IPaymentService paymentService,
            ISepetService sepetService,
            ISiteSettingsService siteSettingsService,
            ILogger<SiparisController> logger)
        {
            _userManager = userManager;
            _adresService = adresService;
            _context = context;
            _emailService = emailService;
            _paymentService = paymentService;
            _sepetService = sepetService;
            _siteSettingsService = siteSettingsService;
            _logger = logger;
        }

        [HttpGet]
        public async Task<IActionResult> Odeme()
        {
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            var sessionId = HttpContext.Session.Id;

            var sepetItems = await _sepetService.GetSepetItemsAsync(userId, sessionId);
            if (sepetItems == null || !sepetItems.Any())
            {
                return RedirectToAction("Index", "Sepet");
            }

            await PrepareCheckoutViewDataAsync(userId, sessionId, sepetItems);

            var model = new Siparis();

            if (User.Identity?.IsAuthenticated == true)
            {
                var user = await _userManager.GetUserAsync(User);
                if (user != null)
                {
                    var tumAdresler = await _adresService.GetAllAsync();
                    ViewBag.KayitliAdresler = tumAdresler.Where(x => x.AppUserId == user.Id).ToList();

                    model.MusteriAdSoyad = user.AdSoyad;
                    model.Eposta = user.Email ?? string.Empty;
                    model.Telefon = user.PhoneNumber ?? string.Empty;
                    model.Sehir = user.Sehir;
                }
            }

            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Odeme(Siparis siparis, string? yeniAdresBasligi, bool adresiKaydet)
        {
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            var sessionId = HttpContext.Session.Id;

            var sepetItems = await _sepetService.GetSepetItemsAsync(userId, sessionId);
            if (sepetItems == null || !sepetItems.Any())
            {
                return RedirectToAction("Index", "Sepet");
            }

            NormalizeCheckoutInput(siparis);

            if (!ValidateCheckoutInput(siparis))
            {
                await PrepareCheckoutViewDataAsync(userId, sessionId, sepetItems);
                ViewBag.FormHata = "Lutfen teslimat bilgilerini eksiksiz ve gecerli formatta doldurun.";
                return View(siparis);
            }

            decimal hamTutar = await _sepetService.GetSepetToplamiAsync(userId, sessionId);

            siparis.SiparisNo = await GenerateUniqueOrderNumberAsync();
            siparis.EmailHashKodu = Guid.NewGuid().ToString("N")[..16];
            siparis.OlusturulmaTarihi = DateTime.UtcNow;
            siparis.Durum = 0;
            siparis.SilindiMi = false;
            siparis.AppUserId = userId;
            siparis.KargoTakipNo ??= string.Empty;
            siparis.ToplamTutar = hamTutar;
            siparis.IndirimTutari = 0;
            siparis.KuponKodu = null;

            string? kuponKodu = HttpContext.Session.GetString("UygulananKupon");
            if (!string.IsNullOrEmpty(kuponKodu))
            {
                var kupon = await _context.Kuponlar.FirstOrDefaultAsync(x => x.Kod == kuponKodu && !x.SilindiMi);
                if (kupon != null &&
                    kupon.AktifMi &&
                    kupon.SonKullanmaTarihi > DateTime.UtcNow &&
                    (kupon.KullanimLimiti <= 0 || kupon.KullanilanMiktar < kupon.KullanimLimiti) &&
                    hamTutar >= kupon.MinSepetTutari)
                {
                    var indirim = CalculateCouponDiscount(kupon, hamTutar);
                    siparis.IndirimTutari = indirim;
                    siparis.KuponKodu = kupon.Kod;
                    siparis.ToplamTutar = Math.Max(0, siparis.ToplamTutar - indirim);
                }
            }

            await using var transaction = await _context.Database.BeginTransactionAsync();

            try
            {
                if (adresiKaydet && !string.IsNullOrEmpty(userId))
                {
                    _context.Adresler.Add(new Adres
                    {
                        AppUserId = userId,
                        Baslik = string.IsNullOrWhiteSpace(yeniAdresBasligi) ? "Yeni Adresim" : yeniAdresBasligi.Trim(),
                        AdSoyad = siparis.MusteriAdSoyad,
                        Telefon = siparis.Telefon,
                        Sehir = siparis.Sehir,
                        Ilce = siparis.Ilce,
                        AcikAdres = siparis.AcikAdres,
                        OlusturulmaTarihi = DateTime.UtcNow,
                        SilindiMi = false
                    });
                }

                _context.Siparisler.Add(siparis);
                await _context.SaveChangesAsync();

                foreach (var item in sepetItems)
                {
                    var gercekSecenekId = await ResolveOrderVariantIdAsync(item);

                    _context.SiparisDetaylari.Add(new SiparisDetay
                    {
                        SiparisId = siparis.Id,
                        UrunSecenekId = gercekSecenekId,
                        Adet = item.Adet,
                        BirimFiyat = item.Fiyat,
                        OlusturulmaTarihi = DateTime.UtcNow,
                        UrunId = item.UrunId,
                        CerceveModeli = item.CerceveModeli,
                        MusteriNotu = item.MusteriNotu,
                        SilindiMi = false
                    });
                }

                await _context.SaveChangesAsync();
                await transaction.CommitAsync();
            }
            catch
            {
                await transaction.RollbackAsync();
                throw;
            }

            HttpContext.Session.SetInt32(PendingPaymentOrderSessionKey, siparis.Id);

            return RedirectToAction(nameof(IyzicoOdemeBaslat), new { id = siparis.Id });
        }

        [HttpGet]
        public async Task<IActionResult> IyzicoOdemeBaslat(int id)
        {
            var siparis = await _context.Siparisler.FindAsync(id);
            if (siparis == null)
            {
                return NotFound();
            }

            if (!CanAccessPaymentOrder(siparis))
            {
                return Forbid();
            }

            if (siparis.Durum != 0)
            {
                return siparis.Durum >= 1
                    ? RedirectToAction(nameof(Basarili), new { siparisNo = siparis.SiparisNo })
                    : RedirectToAction(nameof(Basarisiz));
            }

            var userIp = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "127.0.0.1";
            if (userIp == "::1")
            {
                userIp = "127.0.0.1";
            }

            var adSoyad = string.IsNullOrWhiteSpace(siparis.MusteriAdSoyad) ? "Misafir Soyad" : siparis.MusteriAdSoyad.Trim();
            var nameParts = adSoyad.Split(' ', 2, StringSplitOptions.RemoveEmptyEntries);
            var firstName = nameParts.Length > 0 ? nameParts[0] : "Misafir";
            var lastName = nameParts.Length > 1 ? nameParts[1] : "Soyad";

            var request = new PaymentInitRequest
            {
                OrderId = siparis.SiparisNo,
                TotalPrice = siparis.ToplamTutar,
                PaidPrice = siparis.ToplamTutar,
                CallbackUrl = $"{Request.Scheme}://{Request.Host}/Siparis/IyzicoCallback",
                BuyerId = siparis.AppUserId ?? "GuestUser",
                BuyerName = firstName,
                BuyerSurname = lastName,
                BuyerEmail = siparis.Eposta,
                BuyerPhone = siparis.Telefon,
                BuyerAddress = $"{siparis.AcikAdres} {siparis.Ilce}/{siparis.Sehir}",
                BuyerIp = userIp,
                BuyerCity = siparis.Sehir
            };

            var detaylar = await _context.SiparisDetaylari
                .Include(x => x.Urun)
                    .ThenInclude(x => x.Kategori)
                .Include(x => x.UrunSecenek)
                .Where(x => x.SiparisId == id)
                .ToListAsync();

            foreach (var item in detaylar)
            {
                var detayMetni = BuildOrderLineDetail(item);
                var itemName = item.Urun?.Baslik ?? "Urun";
                if (!string.IsNullOrWhiteSpace(detayMetni))
                {
                    itemName = $"{itemName} - {detayMetni}";
                }

                request.BasketItems.Add(new PaymentBasketItem
                {
                    Id = item.UrunId.ToString(),
                    Name = itemName,
                    Category = item.Urun?.Kategori?.Ad ?? "Genel",
                    Price = item.BirimFiyat * item.Adet
                });
            }

            var result = await _paymentService.InitializeCheckoutAsync(request);

            if (result.Success)
            {
                HttpContext.Session.SetInt32(PendingPaymentOrderSessionKey, siparis.Id);
                ViewBag.IyzicoContent = result.CheckoutFormContent;
                return View("IyzicoOdemeSayfasi");
            }

            _logger.LogWarning(
                "Odeme baslatilamadi. SiparisNo={SiparisNo}, Hata={Error}",
                siparis.SiparisNo,
                result.ErrorMessage);

            ViewBag.Hata = result.ErrorMessage;
            return View("Basarisiz");
        }

        [HttpPost]
        [IgnoreAntiforgeryToken]
        public async Task<IActionResult> IyzicoCallback([FromForm] string token)
        {
            if (string.IsNullOrWhiteSpace(token))
            {
                ViewBag.Hata = "Odeme dogrulama token bilgisi eksik.";
                return View("Basarisiz");
            }

            var result = await _paymentService.VerifyPaymentAsync(token);
            if (!result.Success)
            {
                _logger.LogWarning("Odeme dogrulama basarisiz. Token={Token}, Hata={Error}", token, result.ErrorMessage);
                ViewBag.Hata = result.ErrorMessage ?? "Odeme islemi basarisiz veya iptal edildi.";
                return View("Basarisiz");
            }

            if (string.IsNullOrWhiteSpace(result.ConversationId))
            {
                _logger.LogError("Odeme basarili fakat ConversationId bos dondu. PaymentId={PaymentId}", result.PaymentId);
                ViewBag.Hata = "Odeme dogrulandi ancak siparis eslestirilemedi.";
                return View("Basarisiz");
            }

            var siparis = await _context.Siparisler
                .FirstOrDefaultAsync(x => x.SiparisNo == result.ConversationId && !x.SilindiMi);

            if (siparis == null)
            {
                _logger.LogError(
                    "Odeme basarili fakat eslesen siparis bulunamadi. ConversationId={ConversationId}, PaymentId={PaymentId}",
                    result.ConversationId,
                    result.PaymentId);

                ViewBag.Hata = "Odeme onaylandi ancak siparis bulunamadi.";
                return View("Basarisiz");
            }

            if (siparis.Durum >= 1)
            {
                return RedirectToAction(nameof(Basarili), new { siparisNo = siparis.SiparisNo });
            }

            if (result.PaidPrice <= 0 || Math.Abs(result.PaidPrice - siparis.ToplamTutar) > 0.01m)
            {
                _logger.LogError(
                    "Odeme tutari uyusmazligi. SiparisNo={SiparisNo}, Beklenen={Beklenen}, Gelen={Gelen}, PaymentId={PaymentId}",
                    siparis.SiparisNo,
                    siparis.ToplamTutar,
                    result.PaidPrice,
                    result.PaymentId);

                ViewBag.Hata = "Odeme tutari dogrulanamadi. Lutfen destek ile iletisime gecin.";
                return View("Basarisiz");
            }

            await using var transaction = await _context.Database.BeginTransactionAsync();

            siparis.Durum = 1;
            siparis.Aciklama = $"Odeme basarili - PaymentId: {result.PaymentId}, Kart: {result.CardFamily} ****{result.LastFourDigits}, Taksit: {result.Installment}";

            if (!string.IsNullOrWhiteSpace(siparis.KuponKodu))
            {
                var kupon = await _context.Kuponlar.FirstOrDefaultAsync(x => x.Kod == siparis.KuponKodu);
                if (kupon != null)
                {
                    kupon.KullanilanMiktar++;
                }
            }

            await ClearOrderCartAsync(siparis);
            await _context.SaveChangesAsync();
            await transaction.CommitAsync();

            HttpContext.Session.Remove("UygulananKupon");
            HttpContext.Session.Remove(PendingPaymentOrderSessionKey);

            _logger.LogInformation(
                "Odeme onaylandi. SiparisNo={SiparisNo}, PaymentId={PaymentId}, Tutar={PaidPrice}",
                siparis.SiparisNo,
                result.PaymentId,
                result.PaidPrice);

            await SendAdminOrderNotificationEmailAsync(siparis);
            await SendCustomerOrderConfirmationEmailAsync(siparis);

            return RedirectToAction(nameof(Basarili), new { siparisNo = siparis.SiparisNo });
        }

        public IActionResult Basarili(string siparisNo)
        {
            ViewBag.SiparisNo = siparisNo;
            return View();
        }

        public IActionResult Basarisiz()
        {
            return View();
        }

        private async Task PrepareCheckoutViewDataAsync(string? userId, string sessionId, List<SepetItem>? sepetItems = null)
        {
            sepetItems ??= await _sepetService.GetSepetItemsAsync(userId, sessionId);
            var araToplam = sepetItems.Sum(x => x.Toplam);
            decimal indirimTutari = 0;
            var kuponKodu = HttpContext.Session.GetString("UygulananKupon");

            if (!string.IsNullOrEmpty(kuponKodu))
            {
                var kupon = await _context.Kuponlar.FirstOrDefaultAsync(x => x.Kod == kuponKodu && !x.SilindiMi);
                if (kupon != null &&
                    kupon.AktifMi &&
                    kupon.SonKullanmaTarihi > DateTime.UtcNow &&
                    (kupon.KullanimLimiti <= 0 || kupon.KullanilanMiktar < kupon.KullanimLimiti) &&
                    araToplam >= kupon.MinSepetTutari)
                {
                    indirimTutari = CalculateCouponDiscount(kupon, araToplam);
                }
                else
                {
                    HttpContext.Session.Remove("UygulananKupon");
                    kuponKodu = null;
                }
            }

            ViewBag.AraToplam = araToplam;
            ViewBag.IndirimTutari = indirimTutari;
            ViewBag.KuponKodu = kuponKodu;
            ViewBag.ToplamTutar = Math.Max(0, araToplam - indirimTutari);
            ViewBag.SepetItems = sepetItems;

            if (!string.IsNullOrWhiteSpace(userId))
            {
                var tumAdresler = await _adresService.GetAllAsync();
                ViewBag.KayitliAdresler = tumAdresler.Where(x => x.AppUserId == userId).ToList();
            }
        }

        private static void NormalizeCheckoutInput(Siparis siparis)
        {
            siparis.MusteriAdSoyad = siparis.MusteriAdSoyad?.Trim() ?? string.Empty;
            siparis.Eposta = siparis.Eposta?.Trim() ?? string.Empty;
            siparis.Sehir = siparis.Sehir?.Trim() ?? string.Empty;
            siparis.Ilce = siparis.Ilce?.Trim() ?? string.Empty;
            siparis.AcikAdres = siparis.AcikAdres?.Trim() ?? string.Empty;

            var temizTel = new string((siparis.Telefon ?? string.Empty).Where(char.IsDigit).ToArray());
            if (!temizTel.StartsWith("0") && temizTel.Length == 10)
            {
                temizTel = "0" + temizTel;
            }

            siparis.Telefon = temizTel;
        }

        private bool ValidateCheckoutInput(Siparis siparis)
        {
            if (string.IsNullOrWhiteSpace(siparis.MusteriAdSoyad))
            {
                ModelState.AddModelError(nameof(Siparis.MusteriAdSoyad), "Ad soyad zorunludur.");
            }

            if (string.IsNullOrWhiteSpace(siparis.Eposta) || !IsValidEmail(siparis.Eposta))
            {
                ModelState.AddModelError(nameof(Siparis.Eposta), "Gecerli bir e-posta adresi girilmelidir.");
            }

            if (siparis.Telefon.Length != 11 || !siparis.Telefon.StartsWith("0"))
            {
                ModelState.AddModelError(nameof(Siparis.Telefon), "Telefon 0 ile baslayan 11 haneli bir numara olmalidir.");
            }

            if (string.IsNullOrWhiteSpace(siparis.Sehir))
            {
                ModelState.AddModelError(nameof(Siparis.Sehir), "Sehir zorunludur.");
            }

            if (string.IsNullOrWhiteSpace(siparis.Ilce))
            {
                ModelState.AddModelError(nameof(Siparis.Ilce), "Ilce zorunludur.");
            }

            if (string.IsNullOrWhiteSpace(siparis.AcikAdres) || siparis.AcikAdres.Length < 10)
            {
                ModelState.AddModelError(nameof(Siparis.AcikAdres), "Acik adres en az 10 karakter olmalidir.");
            }

            return ModelState.IsValid;
        }

        private static bool IsValidEmail(string email)
        {
            try
            {
                var address = new System.Net.Mail.MailAddress(email);
                return string.Equals(address.Address, email, StringComparison.OrdinalIgnoreCase);
            }
            catch
            {
                return false;
            }
        }

        private async Task<string> GenerateUniqueOrderNumberAsync()
        {
            for (var attempt = 0; attempt < 5; attempt++)
            {
                var candidate = DateTime.UtcNow.ToString("yyyyMMddHHmmssfff") + Random.Shared.Next(100, 999);
                if (!await _context.Siparisler.AnyAsync(x => x.SiparisNo == candidate))
                {
                    return candidate;
                }
            }

            return $"{DateTime.UtcNow:yyyyMMddHHmmssfff}{Guid.NewGuid():N}"[..24];
        }

        private async Task<int?> ResolveOrderVariantIdAsync(SepetItem item)
        {
            if (item.UrunSecenekId.HasValue)
            {
                return item.UrunSecenekId.Value;
            }

            var varsayilan = await _context.UrunSecenekleri
                .AsNoTracking()
                .Where(x =>
                    x.UrunId == item.UrunId &&
                    !x.SilindiMi &&
                    x.AktifMi &&
                    (!x.TukeninceGizle || x.StokAdedi > 0 || x.OnSipariseAcikMi))
                .OrderByDescending(x => x.VarsayilanMi)
                .ThenBy(x => x.Sira)
                .ThenBy(x => x.SatisFiyati)
                .FirstOrDefaultAsync();

            return varsayilan?.Id;
        }

        private static decimal CalculateCouponDiscount(Kupon kupon, decimal sepetTutari)
        {
            var discount = kupon.Tip == 0
                ? sepetTutari * (kupon.Deger / 100)
                : kupon.Deger;

            return Math.Round(Math.Min(sepetTutari, Math.Max(0, discount)), 2);
        }

        private async Task SendAdminOrderNotificationEmailAsync(Siparis siparis)
        {
            var settings = _siteSettingsService.GetSettings();
            if (!settings.YeniSiparisMailBildirimi)
            {
                return;
            }

            var recipientEmail = string.IsNullOrWhiteSpace(settings.BildirimAliciEmail)
                ? settings.Email
                : settings.BildirimAliciEmail;

            if (string.IsNullOrWhiteSpace(recipientEmail))
            {
                return;
            }

            var brandName = string.IsNullOrWhiteSpace(settings.MarkaAdi) ? settings.SiteAdi : settings.MarkaAdi;
            var detailUrl = Url.Action("Detay", "Siparis", new { area = "Admin", id = siparis.Id }, Request.Scheme)
                ?? $"{Request.Scheme}://{Request.Host}/Admin/Siparis/Detay/{siparis.Id}";

            var customerName = System.Net.WebUtility.HtmlEncode(siparis.MusteriAdSoyad ?? string.Empty);
            var customerEmail = System.Net.WebUtility.HtmlEncode(siparis.Eposta ?? string.Empty);
            var orderNumber = System.Net.WebUtility.HtmlEncode(siparis.SiparisNo ?? string.Empty);
            var orderItemsHtml = await BuildOrderItemsTableRowsAsync(siparis.Id);

            var body = $@"
                <h3>Yeni onaylanan sipari&#351;</h3>
                <p><strong>Sipari&#351; No:</strong> {orderNumber}</p>
                <p><strong>M&uuml;&#351;teri:</strong> {customerName}</p>
                <p><strong>E-posta:</strong> {customerEmail}</p>
                <p><strong>Tutar:</strong> {siparis.ToplamTutar:N2} TL</p>
                <table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='border:1px solid #e5e2dc; border-radius:10px; background:#fff; margin:16px 0;'>
                    <thead>
                        <tr style='background:#fafaf8;'>
                            <th style='padding:10px; text-align:left; color:#313511;'>Ürün</th>
                            <th style='padding:10px; text-align:center; color:#313511;'>Adet</th>
                            <th style='padding:10px; text-align:right; color:#313511;'>Tutar</th>
                        </tr>
                    </thead>
                    <tbody>{orderItemsHtml}</tbody>
                </table>
                <p><a href=""{detailUrl}"">Admin panelinde sipari&#351;i g&ouml;r&uuml;nt&uuml;le</a></p>";

            try
            {
                await _emailService.SendTemplateMailAsync(
                    recipientEmail,
                    $"{brandName} - Yeni Sipari\u015F {siparis.SiparisNo}",
                    "Operasyon Ekibi",
                    body);
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Yeni siparis mail bildirimi gonderilemedi. SiparisNo={SiparisNo}", siparis.SiparisNo);
            }
        }

        private async Task SendCustomerOrderConfirmationEmailAsync(Siparis siparis)
        {
            if (string.IsNullOrWhiteSpace(siparis.Eposta))
            {
                _logger.LogWarning("Musteri emaili eksik, siparis onay maili gonderilemedi. SiparisNo={SiparisNo}", siparis.SiparisNo);
                return;
            }

            var settings = _siteSettingsService.GetSettings();
            var brandName = string.IsNullOrWhiteSpace(settings.MarkaAdi) ? settings.SiteAdi : settings.MarkaAdi;
            var siteUrl = _siteSettingsService.BuildAbsoluteUrl(string.Empty);

            var detaylar = await _context.SiparisDetaylari
                .Include(x => x.Urun)
                .Include(x => x.UrunSecenek)
                .Where(x => x.SiparisId == siparis.Id && !x.SilindiMi)
                .ToListAsync();

            var urunListesi = new System.Text.StringBuilder();
            foreach (var item in detaylar)
            {
                var urunAdi = System.Net.WebUtility.HtmlEncode(item.Urun?.Baslik ?? "Ürün");
                var detayMetni = System.Net.WebUtility.HtmlEncode(BuildOrderLineDetail(item));
                var adet = item.Adet;
                var fiyat = item.BirimFiyat * item.Adet;
                var notSatiri = !string.IsNullOrWhiteSpace(item.MusteriNotu)
                    ? $"<div style='margin-top:4px; font-size:12px; color:#b58735; font-style:italic;'>Not: {System.Net.WebUtility.HtmlEncode(item.MusteriNotu)}</div>"
                    : string.Empty;
                urunListesi.Append($@"
                    <tr>
                        <td style='padding:12px; border-bottom:1px solid #e5e2dc; color:#47473d;'>
                            <div>{urunAdi}</div>
                            {(string.IsNullOrWhiteSpace(detayMetni) ? string.Empty : $"<div style='margin-top:4px; font-size:12px; color:#6f6a5e;'>{detayMetni}</div>")}
                            {notSatiri}
                        </td>
                        <td style='padding:12px; border-bottom:1px solid #e5e2dc; text-align:center; color:#47473d;'>{adet}</td>
                        <td style='padding:12px; border-bottom:1px solid #e5e2dc; text-align:right; color:#313511; font-weight:600;'>{fiyat:N2} TL</td>
                    </tr>");
            }

            var musteriAdSoyad = System.Net.WebUtility.HtmlEncode(siparis.MusteriAdSoyad ?? "Değerli Müşterimiz");
            var siparisNo = System.Net.WebUtility.HtmlEncode(siparis.SiparisNo ?? "");
            var toplamTutar = siparis.ToplamTutar;
            var teslimatAdresi = $"{siparis.AcikAdres}, {siparis.Ilce}/{siparis.Sehir}";
            var teslimatBilgi = System.Net.WebUtility.HtmlEncode(teslimatAdresi);

            var content = $@"
                <p style='margin-bottom:20px;'>Merhaba <strong>{musteriAdSoyad}</strong>,</p>
                <p style='margin-bottom:20px;'>Sipari&#351;inizi ba&#351;ar&#305;yla ald&#305;k. A&#351;a&#287;&#305;da sipari&#351; &ouml;zeti yer almaktad&#305;r:</p>
                
                <table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='border:1px solid #e5e2dc; border-radius:12px; background:#fff; margin:20px 0;'>
                    <thead>
                        <tr style='background:#fafaf8;'>
                            <th style='padding:12px; border-bottom:2px solid #e5e2dc; text-align:left; color:#313511; font-size:13px;'>Ürün</th>
                            <th style='padding:12px; border-bottom:2px solid #e5e2dc; text-align:center; color:#313511; font-size:13px;'>Adet</th>
                            <th style='padding:12px; border-bottom:2px solid #e5e2dc; text-align:right; color:#313511; font-size:13px;'>Tutar</th>
                        </tr>
                    </thead>
                    <tbody>
                        {urunListesi}
                    </tbody>
                    <tfoot>
                        <tr style='background:#fafaf8;'>
                            <td colspan='2' style='padding:14px; border-top:2px solid #e5e2dc; text-align:right; color:#313511; font-weight:700;'>Toplam:</td>
                            <td style='padding:14px; border-top:2px solid #e5e2dc; text-align:right; color:#b58735; font-size:18px; font-weight:700;'>{toplamTutar:N2} TL</td>
                        </tr>
                    </tfoot>
                </table>
                
                <table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='border:1px solid #e5e2dc; border-radius:12px; background:#fffaf0; margin:20px 0;'>
                    <tr>
                        <td style='padding:16px; color:#47473d;'>
                            <strong style='color:#313511;'>Sipari&#351; No:</strong> <span style='font-size:16px; color:#b58735; font-weight:700;'>{siparisNo}</span>
                        </td>
                    </tr>
                    <tr>
                        <td style='padding:16px; border-top:1px solid #e5e2dc; color:#47473d;'>
                            <strong style='color:#313511;'>Teslimat Adresi:</strong> {teslimatBilgi}
                        </td>
                    </tr>
                </table>
                
                <p style='margin-top:24px; color:#47473d; font-size:14px;'>
                    Sipari&#351;inizin durumunu <a href='{siteUrl}/Profil/Siparislerim' style='color:#313511; text-decoration:underline;'>sipari&#351;lerim</a> sayfas&#305;ndan takip edebilirsiniz.
                </p>
                <p style='margin-top:16px; color:#47473d; font-size:14px;'>
                    Herhangi bir sorunuz veya talebiniz olursa bizimle <a href='{siteUrl}/Kurumsal/Iletisim' style='color:#313511; text-decoration:underline;'>ileti&#351;ime</a> geçebilirsiniz.
                </p>
                <p style='margin-top:24px; color:#999; font-size:13px;'>
                    Bu e-posta otomatik olarak g&ouml;nderilmi&#351;tir. L&uuml;tfen bu mesaj&#305; do&#287;rudan yan&#305;tlamay&#305;n.
                </p>";

            try
            {
                await _emailService.SendTemplateMailAsync(
                    siparis.Eposta,
                    $"{brandName} - Sipari\u015Finiz Al\u0131nd\u0131 ({siparisNo})",
                    musteriAdSoyad,
                    content,
                    "",
                    "");
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Musteri siparis onay maili gonderilemedi. SiparisNo={SiparisNo}, Email={Email}", siparis.SiparisNo, siparis.Eposta);
            }
        }

        private async Task<string> BuildOrderItemsTableRowsAsync(int siparisId)
        {
            var detaylar = await _context.SiparisDetaylari
                .Include(x => x.Urun)
                .Include(x => x.UrunSecenek)
                .Where(x => x.SiparisId == siparisId && !x.SilindiMi)
                .ToListAsync();

            var rows = new System.Text.StringBuilder();
            foreach (var item in detaylar)
            {
                var urunAdi = System.Net.WebUtility.HtmlEncode(item.Urun?.Baslik ?? "Ürün");
                var detayMetni = System.Net.WebUtility.HtmlEncode(BuildOrderLineDetail(item));
                var detayHtml = string.IsNullOrWhiteSpace(detayMetni)
                    ? string.Empty
                    : $"<div style='margin-top:4px; font-size:12px; color:#6f6a5e;'>{detayMetni}</div>";

                rows.Append($@"
                    <tr>
                        <td style='padding:10px; border-top:1px solid #e5e2dc; color:#47473d;'>
                            <div>{urunAdi}</div>
                            {detayHtml}
                        </td>
                        <td style='padding:10px; border-top:1px solid #e5e2dc; text-align:center; color:#47473d;'>{item.Adet}</td>
                        <td style='padding:10px; border-top:1px solid #e5e2dc; text-align:right; color:#313511; font-weight:600;'>{(item.BirimFiyat * item.Adet):N2} TL</td>
                    </tr>");
            }

            return rows.ToString();
        }

        private static string BuildOrderLineDetail(SiparisDetay item)
        {
            var details = new List<string>();
            var variant = item.UrunSecenek;
            if (variant != null)
            {
                var variantText = string.IsNullOrWhiteSpace(variant.VaryantBasligi)
                    ? variant.Olcu
                    : variant.VaryantBasligi;

                if (!string.IsNullOrWhiteSpace(variantText) &&
                    !variantText.Contains("Standart", StringComparison.OrdinalIgnoreCase))
                {
                    details.Add(variantText);
                }
            }

            if (!string.IsNullOrWhiteSpace(item.CerceveModeli) && item.CerceveModeli != "Çerçevesiz")
            {
                details.Add($"Çerçeve: {item.CerceveModeli}");
            }

            return string.Join(" | ", details);
        }

        private bool CanAccessPaymentOrder(Siparis siparis)
        {
            var userId = User.Identity?.IsAuthenticated == true ? _userManager.GetUserId(User) : null;
            if (!string.IsNullOrWhiteSpace(siparis.AppUserId))
            {
                return string.Equals(siparis.AppUserId, userId, StringComparison.Ordinal);
            }

            return HttpContext.Session.GetInt32(PendingPaymentOrderSessionKey) == siparis.Id;
        }

        private async Task ClearOrderCartAsync(Siparis siparis)
        {
            Sepet? sepet = null;

            if (!string.IsNullOrWhiteSpace(siparis.AppUserId))
            {
                sepet = await _context.Sepetler
                    .Include(x => x.SepetItems.Where(i => !i.SilindiMi))
                    .FirstOrDefaultAsync(x => x.AppUserId == siparis.AppUserId && !x.SilindiMi);
            }
            else
            {
                var sessionId = HttpContext.Session.Id;
                sepet = await _context.Sepetler
                    .Include(x => x.SepetItems.Where(i => !i.SilindiMi))
                    .FirstOrDefaultAsync(x =>
                        x.SessionId == sessionId &&
                        string.IsNullOrEmpty(x.AppUserId) &&
                        !x.SilindiMi);
            }

            if (sepet == null)
            {
                return;
            }

            foreach (var item in sepet.SepetItems.Where(x => !x.SilindiMi))
            {
                item.SilindiMi = true;
            }

            sepet.SonGuncellemeTarihi = DateTime.UtcNow;
        }
    }
}

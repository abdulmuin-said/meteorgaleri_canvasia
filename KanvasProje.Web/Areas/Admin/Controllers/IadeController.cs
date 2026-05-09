using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using KanvasProje.Data;
using KanvasProje.Core.Varliklar;

namespace KanvasProje.Web.Areas.Admin.Controllers
{
    [Area("Admin")]
    public class IadeController : AdminBaseController
    {
        private readonly KanvasDbContext _context;

        public IadeController(KanvasDbContext context)
        {
            _context = context;
        }

        public async Task<IActionResult> Index()
        {
            // Talepleri ve ilgili siparişi getir
            var talepler = await _context.IadeTalepleri
                                         .Include(x => x.Siparis)
                                         .OrderByDescending(x => x.OlusturulmaTarihi)
                                         .ToListAsync();
            return View(talepler);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DurumGuncelle(int id, int durum, string adminNotu)
        {
            var talep = await _context.IadeTalepleri.FindAsync(id);
            if (talep == null) return NotFound();

            talep.Durum = durum; // 1: Onay, 2: Tamamlandı, 3: Red
            talep.AdminNotu = adminNotu;

            // Eğer İade Onaylandıysa (1) veya Tamamlandıysa (2), Sipariş durumunu da güncelle
            var siparis = await _context.Siparisler.FindAsync(talep.SiparisId);
            if (siparis != null)
            {
                if (durum == 1) siparis.Durum = 6; // İade Onaylandı (Kargo Bekleniyor)
                else if (durum == 2) siparis.Durum = 7; // İade Tamamlandı (Para İade Edildi)
                else if (durum == 3) siparis.Durum = 3; // Reddedilirse tekrar "Teslim Edildi"ye dönsün
            }

            await _context.SaveChangesAsync();
            return RedirectToAction("Index");
        }
    }
}

using KanvasProje.Core.Models;
using KanvasProje.Service.Services;
using Microsoft.AspNetCore.Mvc;

namespace KanvasProje.Web.Areas.Admin.Controllers
{
    [Area("Admin")]
    public class AnaSayfaController : AdminBaseController
    {
        private readonly IHomePageSettingsService _homePageSettingsService;
        private readonly IWebHostEnvironment _env;

        public AnaSayfaController(IHomePageSettingsService homePageSettingsService, IWebHostEnvironment env)
        {
            _homePageSettingsService = homePageSettingsService;
            _env = env;
        }

        public IActionResult Index()
        {
            return View(_homePageSettingsService.GetSettings());
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Index(HomePageSettingsModel model, IList<IFormFile> SlideImages)
        {
            try
            {
                // Resim Yukleme Islemi
                if (SlideImages != null && SlideImages.Count > 0)
                {
                    string uploadsFolder = Path.Combine(_env.WebRootPath, "uploads", "slider");
                    if (!Directory.Exists(uploadsFolder))
                    {
                        Directory.CreateDirectory(uploadsFolder);
                    }

                    // SlideImages sayisi 3'e esit olmayabilir, input array oldugu icin sirayla gelir.
                    // Fakat null olanlar (secilmeyenler) gelmeyebilir. Bizim formda her slide icin bir dosya input'u var.
                    // Ancak bazi dosyalar secilmeyebilir. Bu yuzden Request.Form.Files uzerinden iterasyon yapmak daha guvenli olabilir.
                    // Veya HTML'de her dosya girdisi icin name="SlideImages" var. C# secilmeyenleri null olarak atamaz, atlar.
                    // O yuzden dosyalarin indexini anlamak icin IFormFile objesinin "Name" propuna gore ayirmaliyiz ama hepsi ayni.
                    // En iyisi Request uzerinden ilerlemek.
                    
                    int fileIndex = 0;
                    for (int i = 0; i < model.Hero.DesktopSlides.Count; i++)
                    {
                        var file = Request.Form.Files.Count > i ? Request.Form.Files[i] : null;
                        
                        // Eger bu form verilerinde gercekten bir dosya var mi diye kontrol edelim:
                        // Aslinda, formda her slayt icin input type=file var. 
                        // Sadece secilenler gelir. Biz her input'a farkli isim de verebilirdik.
                    }
                }
                
                // Daha saglam bir upload yontemi: HTML'de "name" attr'unu degistirmedim ama Request.Form.Files ile tek tek gezecegiz.
                // HTML'de name="SlideImages" dedigimiz icin, IFormFileCollection'da tum secilen dosyalar olur.
                // HTML formunda her slaytin input type="file" alani oldugu icin sirali sekilde gelirler.
                // Ancak bos birakilan inputlar List'e dahil edilmez.
                
                // Bunu engellemek icin gercek yukleme mantigi:
                var files = Request.Form.Files;
                int fileUploadIndex = 0;
                
                // Burada SlideImages listesine gelen dosyalari sirasiyla bos olan/olmayan seklinde alamayiz.
                // O yuzden dosyalari direk modelin icine alip, onden degistirmedigim alanlar haric, yenilerini kaydedecegim.
            }
            catch (Exception ex)
            {
                TempData["Hata"] = "Ana sayfa blok ayarlari kaydedilirken hata olustu: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }

            return RedirectToAction(nameof(Index));
        }
    }
}

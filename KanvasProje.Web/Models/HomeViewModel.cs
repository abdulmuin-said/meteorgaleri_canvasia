using KanvasProje.Core.Varliklar;
using KanvasProje.Core.Models;

namespace KanvasProje.Web.Models
{
    public class HomeViewModel
    {
        public List<Urun> VitrinUrunleri { get; set; } = new List<Urun>();
        public List<Urun> BesParcaliKoleksiyon { get; set; } = new List<Urun>();
        public List<Urun> CokSatanlar { get; set; } = new List<Urun>();
        public List<Urun> FirsatUrunleri { get; set; } = new List<Urun>();
        public List<Kategori> Kategoriler { get; set; } = new List<Kategori>();
        public HomePageSettingsModel HomePageSettings { get; set; } = new HomePageSettingsModel();
        public List<Slayt> AktifSlaytlar { get; set; } = new List<Slayt>();
    }
}

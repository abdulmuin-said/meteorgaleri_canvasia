import os

layout_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Shared\_Layout.cshtml"
with open(layout_path, "r", encoding="utf-8") as f:
    layout = f.read()

script = """
        // Favori Toggle İşlemi
        window.toggleFavori = function(btn, urunId) {
            event.preventDefault();
            event.stopPropagation();
            
            const originalHtml = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin text-sm"></i>';
            btn.disabled = true;

            // Form tabanlı AntiForgeryToken almak için
            let token = document.querySelector('input[name="__RequestVerificationToken"]')?.value;
            
            fetch('/Favori/Toggle?urunId=' + urunId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'RequestVerificationToken': token || ''
                }
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    if(data.isAdded) {
                        btn.innerHTML = '<i class="fas fa-heart text-sm text-red-500"></i>';
                        if(window.showToast) window.showToast('Ürün favorilerinize eklendi.', 'success');
                    } else {
                        btn.innerHTML = '<i class="far fa-heart text-sm text-[#47473d] group-hover/btn:text-red-500"></i>';
                        if(window.showToast) window.showToast('Ürün favorilerinizden çıkarıldı.', 'info');
                    }
                } else {
                    if (data.message === "Lütfen önce giriş yapınız.") {
                        window.location.href = '/Hesap/GirisYap?ReturnUrl=' + window.location.pathname;
                    } else {
                        if(window.showToast) window.showToast(data.message || 'Bir hata oluştu.', 'error');
                        btn.innerHTML = originalHtml;
                    }
                }
            })
            .catch(err => {
                console.error(err);
                if(window.showToast) window.showToast('Bağlantı hatası.', 'error');
                btn.innerHTML = originalHtml;
            })
            .finally(() => {
                btn.disabled = false;
            });
        };
"""

if "window.toggleFavori =" not in layout:
    # Inject before </script></body>
    layout = layout.replace("</script>\n</body>", script + "\n</script>\n</body>")
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout)
    print("ToggleFavori JS added to layout.")

# Add AntiForgeryToken to Layout if not present so fetch can use it
if '__RequestVerificationToken' not in layout:
    token_form = """    <!-- Arama Modal Bitiş -->
    <form id="globalAntiForgeryForm" class="hidden">
        @Html.AntiForgeryToken()
    </form>"""
    layout = layout.replace("    <!-- Arama Modal Bitiş -->", token_form)
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout)
    print("AntiForgeryToken added to Layout.")

# Update Home/Index.cshtml
home_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Home\Index.cshtml"
with open(home_path, "r", encoding="utf-8") as f:
    home = f.read()

heart_btn = """<button type="button" onclick="window.toggleFavori(this, @urun.Id)" class="group/btn absolute top-2 right-2 w-8 h-8 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center transition-colors shadow-sm z-20" title="Favorilere Ekle">
                            <i class="far fa-heart text-sm text-[#47473d] group-hover/btn:text-red-500 transition-colors"></i>
                        </button>"""

if "window.toggleFavori" not in home:
    home = home.replace(
        '<span class="absolute top-2 left-2 bg-white px-2 py-1 text-[10px] uppercase tracking-wider z-10 shadow-sm text-[#313511]">\n                                @(urun.YeniUrunMu ? "Yeni" : "Fırsat")\n                            </span>',
        '<span class="absolute top-2 left-2 bg-white px-2 py-1 text-[10px] uppercase tracking-wider z-10 shadow-sm text-[#313511]">\n                                @(urun.YeniUrunMu ? "Yeni" : "Fırsat")\n                            </span>\n                            ' + heart_btn
    )
    
    home = home.replace(
        '<a href="@BuildProductUrl(urun)" class="block relative overflow-hidden mb-4 aspect-square bg-[#f1ede7]">\n                        @if',
        '<div class="relative overflow-hidden mb-4 aspect-square bg-[#f1ede7]">\n                        <a href="@BuildProductUrl(urun)" class="block w-full h-full">\n                        @if'
    )
    
    # Needs careful string replacements for Home/Index.cshtml
    pass

# We will just rewrite the "Öne Çıkan Eserler" block to ensure clean HTML.
import re

vitrin_block = re.search(r'<!-- BEGIN: Öne Çıkan Eserler \(Vitrin\) -->(.*?)<!-- END: Öne Çıkan Eserler -->', home, re.DOTALL)
if vitrin_block:
    old_vitrin = vitrin_block.group(1)
    
    new_vitrin = """
@if (Model.VitrinUrunleri != null && Model.VitrinUrunleri.Any())
{
    <section class="py-16 container mx-auto px-4">
        <div class="flex items-center justify-center mb-10">
            <hr class="w-1/4 border-[#e5e2dc] hidden md:block"/>
            <h2 class="font-serif text-3xl mx-8 text-center text-[#313511]">Öne Çıkan Eserler</h2>
            <hr class="w-1/4 border-[#e5e2dc] hidden md:block"/>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-6">
            @foreach (var urun in Model.VitrinUrunleri.Take(5))
            {
                <div class="group cursor-pointer flex flex-col">
                    <div class="relative overflow-hidden mb-4 aspect-square bg-[#f1ede7]">
                        <a href="@BuildProductUrl(urun)" class="block w-full h-full">
                            @if (urun.YeniUrunMu || urun.IndirimVarMi)
                            {
                                <span class="absolute top-2 left-2 bg-white px-2 py-1 text-[10px] uppercase tracking-wider z-10 shadow-sm text-[#313511]">
                                    @(urun.YeniUrunMu ? "Yeni" : "Fırsat")
                                </span>
                            }
                            @{
                                var gorsel = !string.IsNullOrWhiteSpace(urun.AnaGorselUrl)
                                    ? urun.AnaGorselUrl
                                    : urun.UrunResimleri?.OrderBy(r => r.Sira).FirstOrDefault()?.ResimYolu;
                            }
                            @if (!string.IsNullOrWhiteSpace(gorsel))
                            {
                                <img alt="@urun.Baslik" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="@gorsel" loading="lazy"/>
                            }
                            else
                            {
                                <div class="w-full h-full flex items-center justify-center text-gray-300">
                                    <i class="fas fa-image fa-2x"></i>
                                </div>
                            }
                        </a>
                        <button type="button" onclick="window.toggleFavori(this, @urun.Id)" class="group/btn absolute top-2 right-2 w-8 h-8 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center transition-colors shadow-sm z-20" title="Favorilere Ekle">
                            <i class="far fa-heart text-sm text-[#47473d] group-hover/btn:text-red-500 transition-colors"></i>
                        </button>
                    </div>
                    <h3 class="text-xs font-semibold mb-1 text-[#1c1c18] tracking-wide line-clamp-2">
                        <a href="@BuildProductUrl(urun)" class="hover:text-[#b58735] transition-colors">@urun.Baslik</a>
                    </h3>
                    <p class="text-xs text-[#47473d]">@urun.EtkinFiyat.ToString("N0") @currencySymbol</p>
                </div>
            }
        </div>
        <div class="text-center mt-12">
            <a href="/Urun" class="inline-block border border-[#313511] text-[#313511] px-8 py-3 text-xs tracking-widest hover:bg-[#313511] hover:text-white transition-colors uppercase rounded-full">
                Tümünü Gör
            </a>
        </div>
    </section>
}
"""
    home = home.replace(old_vitrin, new_vitrin)
    with open(home_path, "w", encoding="utf-8") as f:
        f.write(home)
    print("Home Index updated with heart buttons.")
"""
import os

# 1. Update Favori/Index.cshtml
favori_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Favori\Index.cshtml"

new_favori = """@model IEnumerable<KanvasProje.Core.Varliklar.Urun>
@inject KanvasProje.Service.Services.ISiteSettingsService SiteSettingsService
@{
    ViewData["Title"] = "Favorilerim";
    var currencySymbol = "TL";
}

<form id="favoriAntiForgeryForm" class="hidden">
    @Html.AntiForgeryToken()
</form>

<!-- Breadcrumb -->
<div class="bg-[#f1ede7] border-b border-[#e5e2dc] py-3">
    <div class="container mx-auto px-4 flex items-center gap-2 text-xs text-[#47473d]">
        <a href="/" class="hover:text-[#313511] transition-colors">Ana Sayfa</a>
        <span>/</span>
        <a href="/Profil" class="hover:text-[#313511] transition-colors">Hesabım</a>
        <span>/</span>
        <span class="text-[#1c1c18] font-medium">Favorilerim</span>
    </div>
</div>

<div class="container mx-auto px-4 py-16 max-w-6xl">
    <div class="text-center mb-12">
        <h1 class="font-serif text-3xl md:text-5xl text-[#313511] mb-4">Favori Koleksiyonum</h1>
        <p class="text-sm text-[#47473d]">Beğendiğiniz eserler burada sizi bekliyor.</p>
    </div>

    @if (!Model.Any())
    {
        <div class="text-center py-16 bg-white border border-[#e5e2dc] rounded-lg">
            <i class="far fa-heart text-6xl text-[#e5e2dc] mb-4"></i>
            <h4 class="font-serif text-2xl text-[#313511] mb-2">Henüz favori ürününüz yok.</h4>
            <p class="text-sm text-[#47473d] mb-6">Koleksiyonumuzu keşfederek beğendiğiniz ürünleri favorilerinize ekleyebilirsiniz.</p>
            <a href="/Urun" class="inline-block bg-[#313511] text-white px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors">
                Koleksiyonu Keşfet
            </a>
        </div>
    }
    else
    {
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6" id="favoriListesi">
            @foreach (var urun in Model)
            {
                var urlSlug = string.IsNullOrEmpty(urun.Slug) ? urun.Id.ToString() : $"{urun.Slug}-{urun.Id}";
                <div class="favori-item group relative flex flex-col bg-white border border-[#e5e2dc] hover:border-[#b58735] transition-colors rounded-lg overflow-hidden">
                    <div class="relative aspect-[4/5] bg-[#fcf9f3] overflow-hidden">
                        <a href="/Urun/Detay/@urlSlug" class="block w-full h-full">
                            <img src="@urun.AnaGorselUrl" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" alt="@urun.Baslik" loading="lazy">
                        </a>
                        
                        <button onclick="favoridenCikar(this, @urun.Id)" class="absolute top-3 right-3 w-8 h-8 bg-white/90 backdrop-blur-sm rounded-full text-red-500 flex items-center justify-center hover:bg-white transition-colors shadow-sm" title="Favorilerden Çıkar">
                            <i class="fas fa-heart"></i>
                        </button>
                    </div>

                    <div class="p-4 flex flex-col flex-1">
                        <h6 class="font-semibold text-sm text-[#1c1c18] mb-1 line-clamp-1">
                            <a href="/Urun/Detay/@urlSlug" class="hover:text-[#b58735] transition-colors">@urun.Baslik</a>
                        </h6>
                        <p class="text-sm text-[#47473d] mb-4">@urun.Fiyat.ToString("N2") @currencySymbol</p>

                        <button type="button" class="mt-auto w-full border border-[#313511] text-[#313511] hover:bg-[#313511] hover:text-white py-2 text-xs tracking-widest uppercase rounded transition-colors" onclick="favoriSepeteEkle(this, @urun.Id)">
                            Sepete Ekle
                        </button>
                    </div>
                </div>
            }
        </div>
    }
</div>

<script>
    function getAntiForgeryToken() {
        return document.querySelector('#favoriAntiForgeryForm input[name="__RequestVerificationToken"]').value;
    }

    function favoridenCikar(btn, id) {
        if (!confirm('Bu ürünü favorilerden kaldırmak istediğinize emin misiniz?')) return;

        fetch('/Favori/Toggle?urunId=' + id, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'RequestVerificationToken': getAntiForgeryToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var kart = btn.closest('.favori-item');
                kart.style.transition = 'all 0.4s ease';
                kart.style.opacity = '0';
                kart.style.transform = 'scale(0.9)';
                setTimeout(function () {
                    kart.remove();
                    if (window.showToast) window.showToast('Ürün favorilerden çıkarıldı.', 'info');
                    var kalanUrunler = document.querySelectorAll('.favori-item');
                    if (kalanUrunler.length === 0) { location.reload(); }
                }, 400);
            } else {
                if (window.showToast) window.showToast(data.message || 'İşlem başarısız.', 'error');
            }
        })
        .catch(error => {
            console.error('Hata:', error);
            if (window.showToast) window.showToast('Bağlantı hatası.', 'error');
        });
    }

    function favoriSepeteEkle(btn, urunId) {
        var originalHtml = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        btn.disabled = true;

        fetch('/Sepet/Ekle?UrunId=' + urunId + '&Adet=1', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'RequestVerificationToken': getAntiForgeryToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                btn.innerHTML = '<i class="fas fa-check"></i>';
                btn.classList.add('bg-[#313511]', 'text-white');
                
                if (window.showToast) window.showToast('Ürün sepetinize eklendi.', 'success');

                var cartBadge = document.getElementById('cartItemCount');
                if (cartBadge) {
                    var count = parseInt(cartBadge.textContent) || 0;
                    cartBadge.textContent = count + 1;
                    cartBadge.classList.add('scale-150');
                    setTimeout(() => cartBadge.classList.remove('scale-150'), 300);
                }

                setTimeout(function () {
                    btn.innerHTML = originalHtml;
                    btn.classList.remove('bg-[#313511]', 'text-white');
                    btn.disabled = false;
                }, 2000);
            } else {
                if (window.showToast) window.showToast(data.message || 'Hata oluştu.', 'error');
                btn.innerHTML = originalHtml;
                btn.disabled = false;
            }
        })
        .catch(err => {
            console.error(err);
            if (window.showToast) window.showToast('Bağlantı hatası.', 'error');
            btn.innerHTML = originalHtml;
            btn.disabled = false;
        });
    }
</script>
"""

with open(favori_path, "w", encoding="utf-8") as f:
    f.write(new_favori)

# 2. Add Heart icon to layout
layout_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Shared\_Layout.cshtml"
with open(layout_path, "r", encoding="utf-8") as f:
    layout = f.read()

# The layout has the search and cart icons inside a flex container
# We need to insert the Heart icon between Search and Cart
old_icons = """                <!-- Arama -->
                <button type="button" aria-label="Arama" class="hover:text-[#b58735] transition-colors" onclick="document.getElementById('fullscreenSearch').classList.remove('hidden'); document.getElementById('fullscreenSearch').classList.add('flex'); setTimeout(() => document.getElementById('fullscreenSearchInput').focus(), 100);">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 24 24"><path d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
                </button>

                <!-- Sepet -->
                <a href="/Sepet" aria-label="Sepet" class="relative">"""

new_icons = """                <!-- Arama -->
                <button type="button" aria-label="Arama" class="hover:text-[#b58735] transition-colors" onclick="document.getElementById('fullscreenSearch').classList.remove('hidden'); document.getElementById('fullscreenSearch').classList.add('flex'); setTimeout(() => document.getElementById('fullscreenSearchInput').focus(), 100);">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 24 24"><path d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
                </button>

                <!-- Favoriler -->
                <a href="/Favori" aria-label="Favoriler" class="hover:text-red-500 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" /></svg>
                </a>

                <!-- Sepet -->
                <a href="/Sepet" aria-label="Sepet" class="relative">"""

if old_icons in layout:
    layout = layout.replace(old_icons, new_icons)
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout)
    print("Heart icon added to Layout.")
else:
    print("Could not find the insertion point for Heart icon in Layout.")

print("Favori Index updated.")

import os

def write_view(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. Profil/HesabiSil.cshtml
hesabi_sil = """@{
    ViewData["Title"] = "Hesabı Sil";
}

<div class="bg-[#f1ede7] border-b border-[#e5e2dc] py-3">
    <div class="container mx-auto px-4 flex items-center gap-2 text-xs text-[#47473d]">
        <a href="/" class="hover:text-[#313511] transition-colors">Ana Sayfa</a>
        <span>/</span>
        <a href="/Profil" class="hover:text-[#313511] transition-colors">Hesabım</a>
        <span>/</span>
        <span class="text-[#1c1c18] font-medium">Hesabı Sil</span>
    </div>
</div>

<div class="container mx-auto px-4 py-16 max-w-2xl text-center">
    <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-100 mb-6">
        <i class="fas fa-exclamation-triangle text-4xl text-red-600"></i>
    </div>
    <h1 class="font-serif text-3xl tracking-widest text-[#313511] uppercase mb-4">Hesabınızı Silmek Üzeresiniz</h1>
    <p class="text-sm text-[#47473d] mb-8 leading-relaxed">
        Hesabınızı silerseniz sipariş geçmişiniz, favorileriniz ve tüm kayıtlı adres bilgileriniz kalıcı olarak silinecektir. Bu işlem geri alınamaz. 
        Onaylıyor musunuz?
    </p>

    <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <form asp-action="HesabiSilOnay" method="post" class="w-full sm:w-auto">
            <button type="submit" class="w-full sm:w-auto bg-red-600 text-white px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-red-700 transition-colors flex items-center justify-center gap-2">
                <i class="fas fa-trash"></i> Evet, Hesabımı Sil
            </button>
        </form>
        <a href="/Profil" class="w-full sm:w-auto bg-white border border-[#e5e2dc] text-[#313511] px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#fcf9f3] transition-colors inline-block text-center">
            Vazgeç
        </a>
    </div>
</div>
"""
write_view(r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Profil\HesabiSil.cshtml", hesabi_sil)

# 2. Profil/IadeOlustur.cshtml
iade_olustur = """@model KanvasProje.Core.Varliklar.Siparis
@{
    ViewData["Title"] = "İade Talebi Oluştur";
}

<div class="bg-[#f1ede7] border-b border-[#e5e2dc] py-3">
    <div class="container mx-auto px-4 flex items-center gap-2 text-xs text-[#47473d]">
        <a href="/" class="hover:text-[#313511] transition-colors">Ana Sayfa</a>
        <span>/</span>
        <a href="/Profil" class="hover:text-[#313511] transition-colors">Hesabım</a>
        <span>/</span>
        <a href="/Profil/Siparislerim" class="hover:text-[#313511] transition-colors">Siparişlerim</a>
        <span>/</span>
        <span class="text-[#1c1c18] font-medium">İade Talebi</span>
    </div>
</div>

<div class="container mx-auto px-4 py-10 max-w-3xl">
    <h1 class="font-serif text-3xl text-[#313511] mb-6">İade Talebi Oluştur</h1>
    
    <div class="bg-white border border-[#e5e2dc] rounded-lg p-6 mb-8">
        <h3 class="font-bold text-[#1c1c18] mb-4 border-b border-[#e5e2dc] pb-2">Sipariş Bilgileri</h3>
        <p class="text-sm text-[#47473d] mb-2"><strong>Sipariş No:</strong> @Model.SiparisNo</p>
        <p class="text-sm text-[#47473d] mb-2"><strong>Tarih:</strong> @Model.OlusturulmaTarihi.ToString("dd.MM.yyyy")</p>
        <p class="text-sm text-[#47473d]"><strong>Tutar:</strong> @Model.ToplamTutar.ToString("N2") TL</p>
    </div>

    <form asp-action="IadeTalebiGonder" method="post" class="space-y-6">
        <input type="hidden" name="siparisId" value="@Model.Id" />
        
        <div>
            <label class="block text-xs uppercase tracking-widest text-[#1c1c18] font-medium mb-2">İade Nedeni</label>
            <select name="IadeNedeni" required class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3]">
                <option value="">Seçiniz</option>
                <option value="Hasarlı Ürün">Ürün hasarlı geldi</option>
                <option value="Yanlış Ürün">Yanlış ürün gönderildi</option>
                <option value="Beklentimi Karşılamadı">Ürün beklentimi karşılamadı</option>
                <option value="Vazgeçtim">Satın almaktan vazgeçtim</option>
            </select>
        </div>

        <div>
            <label class="block text-xs uppercase tracking-widest text-[#1c1c18] font-medium mb-2">Açıklama (İsteğe Bağlı)</label>
            <textarea name="Aciklama" rows="4" class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3] resize-none" placeholder="İade talebinizle ilgili eklemek istedikleriniz..."></textarea>
        </div>

        <div class="flex gap-4">
            <button type="submit" class="bg-[#313511] text-white px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors">
                Talebi Gönder
            </button>
            <a href="/Profil/Siparislerim" class="bg-white border border-[#e5e2dc] text-[#313511] px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#fcf9f3] transition-colors inline-flex items-center">
                İptal
            </a>
        </div>
    </form>
</div>
"""
write_view(r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Profil\IadeOlustur.cshtml", iade_olustur)

# 3. Siparis/Basarisiz.cshtml
siparis_basarisiz = """@{
    ViewData["Title"] = "Ödeme Başarısız";
}

<div class="min-h-[70vh] flex items-center justify-center py-16 px-4 bg-[#fcf9f3]">
    <div class="w-full max-w-lg text-center">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-100 mb-6">
            <i class="fas fa-times text-4xl text-red-600"></i>
        </div>
        <h1 class="font-serif text-3xl tracking-widest text-red-700 uppercase mb-4">Ödeme Başarısız</h1>
        
        @if (ViewBag.Hata != null)
        {
            <div class="bg-white border border-red-200 text-red-700 text-sm px-6 py-4 rounded-lg mb-8 shadow-sm">
                <p class="font-medium">Hata Detayı:</p>
                <p class="mt-1">@ViewBag.Hata</p>
            </div>
        }
        else
        {
            <p class="text-sm text-[#47473d] mb-8 leading-relaxed">
                Ödeme işleminiz sırasında bir sorun oluştu ve siparişiniz tamamlanamadı. Kredi kartı bilgilerinizde veya limitinizde bir sorun olabilir.
            </p>
        }

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="/Sepet" class="w-full sm:w-auto bg-[#313511] text-white px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors">
                Sepete Dön ve Tekrar Dene
            </a>
            <a href="/Kurumsal/Iletisim" class="w-full sm:w-auto bg-white border border-[#e5e2dc] text-[#313511] px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#fcf9f3] transition-colors">
                Destek Al
            </a>
        </div>
    </div>
</div>
"""
write_view(r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Siparis\Basarisiz.cshtml", siparis_basarisiz)

print("Profil and Siparis views updated.")

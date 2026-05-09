import os

base_dir = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Hesap"

def write_view(filename, content):
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)

# 1. SifremiUnuttum.cshtml
sifre_unuttum = """@{
    ViewData["Title"] = "Şifremi Unuttum";
}

<div class="min-h-[80vh] flex items-center justify-center py-16 px-4 bg-[#fcf9f3]">
    <div class="w-full max-w-md">
        <div class="text-center mb-10">
            <h1 class="font-serif text-3xl tracking-widest text-[#313511] uppercase">Şifremi Unuttum</h1>
            <p class="text-xs text-[#47473d] mt-2 tracking-wide">E-posta adresinizi girin, sıfırlama bağlantısı gönderelim.</p>
        </div>

        @if (TempData["Basari"] != null)
        {
            <div class="bg-green-50 border border-green-200 text-green-700 text-sm px-4 py-3 rounded mb-6 flex items-center gap-2">
                <i class="fas fa-check-circle"></i>
                @TempData["Basari"]
            </div>
        }
        @if (ViewBag.Hata != null)
        {
            <div class="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded mb-6 flex items-center gap-2">
                <i class="fas fa-exclamation-circle"></i>
                @ViewBag.Hata
            </div>
        }

        <div class="bg-white border border-[#e5e2dc] rounded-lg p-8 shadow-sm">
            <form asp-action="SifremiUnuttum" method="post" class="space-y-5">
                <div>
                    <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Kayıtlı E-posta</label>
                    <input name="eposta" type="email" placeholder="ornek@mail.com" required
                           class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3] transition-colors" />
                </div>
                <button type="submit"
                        class="w-full bg-[#313511] text-white py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors flex items-center justify-center gap-2">
                    <i class="fas fa-envelope"></i> Bağlantı Gönder
                </button>
            </form>
            <div class="mt-6 text-center">
                <a href="/Hesap/GirisYap" class="text-xs text-[#b58735] hover:underline uppercase tracking-widest">Giriş Ekranına Dön</a>
            </div>
        </div>
    </div>
</div>
"""
write_view("SifremiUnuttum.cshtml", sifre_unuttum)

# 2. SifreSifirla.cshtml
sifre_sifirla = """@model KanvasProje.Core.Varliklar.AppUser
@{
    ViewData["Title"] = "Şifre Sıfırlama";
    var token = Context.Request.Query["token"].ToString();
    var eposta = Context.Request.Query["eposta"].ToString();
}

<div class="min-h-[80vh] flex items-center justify-center py-16 px-4 bg-[#fcf9f3]">
    <div class="w-full max-w-md">
        <div class="text-center mb-10">
            <h1 class="font-serif text-3xl tracking-widest text-[#313511] uppercase">Yeni Şifre</h1>
            <p class="text-xs text-[#47473d] mt-2 tracking-wide">Lütfen yeni şifrenizi belirleyin.</p>
        </div>

        @if (ViewBag.Hata != null)
        {
            <div class="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded mb-6 flex items-center gap-2">
                <i class="fas fa-exclamation-circle"></i>
                @ViewBag.Hata
            </div>
        }

        <div class="bg-white border border-[#e5e2dc] rounded-lg p-8 shadow-sm">
            <form asp-action="SifreSifirlaPost" method="post" class="space-y-5">
                <input type="hidden" name="token" value="@token" />
                <input type="hidden" name="eposta" value="@eposta" />

                <div>
                    <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Yeni Şifre</label>
                    <input name="yeniSifre" type="password" placeholder="••••••••" required
                           class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3] transition-colors" />
                </div>
                <div>
                    <label class="block text-xs font-medium text-[#1c1c18] tracking-wide mb-1.5 uppercase">Şifre Tekrar</label>
                    <input name="yeniSifreTekrar" type="password" placeholder="••••••••" required
                           class="w-full border border-[#e5e2dc] rounded px-4 py-3 text-sm focus:ring-1 focus:ring-[#b58735] focus:border-[#b58735] outline-none bg-[#fcf9f3] transition-colors" />
                </div>
                <button type="submit"
                        class="w-full bg-[#313511] text-white py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors flex items-center justify-center gap-2">
                    <i class="fas fa-lock"></i> Şifreyi Güncelle
                </button>
            </form>
        </div>
    </div>
</div>
"""
write_view("SifreSifirla.cshtml", sifre_sifirla)

# 3. EpostaOnayBilgilendirme.cshtml
eposta_onay = """@{
    ViewData["Title"] = "E-posta Onayı Gerekli";
}

<div class="min-h-[80vh] flex items-center justify-center py-16 px-4 bg-[#fcf9f3]">
    <div class="w-full max-w-lg text-center">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-[#e2e6b3] mb-6">
            <i class="fas fa-envelope-open-text text-3xl text-[#313511]"></i>
        </div>
        <h1 class="font-serif text-3xl tracking-widest text-[#313511] uppercase mb-4">E-Posta Onayı</h1>
        <p class="text-sm text-[#47473d] mb-8 leading-relaxed">
            Kayıt işleminizi tamamlamak için e-posta adresinize bir onay bağlantısı gönderdik. Lütfen gelen kutunuzu (veya spam klasörünü) kontrol ederek e-postanızı doğrulayın.
        </p>
        <a href="/Hesap/GirisYap" class="inline-block bg-[#313511] text-white px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors">
            Giriş Ekranına Dön
        </a>
    </div>
</div>
"""
write_view("EpostaOnayBilgilendirme.cshtml", eposta_onay)

# 4. DogrulamaBasarili.cshtml
dogrulama_basarili = """@{
    ViewData["Title"] = "Doğrulama Başarılı";
}

<div class="min-h-[80vh] flex items-center justify-center py-16 px-4 bg-[#fcf9f3]">
    <div class="w-full max-w-lg text-center">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-green-100 mb-6">
            <i class="fas fa-check text-4xl text-green-600"></i>
        </div>
        <h1 class="font-serif text-3xl tracking-widest text-[#313511] uppercase mb-4">Hesabınız Doğrulandı!</h1>
        <p class="text-sm text-[#47473d] mb-8 leading-relaxed">
            E-posta adresiniz başarıyla doğrulandı. Artık hesabınıza güvenle giriş yapabilirsiniz.
        </p>
        <a href="/Hesap/GirisYap" class="inline-block bg-[#313511] text-white px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors">
            Giriş Yap
        </a>
    </div>
</div>
"""
write_view("DogrulamaBasarili.cshtml", dogrulama_basarili)

# 5. ErisimEngellendi.cshtml
erisim_engellendi = """@{
    ViewData["Title"] = "Erişim Engellendi";
}

<div class="min-h-[80vh] flex items-center justify-center py-16 px-4 bg-[#fcf9f3]">
    <div class="w-full max-w-lg text-center">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-100 mb-6">
            <i class="fas fa-ban text-4xl text-red-600"></i>
        </div>
        <h1 class="font-serif text-3xl tracking-widest text-red-700 uppercase mb-4">Yetkisiz Erişim</h1>
        <p class="text-sm text-[#47473d] mb-8 leading-relaxed">
            Bu sayfaya erişim yetkiniz bulunmamaktadır.
        </p>
        <a href="/" class="inline-block bg-[#313511] text-white px-8 py-3 text-xs tracking-widest uppercase rounded hover:bg-[#1c2001] transition-colors">
            Ana Sayfaya Dön
        </a>
    </div>
</div>
"""
write_view("ErisimEngellendi.cshtml", erisim_engellendi)

print("Hesap views updated.")

import re

with open(r'e:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Shared\_Layout.cshtml', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix mobile icons
content = content.replace('<a href="/Profil" aria-label="Hesabım" title="Hesabım" class="hidden md:block">', '<a href="/Profil" aria-label="Hesabım" title="Hesabım" class="md:block">')
content = content.replace('<a href="/Hesap/GirisYap" aria-label="Giriş Yap" title="Giriş Yap" class="hidden md:block">', '<a href="/Hesap/GirisYap" aria-label="Giriş Yap" title="Giriş Yap" class="md:block">')
content = content.replace('<a href="/Favori" aria-label="Favoriler" class="hover:text-red-500 transition-colors hidden md:block">', '<a href="/Favori" aria-label="Favoriler" class="hover:text-red-500 transition-colors md:block">')

# 2. Dynamic Logo
old_logo = '''            <!-- Logo -->
            <a class="mb-4 mt-2" href="/">
                <h1 class="font-serif text-2xl md:text-3xl tracking-widest text-[#313511] font-medium text-center">@brandName</h1>
            </a>'''
new_logo = '''            <!-- Logo -->
            <a class="mb-4 mt-2" href="/">
                @if (!string.IsNullOrEmpty(siteSettings.SiteLogoUrl)) {
                    <img src="@siteSettings.SiteLogoUrl" alt="@siteSettings.MarkaAdi" class="h-[40px] md:h-[50px] object-contain mx-auto" />
                } else {
                    <h1 class="font-serif text-2xl md:text-3xl tracking-widest text-[#313511] font-medium text-center">@siteSettings.MarkaAdi</h1>
                }
            </a>'''
content = content.replace(old_logo, new_logo)

# 3. Dynamic Footer
old_footer = '''                <!-- Footer Links -->
                <div class="flex flex-col md:items-end">
                    <h4 class="font-bold text-sm tracking-widest mb-4 uppercase text-[#c6ca99]">KURUMSAL</h4>
                    <ul class="space-y-2 text-sm font-light text-gray-300 text-left md:text-right">
                        <li><a class="hover:text-white transition-colors" href="/Kurumsal/Hakkimizda">Hakkımızda</a></li>
                        <li><a class="hover:text-white transition-colors" href="/Kurumsal/Iletisim">İletişim</a></li>
                        <li><a class="hover:text-white transition-colors" href="/Urun">Koleksiyonlar</a></li>
                        <li><a class="hover:text-white transition-colors" href="/Sozlesmeler/Gizlilik">Gizlilik Politikası</a></li>
                        <li><a class="hover:text-white transition-colors" href="/Sozlesmeler/MesafeliSatis">Mesafeli Satış Sözleşmesi</a></li>
                    </ul>
                </div>'''

new_footer = '''                <!-- Footer Links & Socials -->
                <div class="flex flex-col md:items-end">
                    <h4 class="font-bold text-sm tracking-widest mb-4 uppercase text-[#c6ca99]">KURUMSAL</h4>
                    <ul class="space-y-2 text-sm font-light text-gray-300 text-left md:text-right">
                        <li><a class="hover:text-white transition-colors" href="/Kurumsal/Hakkimizda">Hakkımızda</a></li>
                        <li><a class="hover:text-white transition-colors" href="/Kurumsal/Iletisim">İletişim</a></li>
                        <li><a class="hover:text-white transition-colors" href="/Urun">Koleksiyonlar</a></li>
                        <li><a class="hover:text-white transition-colors" href="/Sozlesmeler/Gizlilik">Gizlilik Politikası</a></li>
                        <li><a class="hover:text-white transition-colors" href="/Sozlesmeler/MesafeliSatis">Mesafeli Satış Sözleşmesi</a></li>
                    </ul>
                    <div class="mt-6 flex gap-4 text-gray-400">
                        @if(!string.IsNullOrEmpty(siteSettings.InstagramUrl)) {
                            <a href="@siteSettings.InstagramUrl" target="_blank" class="hover:text-white transition-colors"><i class="fab fa-instagram text-xl"></i></a>
                        }
                        @if(!string.IsNullOrEmpty(siteSettings.FacebookUrl)) {
                            <a href="@siteSettings.FacebookUrl" target="_blank" class="hover:text-white transition-colors"><i class="fab fa-facebook text-xl"></i></a>
                        }
                        @if(!string.IsNullOrEmpty(siteSettings.WhatsappNumarasi)) {
                            <a href="https://wa.me/@siteSettings.WhatsappNumarasi.Replace(" ", "").Replace("+", "")" target="_blank" class="hover:text-white transition-colors"><i class="fab fa-whatsapp text-xl"></i></a>
                        }
                        @if(!string.IsNullOrEmpty(siteSettings.YoutubeUrl)) {
                            <a href="@siteSettings.YoutubeUrl" target="_blank" class="hover:text-white transition-colors"><i class="fab fa-youtube text-xl"></i></a>
                        }
                    </div>
                </div>'''
content = content.replace(old_footer, new_footer)

with open(r'e:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Shared\_Layout.cshtml', 'w', encoding='utf-8') as f:
    f.write(content)

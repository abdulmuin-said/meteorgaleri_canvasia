import re

with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Areas\Admin\Views\Shared\_AdminLayout.cshtml', 'r', encoding='utf-8') as f:
    content = f.read()

# Font change
old_font = '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">'
new_font = '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>'
content = content.replace(old_font, new_font)

# Menu change
menu_pattern = re.compile(r'<ul class="ca-menu">.*?</ul>', re.DOTALL)
new_menu = """<ul class="ca-menu">
                @if (canViewDashboard)
                {
                    <li class="ca-menu-label">GENEL</li>
                    <li class="ca-menu-item @(currentController == "Home" ? "active" : "")">
                        <a href="/Admin/Home">
                            <i class="fas fa-th-large"></i> Panel
                        </a>
                    </li>
                }

                @if (canManageOrders || canManageProducts)
                {
                    <li class="ca-menu-label">E-TİCARET YÖNETİMİ</li>
                }

                @if (canManageOrders)
                {
                    <li class="ca-menu-item @(currentController == "Siparis" ? "active" : "")">
                        <a href="/Admin/Siparis">
                            <i class="fas fa-shopping-basket"></i>
                            <span>Siparişler</span>
                            @if (ViewBag.BekleyenSiparis != null && (int)ViewBag.BekleyenSiparis > 0)
                            {
                                <span class="ca-menu-badge badge bg-danger rounded-pill">@ViewBag.BekleyenSiparis</span>
                            }
                        </a>
                    </li>
                    <li class="ca-menu-item @(currentController == "Iade" ? "active" : "")">
                        <a href="/Admin/Iade">
                            <i class="fas fa-undo-alt"></i> İade Talepleri
                        </a>
                    </li>
                }

                @if (canManageProducts)
                {
                    <li class="ca-menu-item @(currentController == "Urun" ? "active" : "")">
                        <a href="/Admin/Urun">
                            <i class="fas fa-box-open"></i> Ürünler
                        </a>
                    </li>
                    <li class="ca-menu-item @(currentController == "Kategori" ? "active" : "")">
                        <a href="/Admin/Kategori">
                            <i class="fas fa-layer-group"></i> Kategoriler
                        </a>
                    </li>
                }

                @if (canManageContent)
                {
                    <li class="ca-menu-label">GÖRÜNÜM & İÇERİK</li>
                    <li class="ca-menu-item @(currentController == "AnaSayfa" ? "active" : "")">
                        <a href="/Admin/AnaSayfa">
                            <i class="fas fa-images"></i> Ana Sayfa Slider
                        </a>
                    </li>
                    <li class="ca-menu-item @(currentController == "Sayfa" ? "active" : "")">
                        <a href="/Admin/Sayfa">
                            <i class="fas fa-file-contract"></i> Kurumsal Sayfalar
                        </a>
                    </li>
                    <li class="ca-menu-item @(currentController == "Kupon" ? "active" : "")">
                        <a href="/Admin/Kupon">
                            <i class="fas fa-tags"></i> Kuponlar
                        </a>
                    </li>
                }

                @if (canManageUsers || canManageContent)
                {
                    <li class="ca-menu-label">MÜŞTERİ İLİŞKİLERİ</li>
                }

                @if (canManageContent)
                {
                    <li class="ca-menu-item @(currentController == "Iletisim" ? "active" : "")">
                        <a href="/Admin/Iletisim">
                            <i class="fas fa-inbox"></i>
                            <span>Mesajlar</span>
                            @if (ViewBag.OkunmamisIletisim != null && (int)ViewBag.OkunmamisIletisim > 0)
                            {
                                <span class="ca-menu-badge badge bg-warning rounded-pill">@ViewBag.OkunmamisIletisim</span>
                            }
                        </a>
                    </li>
                    <li class="ca-menu-item @(currentController == "Yorum" ? "active" : "")">
                        <a href="/Admin/Yorum">
                            <i class="fas fa-comments"></i> Ürün Yorumları
                        </a>
                    </li>
                    <li class="ca-menu-item @(currentController == "Bulten" ? "active" : "")">
                        <a href="/Admin/Bulten">
                            <i class="fas fa-envelope-open-text"></i> Bülten Aboneleri
                        </a>
                    </li>
                }

                @if (canManageUsers)
                {
                    <li class="ca-menu-item @(currentController == "Kullanici" ? "active" : "")">
                        <a href="/Admin/Kullanici">
                            <i class="fas fa-users"></i> Üyeler
                        </a>
                    </li>
                }

                @if (canManageSettings)
                {
                    <li class="ca-menu-label">SİSTEM</li>
                    <li class="ca-menu-item @(currentController == "Ayarlar" ? "active" : "")">
                        <a href="/Admin/Ayarlar">
                            <i class="fas fa-cog"></i> Mağaza Ayarları
                        </a>
                    </li>
                }
            </ul>"""

content = menu_pattern.sub(new_menu, content, count=1)

with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Areas\Admin\Views\Shared\_AdminLayout.cshtml', 'w', encoding='utf-8') as f:
    f.write(content)
print('Admin menu basariyla guncellendi!')

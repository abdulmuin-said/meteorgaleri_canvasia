import re

with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Areas\Admin\Views\AnaSayfa\Index.cshtml', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Hero slider block
pattern = re.compile(r'<div class="col-12">\s*<div class="ca-card">\s*<div class="ca-form-header">.*?<div class="col-12">\s*<div class="ca-card">\s*<div class="ca-form-header" style="background:linear-gradient\(135deg,#2563eb,#1d4ed8\);">', re.DOTALL)

new_hero = """<div class="col-12">
                <div class="ca-card">
                    <div class="ca-form-header">
                        <div class="d-flex align-items-center position-relative" style="z-index:2;">
                            <div class="bg-white bg-opacity-25 rounded-3 p-3 me-3">
                                <i class="fas fa-images fa-2x"></i>
                            </div>
                            <div>
                                <h4 class="mb-1 fw-bold">Ana Sayfa Slider</h4>
                                <p class="mb-0 small" style="opacity:.7;">Slider gorselleri, butonlar ve yazilar.</p>
                            </div>
                        </div>
                        <i class="fas fa-photo-video ca-form-header-icon"></i>
                    </div>
                    <div class="ca-card-body">
                        <div class="row g-4">
                            <div class="col-md-12">
                                <div class="ca-form-group">
                                    <label class="ca-label">Slider Aktif</label>
                                    <div class="form-check form-switch mt-2">
                                        <input asp-for="Hero.Enabled" class="form-check-input" />
                                    </div>
                                </div>
                            </div>

                            @for (var i = 0; i < Model.Hero.DesktopSlides.Count; i++)
                            {
                                <div class="col-12 mt-5">
                                    <h5 class="fw-bold border-bottom pb-2" style="color:var(--ca-primary);">Slider @(i + 1) Ayarlari</h5>
                                    <input type="hidden" asp-for="Hero.DesktopSlides[i].Id" />
                                    <input type="hidden" asp-for="Hero.DesktopSlides[i].SortOrder" value="@i" />
                                </div>
                                <div class="col-md-6">
                                    <div class="ca-form-group">
                                        <label class="ca-label">Gorsel URL (1920x900px) (veya yerel path örn: /images/slider/1.jpg)</label>
                                        <input asp-for="Hero.DesktopSlides[i].ImageUrl" class="ca-input" />
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="ca-form-group">
                                        <label class="ca-label">Ana Baslik (Buyuk Metin)</label>
                                        <input asp-for="Hero.DesktopSlides[i].Title" class="ca-input" />
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="ca-form-group">
                                        <label class="ca-label">Kucuk Ust Baslik</label>
                                        <input asp-for="Hero.DesktopSlides[i].Subtitle" class="ca-input" />
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="ca-form-group">
                                        <label class="ca-label">Aciklama Metni</label>
                                        <input asp-for="Hero.DesktopSlides[i].Description" class="ca-input" />
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="ca-form-group">
                                        <label class="ca-label">Buton Yazisi</label>
                                        <input asp-for="Hero.DesktopSlides[i].ButtonText" class="ca-input" />
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="ca-form-group">
                                        <label class="ca-label">Buton Linki (örn: /Urun)</label>
                                        <input asp-for="Hero.DesktopSlides[i].ButtonUrl" class="ca-input" />
                                    </div>
                                </div>
                            }
                        </div>
                    </div>
                </div>
            </div>

            @await Html.PartialAsync("_SimpleBlockEditor", ("Kategori Alani", "Kategoriler", Model.Categories))
            @await Html.PartialAsync("_ProductBlockEditor", ("Öne Çıkan Ürünler", "FeaturedProducts", Model.FeaturedProducts))
            @await Html.PartialAsync("_ProductBlockEditor", ("En Cok Satanlar", "BestSellers", Model.BestSellers))
            @await Html.PartialAsync("_ProductBlockEditor", ("Fırsat Ürünleri", "Deals", Model.Deals))

            <div class="col-12">
                <div class="ca-card">
                    <div class="ca-form-header" style="background:linear-gradient(135deg,#2563eb,#1d4ed8);">"""

content = pattern.sub(new_hero, content, count=1)

with open(r'E:\Projeler\MeteorGaleri\KanvasProje.Web\Areas\Admin\Views\AnaSayfa\Index.cshtml', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')

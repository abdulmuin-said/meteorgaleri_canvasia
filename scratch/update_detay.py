import re

file_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Urun\Detay.cshtml"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the start and end tokens
start_token = "<!-- Mobile Lightbox -->"
end_token = "<!-- Desktop Lightbox Modal -->" # Replace up to here, and also the modals.

# Actually, the best way is to replace everything from `<!-- Mobile Lightbox -->` up to `<script>`
script_token = "<script>"
start_idx = content.find(start_token)
end_idx = content.find(script_token)

if start_idx == -1 or end_idx == -1:
    print("Tokens not found.")
    exit()

new_html = """<!-- Mobile Lightbox -->
<div id="mobileLightbox" class="fixed inset-0 z-50 hidden bg-black bg-opacity-95 items-center justify-center">
    <button class="absolute top-4 right-4 text-white p-2" onclick="closeMobileLightbox()">
        <i class="fas fa-times text-2xl"></i>
    </button>
    <div class="w-full h-full flex items-center justify-center overflow-hidden" id="lightboxImgContainer">
        <img id="mobileLightboxImage" class="max-w-full max-h-full object-contain" src="" alt="">
    </div>
    <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex items-center gap-4 bg-black bg-opacity-50 text-white rounded-full px-4 py-2">
        <button onclick="zoomOutMobile()"><i class="fas fa-search-minus"></i></button>
        <span id="zoomLevel" class="text-sm">100%</span>
        <button onclick="zoomInMobile()"><i class="fas fa-search-plus"></i></button>
    </div>
</div>

<!-- Desktop Lightbox Modal -->
<div class="fixed inset-0 z-50 hidden bg-black bg-opacity-95 items-center justify-center" id="desktopLightboxModal">
    <button class="absolute top-4 right-4 text-white p-2" id="closeDesktopModalBtn">
        <i class="fas fa-times text-2xl"></i>
    </button>
    <div class="absolute top-4 left-1/2 transform -translate-x-1/2 flex items-center gap-4 bg-black bg-opacity-50 text-white rounded-full px-4 py-2">
        <button onclick="resetDesktopZoom()"><i class="fas fa-redo"></i></button>
        <button onclick="zoomOutDesktop()"><i class="fas fa-search-minus"></i></button>
        <button onclick="zoomInDesktop()"><i class="fas fa-search-plus"></i></button>
    </div>
    <div class="w-full h-full flex items-center justify-center overflow-hidden">
        <img id="desktopLightboxImage" src="@varsayilanGaleriGorseli" class="max-w-full max-h-full object-contain transition-transform duration-200" alt="@varsayilanGaleriAltMetni">
    </div>
</div>

<!-- Yorum Yapma Modal -->
<div class="fixed inset-0 z-50 hidden bg-black bg-opacity-50 items-center justify-center" id="commentModal">
    <div class="bg-white rounded-lg w-full max-w-md p-6 relative">
        <button class="absolute top-4 right-4 text-gray-400 hover:text-black" id="closeCommentModalBtn"><i class="fas fa-times"></i></button>
        <h5 class="font-serif text-2xl text-[#313511] mb-6">Ürünü Değerlendir</h5>
        <form action="/Urun/YorumYap" method="post">
            @Html.AntiForgeryToken()
            <input type="hidden" name="UrunId" value="@Model.Id" />
            
            <div class="flex flex-row-reverse justify-center gap-2 mb-6">
                <input type="radio" id="star5" name="Puan" value="5" class="hidden peer/5" />
                <label for="star5" class="text-gray-300 peer-checked/5:text-[#b58735] hover:text-[#b58735] cursor-pointer text-2xl transition-colors"><i class="fas fa-star"></i></label>
                
                <input type="radio" id="star4" name="Puan" value="4" class="hidden peer/4" />
                <label for="star4" class="text-gray-300 peer-checked/4:text-[#b58735] hover:text-[#b58735] cursor-pointer text-2xl transition-colors"><i class="fas fa-star"></i></label>
                
                <input type="radio" id="star3" name="Puan" value="3" class="hidden peer/3" />
                <label for="star3" class="text-gray-300 peer-checked/3:text-[#b58735] hover:text-[#b58735] cursor-pointer text-2xl transition-colors"><i class="fas fa-star"></i></label>
                
                <input type="radio" id="star2" name="Puan" value="2" class="hidden peer/2" />
                <label for="star2" class="text-gray-300 peer-checked/2:text-[#b58735] hover:text-[#b58735] cursor-pointer text-2xl transition-colors"><i class="fas fa-star"></i></label>
                
                <input type="radio" id="star1" name="Puan" value="1" class="hidden peer/1" checked />
                <label for="star1" class="text-gray-300 peer-checked/1:text-[#b58735] hover:text-[#b58735] cursor-pointer text-2xl transition-colors"><i class="fas fa-star"></i></label>
            </div>

            @if (User.Identity?.IsAuthenticated != true)
            {
                <div class="mb-4">
                    <label class="block text-xs uppercase tracking-widest text-[#1c1c18] font-medium mb-1.5">Adınız Soyadınız</label>
                    <input type="text" name="AdSoyad" class="w-full border border-[#e5e2dc] rounded px-4 py-2 text-sm focus:ring-[#b58735] focus:border-[#b58735]" required>
                </div>
            }

            <div class="mb-6">
                <label class="block text-xs uppercase tracking-widest text-[#1c1c18] font-medium mb-1.5">Yorumunuz</label>
                <textarea name="YorumMetni" class="w-full border border-[#e5e2dc] rounded px-4 py-2 text-sm focus:ring-[#b58735] focus:border-[#b58735]" rows="4" required></textarea>
            </div>

            <button type="submit" class="w-full bg-[#313511] text-white text-xs tracking-widest uppercase py-3 rounded hover:bg-[#1c2001] transition-colors">Yorumu Gönder</button>
        </form>
    </div>
</div>

<!-- Breadcrumb -->
<div class="bg-[#f1ede7] border-b border-[#e5e2dc] py-3">
    <div class="container mx-auto px-4 flex items-center gap-2 text-xs text-[#47473d]">
        <a href="/" class="hover:text-[#313511] transition-colors">Ana Sayfa</a>
        <span>/</span>
        <a href="/Urun" class="hover:text-[#313511] transition-colors">Koleksiyon</a>
        <span>/</span>
        <span class="text-[#1c1c18] font-medium">@Model.Baslik</span>
    </div>
</div>

<div class="container mx-auto px-4 py-12">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16">
        
        <!-- Left: Image Gallery -->
        <div class="space-y-4">
            <div class="relative bg-[#f1ede7] aspect-square rounded-lg overflow-hidden group cursor-zoom-in" onclick="openProductLightbox()">
                <img id="mainProductImage" src="@varsayilanGaleriGorseli" data-default-src="@(varsayilanMedya?.ResimYolu ?? Model.AnaGorselUrl)" data-default-alt="@varsayilanGaleriAltMetni" data-product-name="@Model.Baslik" class="w-full h-full object-contain transition-transform duration-500 group-hover:scale-105" alt="@varsayilanGaleriAltMetni">
                <div class="absolute bottom-4 right-4 bg-white/80 backdrop-blur-sm p-2 rounded-full shadow-sm text-[#313511]">
                    <i class="fas fa-search-plus"></i>
                </div>
            </div>
            
            @if (galeriMedyalari.Any())
            {
                <div class="flex gap-3 overflow-x-auto pb-2 custom-scrollbar">
                    @foreach (var resim in galeriMedyalari)
                    {
                        var altMetin = string.IsNullOrWhiteSpace(resim.AltMetin) ? Model.Baslik : resim.AltMetin;
                        <button type="button" class="thumbnail-item flex-shrink-0 w-20 h-20 md:w-24 md:h-24 rounded border-2 @(string.Equals(resim.ResimYolu, varsayilanGaleriGorseli, StringComparison.OrdinalIgnoreCase) ? "border-[#313511]" : "border-transparent") overflow-hidden transition-colors bg-[#fcf9f3]" data-image="@resim.ResimYolu" data-alt="@altMetin" onclick="changeProductImage(this.dataset.image, this, this.dataset.alt)">
                            <img src="@resim.EtkinPosterYolu" class="w-full h-full object-cover" alt="@altMetin" loading="lazy">
                        </button>
                    }
                </div>
            }
        </div>

        <!-- Right: Product Info -->
        <div class="flex flex-col">
            <h1 class="font-serif text-3xl md:text-4xl lg:text-5xl text-[#313511] mb-4">@Model.Baslik</h1>
            
            <div class="flex items-center gap-4 mb-6">
                <div class="flex text-[#b58735] text-sm">
                    @for (int i = 1; i <= 5; i++)
                    {
                        if (i <= tamYildiz) { <i class="fas fa-star"></i> }
                        else if (i == tamYildiz + 1 && yarimYildiz) { <i class="fas fa-star-half-alt"></i> }
                        else { <i class="far fa-star"></i> }
                    }
                </div>
                <span class="text-xs text-[#47473d]">(@yorumSayisi değerlendirme)</span>
            </div>

            <div class="flex items-end gap-4 mb-6">
                <span id="priceDisplay" class="font-serif text-3xl text-[#1c1c18]">@currencySymbol @gosterilecekFiyat.ToString("N2")</span>
                @if (gosterilecekEskiFiyat.HasValue)
                {
                    <span id="oldPriceDisplay" class="text-lg text-[#47473d] line-through mb-1">@currencySymbol @gosterilecekEskiFiyat.Value.ToString("N2")</span>
                }
                else
                {
                    <span id="oldPriceDisplay" class="text-lg text-[#47473d] line-through mb-1 hidden"></span>
                }
                @if (gosterilecekIndirimYuzdesi.HasValue)
                {
                    <span id="discountBadge" class="bg-[#b58735] text-white text-xs px-2 py-1 rounded mb-1">%@gosterilecekIndirimYuzdesi.Value İndirim</span>
                }
                else
                {
                    <span id="discountBadge" class="bg-[#b58735] text-white text-xs px-2 py-1 rounded mb-1 hidden"></span>
                }
            </div>

            <div class="flex flex-wrap items-center gap-y-2 gap-x-4 text-xs text-[#47473d] mb-6 border-y border-[#e5e2dc] py-4">
                <span id="stockStatusText" class="flex items-center gap-1.5"><i class="fas fa-box"></i>@stokDurumuMetni</span>
                @if (!string.IsNullOrWhiteSpace(Model.Marka)) { <span class="flex items-center gap-1.5"><i class="fas fa-tag"></i>@Model.Marka</span> }
                @if (!string.IsNullOrWhiteSpace(Model.SKU)) { <span class="flex items-center gap-1.5"><i class="fas fa-barcode"></i>@Model.SKU</span> }
                @if (Model.KargoyaVerilisSuresiGun > 0) { <span class="flex items-center gap-1.5"><i class="fas fa-truck"></i>@Model.KargoyaVerilisSuresiGun gün içinde kargo</span> }
            </div>

            <div id="variantSummaryText" class="text-sm text-[#47473d] mb-6 @(string.IsNullOrWhiteSpace(seciliVaryantMetni) ? "hidden" : "")">
                <i class="fas fa-layer-group mr-1.5"></i>@seciliVaryantMetni
            </div>

            @if (!string.IsNullOrWhiteSpace(Model.KisaAciklama))
            {
                <p class="text-sm text-[#47473d] mb-8 leading-relaxed">@Model.KisaAciklama</p>
            }

            @if (secenekler.Any())
            {
                <div class="mb-8">
                    <label class="block text-xs uppercase tracking-widest text-[#1c1c18] font-medium mb-3">Ebat Seçiniz</label>
                    <div class="grid grid-cols-2 gap-3">
                        @foreach (var varyant in secenekler)
                        {
                            var varyantSatinAlinabilir = varyant.SatinAlinabilirMi;
                            var varyantOldPrice = Model.Fiyat > varyant.SatisFiyati ? Model.Fiyat : 0;
                            var varyantMedyaUrl = !string.IsNullOrWhiteSpace(varyant.GorselUrl) ? varyant.GorselUrl : (varyantMedyaHaritasi.TryGetValue(varyant.Id, out var eslesen) ? eslesen : string.Empty);
                            var stokMesaji = varyant.StokAdedi > 0 ? $"{varyant.StokAdedi} adet" : (varyant.OnSipariseAcikMi ? "Ön sipariş" : "Tükendi");
                            
                            <label class="relative border rounded p-3 cursor-pointer transition-colors hover:border-[#b58735] has-[:checked]:border-[#313511] has-[:checked]:bg-[#f1ede7] @(!varyantSatinAlinabilir ? "opacity-50 cursor-not-allowed" : "")">
                                <input type="radio" id="variant-@varyant.Id" name="productVariant" value="@varyant.Id" class="variant-radio absolute opacity-0 w-0 h-0" @(varyant.Id == varsayilanSecenek?.Id ? "checked" : "") disabled="@(!varyantSatinAlinabilir)" data-price="@varyant.SatisFiyati" data-oldprice="@(varyantOldPrice > 0 ? varyantOldPrice.ToString(System.Globalization.CultureInfo.InvariantCulture) : string.Empty)" data-stock="@varyant.StokAdedi" data-preorder="@varyant.OnSipariseAcikMi.ToString().ToLowerInvariant()" data-image="@varyantMedyaUrl" data-label="@varyant.VaryantBasligi">
                                <div class="flex justify-between items-start">
                                    <div class="flex flex-col">
                                        <span class="text-sm font-semibold text-[#1c1c18]">@(string.IsNullOrWhiteSpace(varyant.VaryantBasligi) ? varyant.Olcu : varyant.VaryantBasligi)</span>
                                        <span class="text-xs text-[#47473d] mt-1">@currencySymbol @varyant.SatisFiyati.ToString("N2")</span>
                                    </div>
                                    <span class="text-[10px] uppercase tracking-wider @(varyantSatinAlinabilir ? "text-[#b58735]" : "text-red-500")">@stokMesaji</span>
                                </div>
                            </label>
                        }
                    </div>
                </div>
            }

            @if (stoktaVar)
            {
                <div class="flex items-end gap-4 mb-8">
                    <div>
                        <label class="block text-xs uppercase tracking-widest text-[#1c1c18] font-medium mb-3">Adet</label>
                        <div class="flex items-center border border-[#e5e2dc] rounded bg-white">
                            <button type="button" class="w-10 h-12 flex items-center justify-center text-[#47473d] hover:bg-[#f1ede7] transition-colors" onclick="decreaseQuantity()">-</button>
                            <input type="number" id="productQuantity" class="w-12 h-12 text-center text-sm border-none bg-transparent p-0 focus:ring-0 text-[#1c1c18] font-semibold" value="@minSiparisAdedi" min="@minSiparisAdedi" max="@maxSiparisAdedi" readonly>
                            <button type="button" class="w-10 h-12 flex items-center justify-center text-[#47473d] hover:bg-[#f1ede7] transition-colors" onclick="increaseQuantity()">+</button>
                        </div>
                    </div>
                    
                    <form id="addToCartForm" method="post" action="/Sepet/Ekle" class="flex-1">
                        @Html.AntiForgeryToken()
                        <input type="hidden" name="UrunId" value="@Model.Id" />
                        <input type="hidden" id="selectedVariantId" name="SecenekId" value="@varsayilanSecenek?.Id" />
                        <input type="hidden" id="selectedQuantity" name="Adet" value="@minSiparisAdedi" />

                        <button type="button" id="ajaxSepetBtn" class="w-full h-12 bg-[#313511] text-white text-xs uppercase tracking-widest rounded hover:bg-[#1c2001] transition-colors flex items-center justify-center gap-2">
                            <i class="fas fa-shopping-bag"></i> Sepete Ekle
                        </button>
                    </form>
                </div>
            }
            else
            {
                <div class="bg-amber-50 border border-amber-200 text-amber-700 p-4 rounded text-sm mb-8">
                    Bu ürün şu anda satın almaya uygun değil. Stok bilgisi güncellendiğinde tekrar deneyin.
                </div>
            }

            <div class="grid grid-cols-3 gap-2 py-4 border-y border-[#e5e2dc]">
                <div class="text-center">
                    <i class="fas fa-shield-alt text-[#b58735] mb-2 text-lg"></i>
                    <p class="text-xs text-[#1c1c18] font-semibold mb-1">Güvenli Ödeme</p>
                    <p class="text-[10px] text-[#47473d]">256-bit SSL</p>
                </div>
                <div class="text-center">
                    <i class="fas fa-truck text-[#b58735] mb-2 text-lg"></i>
                    <p class="text-xs text-[#1c1c18] font-semibold mb-1">Ücretsiz Kargo</p>
                    <p class="text-[10px] text-[#47473d]">Hızlı Teslimat</p>
                </div>
                <div class="text-center">
                    <i class="fas fa-undo-alt text-[#b58735] mb-2 text-lg"></i>
                    <p class="text-xs text-[#1c1c18] font-semibold mb-1">İade Garantisi</p>
                    <p class="text-[10px] text-[#47473d]">14 Gün İçinde</p>
                </div>
            </div>
            
        </div>
    </div>

    <!-- Tabs Section -->
    <div class="mt-20 border-t border-[#e5e2dc] pt-12">
        <div class="flex flex-col lg:flex-row gap-12">
            
            <!-- Left: Description and Specs -->
            <div class="lg:w-2/3 space-y-12">
                <div>
                    <h2 class="font-serif text-2xl text-[#313511] mb-6 flex items-center gap-3">
                        <i class="fas fa-file-alt text-[#b58735]"></i> Ürün Açıklaması
                    </h2>
                    <div class="prose prose-sm max-w-none text-[#47473d] leading-relaxed">
                        @Html.Raw(Model.Aciklama ?? "Bu ürün için açıklama girilmemiştir.")
                    </div>
                </div>

                @if (teknikTabloSatirlari.Any())
                {
                    <div>
                        <h2 class="font-serif text-2xl text-[#313511] mb-6 flex items-center gap-3">
                            <i class="fas fa-cogs text-[#b58735]"></i> Teknik Özellikler
                        </h2>
                        <div class="bg-white border border-[#e5e2dc] rounded-lg overflow-hidden">
                            <table class="w-full text-sm text-left">
                                <tbody class="divide-y divide-[#e5e2dc]">
                                    @foreach (var satir in teknikTabloSatirlari)
                                    {
                                        <tr class="hover:bg-[#fcf9f3]">
                                            <th class="px-6 py-4 font-semibold text-[#1c1c18] w-1/3 bg-[#f1ede7]">@satir.Baslik</th>
                                            <td class="px-6 py-4 text-[#47473d]">@satir.Deger</td>
                                        </tr>
                                    }
                                </tbody>
                            </table>
                        </div>
                    </div>
                }
                
                @if (medyaVitriniVar)
                {
                    <div>
                        <h2 class="font-serif text-2xl text-[#313511] mb-6 flex items-center gap-3">
                            <i class="fas fa-photo-video text-[#b58735]"></i> Medya & Galeriler
                        </h2>
                        
                        @if (videoMedyalari.Any())
                        {
                            <div class="mb-8">
                                <h3 class="text-lg font-semibold text-[#1c1c18] mb-4">Video Anlatımı</h3>
                                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    @foreach (var medya in videoMedyalari)
                                    {
                                        <div class="bg-white border border-[#e5e2dc] rounded-lg overflow-hidden">
                                            <div class="aspect-video bg-black relative">
                                                @if (!string.IsNullOrWhiteSpace(ProductMediaEmbedHelper.GetEmbedUrl(medya.EtkinKaynak)))
                                                {
                                                    <iframe src="@ProductMediaEmbedHelper.GetEmbedUrl(medya.EtkinKaynak)" class="w-full h-full" title="@medya.Baslik" allowfullscreen></iframe>
                                                }
                                                else
                                                {
                                                    <video controls class="w-full h-full object-cover" poster="@medya.EtkinPosterYolu">
                                                        <source src="@(string.IsNullOrWhiteSpace(medya.VideoUrl) ? medya.ResimYolu : medya.VideoUrl)" type="video/mp4" />
                                                    </video>
                                                }
                                            </div>
                                            <div class="p-4">
                                                <h5 class="text-sm font-semibold text-[#1c1c18] mb-1">@medya.Baslik</h5>
                                                <p class="text-xs text-[#47473d]">@UrunMedyaCatalog.GetAreaLabel(medya.MedyaAlani)</p>
                                            </div>
                                        </div>
                                    }
                                </div>
                            </div>
                        }

                        @if (mockupGruplari.Any())
                        {
                            @foreach (var grup in mockupGruplari)
                            {
                                <div class="mb-8">
                                    <h3 class="text-lg font-semibold text-[#1c1c18] mb-4">@UrunMedyaCatalog.GetAreaLabel(grup.Key)</h3>
                                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                                        @foreach (var medya in grup)
                                        {
                                            <div class="rounded-lg overflow-hidden border border-[#e5e2dc] aspect-square">
                                                <img src="@medya.EtkinKaynak" alt="@medya.AltMetin" class="w-full h-full object-cover" loading="lazy" />
                                            </div>
                                        }
                                    </div>
                                </div>
                            }
                        }
                    </div>
                }
            </div>

            <!-- Right: Reviews -->
            <div class="lg:w-1/3">
                <h2 class="font-serif text-2xl text-[#313511] mb-6 flex items-center gap-3">
                    <i class="fas fa-comments text-[#b58735]"></i> Yorumlar
                </h2>
                
                @if (yorumlar != null && yorumlar.Count > 0)
                {
                    <div class="bg-white border border-[#e5e2dc] rounded-lg p-6 text-center mb-8">
                        <h3 class="font-serif text-5xl text-[#313511] mb-2">@ortalamaPuan.ToString("0.0")</h3>
                        <div class="text-[#b58735] mb-2">
                            @for (int i = 1; i <= 5; i++)
                            {
                                if (i <= tamYildiz) { <i class="fas fa-star"></i> }
                                else if (i == tamYildiz + 1 && yarimYildiz) { <i class="fas fa-star-half-alt"></i> }
                                else { <i class="far fa-star"></i> }
                            }
                        </div>
                        <p class="text-sm text-[#47473d] mb-4">Toplam @yorumSayisi değerlendirme</p>
                        <button class="w-full border border-[#313511] text-[#313511] text-xs tracking-widest uppercase py-2.5 rounded hover:bg-[#313511] hover:text-white transition-colors" id="openCommentModalBtn">
                            Yorum Yap
                        </button>
                    </div>

                    <div class="space-y-4">
                        @foreach (var yorum in yorumlar.Take(3))
                        {
                            <div class="bg-white border border-[#e5e2dc] rounded-lg p-4">
                                <div class="flex items-start justify-between mb-2">
                                    <div class="flex items-center gap-3">
                                        <div class="w-10 h-10 rounded-full bg-[#f1ede7] text-[#313511] flex items-center justify-center font-semibold text-sm">
                                            @{
                                                var names = yorum.AdSoyad.Split(' ');
                                                string initials = "";
                                                if (names.Length > 0) { initials += names[0][0]; }
                                                if (names.Length > 1) { initials += names[names.Length - 1][0]; }
                                                else if (names[0].Length > 1) { initials += names[0][1]; }
                                            }
                                            @initials
                                        </div>
                                        <div>
                                            <h5 class="text-sm font-semibold text-[#1c1c18]">@yorum.AdSoyad</h5>
                                            <div class="text-[#b58735] text-[10px]">
                                                @for (int i = 0; i < yorum.Puan; i++) { <i class="fas fa-star"></i> }
                                            </div>
                                        </div>
                                    </div>
                                    <span class="text-[10px] text-[#47473d]">@yorum.OlusturulmaTarihi.ToString("dd MMM yyyy")</span>
                                </div>
                                <p class="text-sm text-[#47473d] mt-2">@yorum.YorumMetni</p>
                            </div>
                        }
                    </div>
                }
                else
                {
                    <div class="text-center py-12 bg-white border border-[#e5e2dc] rounded-lg">
                        <i class="far fa-comments fa-3x text-[#e5e2dc] mb-4"></i>
                        <h5 class="text-[#313511] font-semibold mb-2">Henüz yorum yapılmamış</h5>
                        <p class="text-sm text-[#47473d] mb-6">Bu ürün için ilk yorumu siz yapın!</p>
                        <button class="bg-[#313511] text-white text-xs tracking-widest uppercase px-6 py-2.5 rounded hover:bg-[#1c2001] transition-colors" id="openCommentModalBtnEmpty">
                            İlk Yorumu Yap
                        </button>
                    </div>
                }
            </div>
        </div>
    </div>
</div>
"""

new_content = content[:start_idx] + new_html + "\n" + content[end_idx:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done")

import re

def build_detay():
    # 1. Read the header
    with open(r"E:\Projeler\MeteorGaleri\scratch\header.txt", "r", encoding="utf-8") as f:
        header = f.read()

    # 2. Extract new_html from update_detay.py
    with open(r"E:\Projeler\MeteorGaleri\scratch\update_detay.py", "r", encoding="utf-8") as f:
        update_detay = f.read()
    
    # We need to extract the string assigned to new_html
    start_str = 'new_html = """<!-- Mobile Lightbox -->'
    end_str = '"""\n\nnew_content ='
    
    s_idx = update_detay.find(start_str)
    e_idx = update_detay.find(end_str)
    
    new_html = update_detay[s_idx + len('new_html = """'):e_idx]

    # Apply fixes to new_html (from update_detay_fixes.py)
    old_price = """<span id="priceDisplay" class="font-serif text-3xl text-[#1c1c18]">@currencySymbol @gosterilecekFiyat.ToString("N2")</span>"""
    new_price = """<span id="priceDisplay" class="font-sans text-2xl font-medium tracking-tight text-[#1c1c18]">@gosterilecekFiyat.ToString("N2") @currencySymbol</span>"""
    new_html = new_html.replace(old_price, new_price)

    old_old_price = """<span id="oldPriceDisplay" class="text-lg text-[#47473d] line-through mb-1">@currencySymbol @gosterilecekEskiFiyat.Value.ToString("N2")</span>"""
    new_old_price = """<span id="oldPriceDisplay" class="text-lg text-[#47473d] line-through mb-1 font-sans">@gosterilecekEskiFiyat.Value.ToString("N2") @currencySymbol</span>"""
    new_html = new_html.replace(old_old_price, new_old_price)

    old_meta = """            <div class="flex flex-wrap items-center gap-y-2 gap-x-4 text-xs text-[#47473d] mb-6 border-y border-[#e5e2dc] py-4">
                <span id="stockStatusText" class="flex items-center gap-1.5"><i class="fas fa-box"></i>@stokDurumuMetni</span>
                @if (!string.IsNullOrWhiteSpace(Model.Marka)) { <span class="flex items-center gap-1.5"><i class="fas fa-tag"></i>@Model.Marka</span> }
                @if (!string.IsNullOrWhiteSpace(Model.SKU)) { <span class="flex items-center gap-1.5"><i class="fas fa-barcode"></i>@Model.SKU</span> }
                @if (Model.KargoyaVerilisSuresiGun > 0) { <span class="flex items-center gap-1.5"><i class="fas fa-truck"></i>@Model.KargoyaVerilisSuresiGun gün içinde kargo</span> }
            </div>"""

    new_meta = """            <div class="flex flex-wrap items-center gap-y-2 gap-x-6 text-xs text-[#47473d] mb-6 border-y border-[#e5e2dc] py-4">
                <span id="stockStatusText" class="flex items-center gap-2"><i class="fas fa-check-circle text-green-600"></i> Stokta</span>
                @if (Model.KargoyaVerilisSuresiGun > 0) { <span class="flex items-center gap-2"><i class="fas fa-truck text-[#a09e99]"></i> @Model.KargoyaVerilisSuresiGun gün içinde kargo</span> }
            </div>"""
    new_html = new_html.replace(old_meta, new_meta)

    old_variants = """                <div class="mb-8">
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
                </div>"""

    new_variants = """                <div class="mb-8">
                    <label class="block text-xs uppercase tracking-widest text-[#1c1c18] font-medium mb-3">Ebat Seçiniz</label>
                    <div class="flex flex-wrap gap-2">
                        @foreach (var varyant in secenekler)
                        {
                            var varyantSatinAlinabilir = varyant.SatinAlinabilirMi;
                            var varyantOldPrice = Model.Fiyat > varyant.SatisFiyati ? Model.Fiyat : 0;
                            var varyantMedyaUrl = !string.IsNullOrWhiteSpace(varyant.GorselUrl) ? varyant.GorselUrl : (varyantMedyaHaritasi.TryGetValue(varyant.Id, out var eslesen) ? eslesen : string.Empty);
                            var rawVb = string.IsNullOrWhiteSpace(varyant.VaryantBasligi) ? varyant.Olcu : varyant.VaryantBasligi;
                            var cleanVb = string.Join(" / ", rawVb.Split(new[] { " / " }, StringSplitOptions.RemoveEmptyEntries).Where(x => !x.Contains("Standart", StringComparison.OrdinalIgnoreCase) && !x.Contains("Bask", StringComparison.OrdinalIgnoreCase)));
                            if (string.IsNullOrWhiteSpace(cleanVb)) cleanVb = rawVb.Split('/')[0].Trim();
                            
                            <label class="relative border border-[#e5e2dc] rounded px-4 py-2 cursor-pointer transition-colors hover:border-[#b58735] has-[:checked]:border-[#313511] has-[:checked]:bg-[#313511] has-[:checked]:text-white @(!varyantSatinAlinabilir ? "opacity-50 cursor-not-allowed" : "text-[#47473d]")">
                                <input type="radio" id="variant-@varyant.Id" name="productVariant" value="@varyant.Id" class="variant-radio absolute opacity-0 w-0 h-0" @(varyant.Id == varsayilanSecenek?.Id ? "checked" : "") disabled="@(!varyantSatinAlinabilir)" data-price="@varyant.SatisFiyati" data-oldprice="@(varyantOldPrice > 0 ? varyantOldPrice.ToString(System.Globalization.CultureInfo.InvariantCulture) : string.Empty)" data-stock="@varyant.StokAdedi" data-preorder="@varyant.OnSipariseAcikMi.ToString().ToLowerInvariant()" data-image="@varyantMedyaUrl" data-label="@cleanVb">
                                <span class="text-sm font-medium">@cleanVb</span>
                            </label>
                        }
                    </div>
                </div>"""
    new_html = new_html.replace(old_variants, new_variants)

    # Apply arrows fix from fix_detay_script.py
    old_main_image = """            <div class="relative bg-[#f1ede7] aspect-square rounded-lg overflow-hidden group cursor-zoom-in" onclick="openProductLightbox()">
                <img id="mainProductImage" src="@varsayilanGaleriGorseli" data-default-src="@(varsayilanMedya?.ResimYolu ?? Model.AnaGorselUrl)" data-default-alt="@varsayilanGaleriAltMetni" data-product-name="@Model.Baslik" class="w-full h-full object-contain transition-transform duration-500 group-hover:scale-105" alt="@varsayilanGaleriAltMetni">
                <div class="absolute bottom-4 right-4 bg-white/80 backdrop-blur-sm p-2 rounded-full shadow-sm text-[#313511]">
                    <i class="fas fa-search-plus"></i>
                </div>
            </div>"""

    new_main_image = """            <div class="relative bg-[#f1ede7] aspect-square rounded-lg overflow-hidden group cursor-zoom-in" onclick="openProductLightbox()">
                <img id="mainProductImage" src="@varsayilanGaleriGorseli" data-default-src="@(varsayilanMedya?.ResimYolu ?? Model.AnaGorselUrl)" data-default-alt="@varsayilanGaleriAltMetni" data-product-name="@Model.Baslik" class="w-full h-full object-contain transition-transform duration-500 group-hover:scale-105" alt="@varsayilanGaleriAltMetni">
                
                <button type="button" class="absolute left-4 top-1/2 -translate-y-1/2 bg-white/80 backdrop-blur-sm w-10 h-10 rounded-full shadow-sm text-[#313511] flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white z-10" onclick="navigateGallery('prev', event)">
                    <i class="fas fa-chevron-left"></i>
                </button>
                <button type="button" class="absolute right-4 top-1/2 -translate-y-1/2 bg-white/80 backdrop-blur-sm w-10 h-10 rounded-full shadow-sm text-[#313511] flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white z-10" onclick="navigateGallery('next', event)">
                    <i class="fas fa-chevron-right"></i>
                </button>

                <div class="absolute bottom-4 right-4 bg-white/80 backdrop-blur-sm w-10 h-10 rounded-full shadow-sm text-[#313511] flex items-center justify-center z-10">
                    <i class="fas fa-search-plus"></i>
                </div>
            </div>"""
    new_html = new_html.replace(old_main_image, new_main_image)

    # 3. Create the javascript block
    js_content = """<script>
// Modal event listeners
document.addEventListener('DOMContentLoaded', function() {
    const desktopModal = document.getElementById('desktopLightboxModal');
    const closeBtn = document.getElementById('closeDesktopModalBtn');
    if (closeBtn && desktopModal) {
        closeBtn.addEventListener('click', () => {
            desktopModal.classList.add('hidden');
            desktopModal.classList.remove('flex');
        });
    }

    const commentModal = document.getElementById('commentModal');
    if (commentModal) {
        const openBtns = [document.getElementById('openCommentModalBtn'), document.getElementById('openCommentModalBtnEmpty')];
        openBtns.forEach(btn => btn && btn.addEventListener('click', () => {
            commentModal.classList.remove('hidden');
            commentModal.classList.add('flex');
        }));
        
        const closeCommentBtn = document.getElementById('closeCommentModalBtn');
        if (closeCommentBtn) {
            closeCommentBtn.addEventListener('click', () => {
                commentModal.classList.add('hidden');
                commentModal.classList.remove('flex');
            });
        }
    }
});

let currentZoom = 1;

function openProductLightbox() {
    if (window.innerWidth >= 1024) {
        document.getElementById('desktopLightboxModal').classList.remove('hidden');
        document.getElementById('desktopLightboxModal').classList.add('flex');
        resetDesktopZoom();
    } else {
        document.getElementById('mobileLightbox').classList.remove('hidden');
        document.getElementById('mobileLightbox').classList.add('flex');
        resetMobileZoom();
    }
}

function closeMobileLightbox() {
    document.getElementById('mobileLightbox').classList.add('hidden');
    document.getElementById('mobileLightbox').classList.remove('flex');
}

function resetMobileZoom() {
    currentZoom = 1;
    updateMobileZoom();
}

function zoomInMobile() {
    if (currentZoom < 3) { currentZoom += 0.5; updateMobileZoom(); }
}

function zoomOutMobile() {
    if (currentZoom > 1) { currentZoom -= 0.5; updateMobileZoom(); }
}

function updateMobileZoom() {
    const img = document.getElementById('mobileLightboxImage');
    if (img) img.style.transform = `scale(${currentZoom})`;
    const zl = document.getElementById('zoomLevel');
    if (zl) zl.innerText = `${Math.round(currentZoom * 100)}%`;
}

function resetDesktopZoom() {
    currentZoom = 1;
    updateDesktopZoom();
}

function zoomInDesktop() {
    if (currentZoom < 3) { currentZoom += 0.5; updateDesktopZoom(); }
}

function zoomOutDesktop() {
    if (currentZoom > 1) { currentZoom -= 0.5; updateDesktopZoom(); }
}

function updateDesktopZoom() {
    const img = document.getElementById('desktopLightboxImage');
    if (img) {
        img.style.transform = `scale(${currentZoom})`;
    }
}

function changeProductImage(imageUrl, thumbnailElement, altText) {
    const mainImage = document.getElementById('mainProductImage');
    if (mainImage) {
        mainImage.src = imageUrl;
        if (altText) mainImage.alt = altText;
    }
    
    const deskImg = document.getElementById('desktopLightboxImage');
    if (deskImg) deskImg.src = imageUrl;
    
    const mobImg = document.getElementById('mobileLightboxImage');
    if (mobImg) mobImg.src = imageUrl;
    
    document.querySelectorAll('.thumbnail-item').forEach(item => {
        item.classList.remove('border-[#313511]');
        item.classList.add('border-transparent');
    });
    if (thumbnailElement) {
        thumbnailElement.classList.remove('border-transparent');
        thumbnailElement.classList.add('border-[#313511]');
        thumbnailElement.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
}

document.querySelectorAll('.variant-radio').forEach(radio => {
    radio.addEventListener('change', function() {
        if (this.checked) {
            const price = parseFloat(this.getAttribute('data-price')) || 0;
            const oldPrice = parseFloat(this.getAttribute('data-oldprice')) || 0;
            const imageUrl = this.getAttribute('data-image');
            const label = this.getAttribute('data-label');
            const isPreorder = this.getAttribute('data-preorder') === 'true';
            const stock = parseInt(this.getAttribute('data-stock')) || 0;
            
            const selectedVariantId = document.getElementById('selectedVariantId');
            if (selectedVariantId) selectedVariantId.value = this.value;
            
            const priceDisplay = document.getElementById('priceDisplay');
            if (priceDisplay) priceDisplay.innerHTML = `${price.toLocaleString('tr-TR', {minimumFractionDigits: 2})} TL`;
            
            const oldPriceDisplay = document.getElementById('oldPriceDisplay');
            const discountBadge = document.getElementById('discountBadge');
            
            if (oldPrice > price) {
                if (oldPriceDisplay) {
                    oldPriceDisplay.innerHTML = `${oldPrice.toLocaleString('tr-TR', {minimumFractionDigits: 2})} TL`;
                    oldPriceDisplay.classList.remove('hidden');
                }
                if (discountBadge) {
                    const discount = Math.round((1 - (price / oldPrice)) * 100);
                    discountBadge.innerHTML = `%${discount} İndirim`;
                    discountBadge.classList.remove('hidden');
                }
            } else {
                if (oldPriceDisplay) oldPriceDisplay.classList.add('hidden');
                if (discountBadge) discountBadge.classList.add('hidden');
            }
            
            if (imageUrl) {
                changeProductImage(imageUrl, null, label);
            }
            
            const variantSummary = document.getElementById('variantSummaryText');
            if (variantSummary) {
                variantSummary.innerHTML = `<i class="fas fa-layer-group mr-1.5"></i> ${label}`;
                variantSummary.classList.remove('hidden');
            }
            
            const stockStatusText = document.getElementById('stockStatusText');
            if (stockStatusText) {
                if (stock > 0) {
                    stockStatusText.innerHTML = `<i class="fas fa-check-circle text-green-600"></i> Stokta`;
                } else if (isPreorder) {
                    stockStatusText.innerHTML = `<i class="fas fa-clock text-blue-600"></i> Ön Siparişe Açık`;
                } else {
                    stockStatusText.innerHTML = `<i class="fas fa-times-circle text-red-600"></i> Tükendi`;
                }
            }
            
            const quantityInput = document.getElementById('productQuantity');
            if (quantityInput) {
                quantityInput.value = 1;
                quantityInput.max = stock > 0 ? stock : (isPreorder ? 99 : 1);
            }
        }
    });
});

function increaseQuantity() {
    const input = document.getElementById('productQuantity');
    const selectedInput = document.getElementById('selectedQuantity');
    if (!input) return;
    
    let max = parseInt(input.getAttribute('max')) || 99;
    let val = parseInt(input.value) || 1;
    if (val < max) {
        input.value = val + 1;
        if (selectedInput) selectedInput.value = val + 1;
    }
}

function decreaseQuantity() {
    const input = document.getElementById('productQuantity');
    const selectedInput = document.getElementById('selectedQuantity');
    if (!input) return;
    
    let min = parseInt(input.getAttribute('min')) || 1;
    let val = parseInt(input.value) || 1;
    if (val > min) {
        input.value = val - 1;
        if (selectedInput) selectedInput.value = val - 1;
    }
}

const ajaxSepetBtn = document.getElementById('ajaxSepetBtn');
if (ajaxSepetBtn) {
    ajaxSepetBtn.addEventListener('click', function (e) {
        e.preventDefault();
        const form = document.getElementById('addToCartForm');
        const formData = new FormData(form);
        const token = form.querySelector('input[name="__RequestVerificationToken"]')?.value || '';
        
        let url = `/Sepet/Ekle?UrunId=${formData.get('UrunId')}&Adet=${formData.get('Adet')}`;
        if (formData.get('SecenekId')) url += `&SecenekId=${formData.get('SecenekId')}`;
        
        const originalHtml = this.innerHTML;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Ekleniyor...';
        this.disabled = true;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'RequestVerificationToken': token
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.innerHTML = '<i class="fas fa-check"></i> Eklendi';
                this.style.background = '#4CAF50';
                this.style.borderColor = '#4CAF50';
                
                const cartCounter = document.getElementById('cartItemCount');
                if (cartCounter) {
                    let current = parseInt(cartCounter.innerText) || 0;
                    let added = parseInt(formData.get('Adet')) || 1;
                    cartCounter.innerText = current + added;
                }

                setTimeout(() => {
                    this.innerHTML = originalHtml;
                    this.style.background = '';
                    this.style.borderColor = '';
                    this.disabled = false;
                }, 2000);
            } else {
                alert(data.message || 'Hata oluştu');
                this.innerHTML = originalHtml;
                this.disabled = false;
            }
        })
        .catch(error => {
            console.error(error);
            alert('Bağlantı hatası');
            this.innerHTML = originalHtml;
            this.disabled = false;
        });
    });
}

function navigateGallery(direction, event) {
    if (event) event.stopPropagation();
    
    const thumbnails = Array.from(document.querySelectorAll('.thumbnail-item'));
    if (thumbnails.length <= 1) return;
    
    const mainImage = document.getElementById('mainProductImage');
    const currentSrc = mainImage.getAttribute('src');
    
    let currentIndex = thumbnails.findIndex(item => item.getAttribute('data-image') === currentSrc);
    if (currentIndex === -1) currentIndex = 0;
    
    let nextIndex;
    if (direction === 'next') {
        nextIndex = (currentIndex + 1) % thumbnails.length;
    } else {
        nextIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
    }
    
    const nextThumb = thumbnails[nextIndex];
    if (nextThumb) {
        nextThumb.click();
    }
}
</script>
"""

    final_content = header + "\n" + new_html + "\n" + js_content

    with open(r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Urun\Detay.cshtml", "w", encoding="utf-8") as f:
        f.write(final_content)

build_detay()

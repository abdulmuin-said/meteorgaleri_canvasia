import re

file_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Urun\Detay.cshtml"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix seciliVaryantMetni
old_varyant_metni = """    var seciliVaryantMetni = varsayilanSecenek != null
        ? (string.IsNullOrWhiteSpace(varsayilanSecenek.VaryantBasligi) ? "Varsayilan varyasyon" : varsayilanSecenek.VaryantBasligi)
        : string.Empty;"""
new_varyant_metni = """    var rawVaryantMetni = varsayilanSecenek != null 
        ? (string.IsNullOrWhiteSpace(varsayilanSecenek.VaryantBasligi) ? (varsayilanSecenek.Olcu ?? "Standart") : varsayilanSecenek.VaryantBasligi) 
        : string.Empty;
    var seciliVaryantMetni = string.Join(" / ", rawVaryantMetni.Split(new[] { " / " }, StringSplitOptions.RemoveEmptyEntries).Where(x => !x.Contains("Standart", StringComparison.OrdinalIgnoreCase) && !x.Contains("Bask", StringComparison.OrdinalIgnoreCase)));
    if (string.IsNullOrWhiteSpace(seciliVaryantMetni) && !string.IsNullOrWhiteSpace(rawVaryantMetni)) seciliVaryantMetni = rawVaryantMetni.Split('/')[0].Trim();"""

content = content.replace(old_varyant_metni, new_varyant_metni)

# 2. Fix Price Display
old_price = """<span id="priceDisplay" class="font-serif text-3xl text-[#1c1c18]">@currencySymbol @gosterilecekFiyat.ToString("N2")</span>"""
new_price = """<span id="priceDisplay" class="font-sans text-2xl font-medium tracking-tight text-[#1c1c18]">@gosterilecekFiyat.ToString("N2") @currencySymbol</span>"""
content = content.replace(old_price, new_price)

old_old_price = """<span id="oldPriceDisplay" class="text-lg text-[#47473d] line-through mb-1">@currencySymbol @gosterilecekEskiFiyat.Value.ToString("N2")</span>"""
new_old_price = """<span id="oldPriceDisplay" class="text-lg text-[#47473d] line-through mb-1 font-sans">@gosterilecekEskiFiyat.Value.ToString("N2") @currencySymbol</span>"""
content = content.replace(old_old_price, new_old_price)

# 3. Clean up Meta Info
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
content = content.replace(old_meta, new_meta)

# 4. Clean up Variants block
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
content = content.replace(old_variants, new_variants)

# 5. Fix JS formatting for priceDisplay update
old_js_price = """function updatePriceDisplay(price, oldPrice) {
    const oldPriceElement = document.getElementById('oldPriceDisplay');
    const discountBadge = document.getElementById('discountBadge');
    document.getElementById('priceDisplay').textContent = '@currencySymbol ' + formatPrice(price);

    if (oldPrice && oldPrice > price) {
        const discountPercent = Math.round((1 - (price / oldPrice)) * 100);
        oldPriceElement.textContent = '@currencySymbol ' + formatPrice(oldPrice);"""

new_js_price = """function updatePriceDisplay(price, oldPrice) {
    const oldPriceElement = document.getElementById('oldPriceDisplay');
    const discountBadge = document.getElementById('discountBadge');
    document.getElementById('priceDisplay').textContent = formatPrice(price) + ' @currencySymbol';

    if (oldPrice && oldPrice > price) {
        const discountPercent = Math.round((1 - (price / oldPrice)) * 100);
        oldPriceElement.textContent = formatPrice(oldPrice) + ' @currencySymbol';"""
content = content.replace(old_js_price, new_js_price)

# 6. Add JS for Sepete Ekle
js_to_add = """
    // AJAX Sepete Ekle
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
                    
                    // Update cart count
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
"""

content = content.replace("</script>", js_to_add + "\n</script>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Detay.cshtml updated with fixes")

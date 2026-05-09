import re

file_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Urun\Detay.cshtml"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove ALL instances of the injected AJAX Sepete Ekle
ajax_block_pattern = re.compile(r"// AJAX Sepete Ekle.*?\}\s*\}\s*", re.DOTALL)
content = re.sub(ajax_block_pattern, "", content)

# 2. Fix the missing </script><script> around ld+json
bad_script_block = """<script type="application/ld+json">
@Html.Raw(productSchema)

// Modal event listeners"""

good_script_block = """<script type="application/ld+json">
@Html.Raw(productSchema)
</script>

<script>
// Modal event listeners"""
content = content.replace(bad_script_block, good_script_block)

# 3. Add the Navigation Arrows to mainProductImage
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
content = content.replace(old_main_image, new_main_image)

# 4. Update changeProductImage logic to fix active border class
old_change_image = """    // Thumbnail aktifliğini güncelle
    document.querySelectorAll('.thumbnail-item').forEach(item => {
        item.classList.remove('active');
    });
    if (thumbnailElement) {
        thumbnailElement.classList.add('active');
    
    // Lightbox'ları resetle"""

new_change_image = """    // Thumbnail aktifliğini güncelle
    document.querySelectorAll('.thumbnail-item').forEach(item => {
        item.classList.remove('border-[#313511]');
        item.classList.add('border-transparent');
    });
    if (thumbnailElement) {
        thumbnailElement.classList.remove('border-transparent');
        thumbnailElement.classList.add('border-[#313511]');
        
        // Aktif thumbnail'ı görünür yap
        thumbnailElement.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
    
    // Lightbox'ları resetle"""
content = content.replace(old_change_image, new_change_image)

# Remove the duplicated scrollIntoView that was in the original because it was malformed
old_scroll = """    // Aktif thumbnail'ı görünür yap
    thumbnailElement.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }

    resetDesktopZoom();"""
new_scroll = """    resetDesktopZoom();"""
content = content.replace(old_scroll, new_scroll)


# 5. Add our JS payload
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

// Galeri Navigasyonu
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
"""

# Append it properly before the LAST </script> tag
last_script_index = content.rfind("</script>")
if last_script_index != -1:
    content = content[:last_script_index] + js_to_add + "\n" + content[last_script_index:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Detay.cshtml fully fixed and navigateGallery added.")

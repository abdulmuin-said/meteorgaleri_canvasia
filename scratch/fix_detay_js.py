import re

file_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Urun\Detay.cshtml"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's find the start of the "// Modal event listeners"
start_str = "// Modal event listeners"
start_idx = content.find(start_str)

if start_idx != -1:
    # Everything before start_idx is good.
    # I will replace the REST of the file starting from start_str with my clean Javascript,
    # except the final </script> tag
    
    clean_js = """// Modal event listeners
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

// Ürün Adedi Değiştirme
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
</script>
"""

    content = content[:start_idx] + clean_js

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Detay.cshtml JS block completely cleaned up and missing functions added.")
else:
    print("Could not find start_str!")

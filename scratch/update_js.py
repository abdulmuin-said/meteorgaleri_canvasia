import re

file_path = r"E:\Projeler\MeteorGaleri\KanvasProje.Web\Views\Urun\Detay.cshtml"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace openProductLightbox
old_open = """function openProductLightbox() {
    if (window.innerWidth > 768) {
        // Desktop: Bootstrap modal aÃƒÂ§
        const lightboxModal = new bootstrap.Modal(document.getElementById('desktopLightboxModal'));
        const mainImage = document.getElementById('mainProductImage');
        const imageSrc = mainImage.src;
        const imageAlt = mainImage.alt || mainImage.getAttribute('data-default-alt') || '';
        
        document.getElementById('desktopLightboxImage').src = imageSrc;
        document.getElementById('desktopLightboxImage').alt = imageAlt;
        resetDesktopZoom();
        
        lightboxModal.show();
    } else {"""

new_open = """function openProductLightbox() {
    if (window.innerWidth > 768) {
        // Desktop: Custom modal
        const lightboxModal = document.getElementById('desktopLightboxModal');
        const mainImage = document.getElementById('mainProductImage');
        const imageSrc = mainImage.src;
        const imageAlt = mainImage.alt || mainImage.getAttribute('data-default-alt') || '';
        
        document.getElementById('desktopLightboxImage').src = imageSrc;
        document.getElementById('desktopLightboxImage').alt = imageAlt;
        resetDesktopZoom();
        
        lightboxModal.classList.remove('hidden');
        lightboxModal.classList.add('flex');
    } else {"""

content = content.replace(old_open, new_open)

old_esc = """// ESC tuÃ…Å¸u ile lightbox kapatma
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Mobile lightbox kapat
        closeMobileLightbox();
        
        // Desktop lightbox kapat
        const desktopModal = bootstrap.Modal.getInstance(document.getElementById('desktopLightboxModal'));
        if (desktopModal) {
            desktopModal.hide();
        }
    }
});"""

new_esc = """// ESC tuÃ…Å¸u ile lightbox kapatma
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Mobile lightbox kapat
        closeMobileLightbox();
        
        // Desktop lightbox kapat
        const desktopModal = document.getElementById('desktopLightboxModal');
        if (desktopModal) {
            desktopModal.classList.add('hidden');
            desktopModal.classList.remove('flex');
        }
        
        // Comment modal
        const commentModal = document.getElementById('commentModal');
        if (commentModal) {
            commentModal.classList.add('hidden');
            commentModal.classList.remove('flex');
        }
    }
});"""

content = content.replace(old_esc, new_esc)

# Add event listeners to the end
js_to_add = """
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
"""

content = content.replace("</script>", js_to_add + "\n</script>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("JS updated")
